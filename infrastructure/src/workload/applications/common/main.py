import json
import pulumi_aws as aws
import pulumi
import src.library.common.naming as naming
from src.library.common.registry import registry
import importlib
import importlib.util
from pulumi import Output
aws_config = pulumi.Config("aws")
aws_region = aws_config.require("region")
config = pulumi.Config()


def create(
        application,
        application_config,
        ecs_cluster,
        vpc,
        alb,
        https_listener,
        dns_zone,
        primary_dns_zone_name,
        api_gw,
        repo_image,
        task_num,
        security_group,
        rds_host,
        rds_config):
    application_module = importlib.import_module(
        f"src.workload.applications.{application}.main",
        package=None
    )

    # IAM roles and Policies
    task_execution_role = aws.iam.Role(
        "{}-ecs-task-execution-role".format(application_config['name']),
        assume_role_policy=json.dumps({
            "Version": "2008-10-17",
            "Statement": [{
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ecs-tasks.amazonaws.com"
                },
                "Action": "sts:AssumeRole",
            }]
        }),
    )

    task_role = aws.iam.Role(
        "{}-ecs-task-role".format(application_config['name']),
        assume_role_policy=json.dumps({
            "Version": "2008-10-17",
            "Statement": [{
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ecs-tasks.amazonaws.com"
                },
                "Action": "sts:AssumeRole",
            }]
        }),
    )

    policy_arns_to_attach = [
        "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
        "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
    ]
    for i, policy_arn in enumerate(policy_arns_to_attach):
        aws.iam.RolePolicyAttachment(
            "{}-ecs-task-execution-role-policy-{}".format(application_config['name'], i),
            role=task_execution_role,
            policy_arn=policy_arn,
        )

    # secrets_manager_policy_document = aws.iam.get_policy_document(
    #     statements=[aws.iam.GetPolicyDocumentStatementArgs(
    #         effect="Allow",
    #         actions=["secretsmanager:GetSecretValue"],
    #         resources=[application_config['secrets_manager']['secret_arn']],
    #     )])

    # secrets_manager_policy = aws.iam.Policy(
    #     "{}-secrets-manager-policy".format(application_config['name']),
    #     description="Policy for retrieving application secrets",
    #     policy=secrets_manager_policy_document.json)

    # aws.iam.RolePolicyAttachment(
    #     "{}-secrets-manager-attachment".format(application_config['name']),
    #     role=task_execution_role.name,
    #     policy_arn=secrets_manager_policy.arn)

    # Attach specific permissions
    application_module.ecs_task_attach_policies(
        task_role=task_role,
        application_config=application_config
    )

    # Log group
    log_group_name = '/ecs/task/{}'.format(application_config['name'])
    aws.cloudwatch.LogGroup(
        '{}-log-group'.format(application_config['name']),
        args=aws.cloudwatch.LogGroupArgs(name=log_group_name)
    )

    image_name_str = repo_image.repository_url.apply(lambda url: url + ":" + application_config['task']['tag'])
    container_definition = pulumi.Output.all(
        image_name_str,
        application_config,
        log_group_name,
        aws_region,
        rds_config,
        rds_host
    ).apply(lambda args: generate_container_definitions(
        args[0],
        args[1],
        args[2],
        args[3],
        args[4],
        args[5],
    ))

    # Task definition
    task_definition = aws.ecs.TaskDefinition(
        "{}-task".format(application_config['name']),
        family=application_config['name'],
        cpu=application_config['task']['cpu'],
        memory=application_config['task']['memory'],
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=task_execution_role.arn,
        task_role_arn=task_role.arn,
        container_definitions=container_definition
    )

    # Load balancer
    target_group = aws.lb.TargetGroup(
        "{}-tg".format(application_config['name']),
        port=80,
        protocol="HTTP",
        target_type="ip",
        vpc_id=vpc.vpc_id,
        health_check=aws.lb.TargetGroupHealthCheckArgs(
            path=application_config['service']['health_check']['path'],
            matcher=application_config['service']['health_check']['matcher'],
            healthy_threshold=int(application_config['service']['health_check']['healthy_threshold']),
            interval=int(application_config['service']['health_check']['interval']),
            timeout=int(application_config['service']['health_check']['timeout']),
            unhealthy_threshold=int(application_config['service']['health_check']['unhealthy_threshold'])
        )
    )

    host_header = '{}.{}'.format(
        application_config['service']['alb']['listener_rule']['host'],
        primary_dns_zone_name
    )

    aws.lb.ListenerRule(
        "{}-alb-listener-rule".format(application_config['name']),
        listener_arn=https_listener.arn.apply(lambda listener_arn: listener_arn),
        priority=int(application_config['service']['alb']['listener_rule']['priority']),
        actions=[aws.lb.ListenerRuleActionArgs(
            type="forward",
            target_group_arn=target_group.arn,
        )],
        conditions=[
            aws.lb.ListenerRuleConditionArgs(
                host_header=aws.lb.ListenerRuleConditionHostHeaderArgs(
                    values=[host_header],
                ),
            ),
        ])

    # Service
    aws.ecs.Service(
        "{}-ecs-svc".format(application_config['name']),
        cluster=ecs_cluster.arn,
        desired_count=task_num,
        launch_type="FARGATE",
        task_definition=task_definition.arn,
        network_configuration={
            "assign_public_ip": "true",
            "subnets": vpc.public_subnet_ids,
            "security_groups": [security_group.id]
        },
        load_balancers=[{
            "target_group_arn": target_group.arn.apply(lambda arn: arn),
            "container_name": application_config['name'],
            "container_port": application_config['task']['container']['port']
        }],
        opts=pulumi.ResourceOptions(
            depends_on=[
                target_group
            ],
            custom_timeouts=pulumi.CustomTimeouts(create='1m')
        )
    )

    dns_record = aws.route53.Record(
        "{}-dns-record".format(application_config['name']),
        zone_id=dns_zone.zone_id,
        name=application_config['service']['alb']['listener_rule']['host'],
        type="A",
        aliases=[aws.route53.RecordAliasArgs(
            name=alb.dns_name,
            zone_id=alb.zone_id,
            evaluate_target_health=True,
        )])

    # API Gateway integration
    integration_uri = "https://{}.{}".format(
        application_config['service']['alb']['listener_rule']['host'],
        primary_dns_zone_name
    )
    api_gw_integration = aws.apigatewayv2.Integration(
        naming.get('api-gateway-integration', application_config['name']),
        api_id=api_gw.id,
        integration_type="HTTP_PROXY",
        integration_method="ANY",
        integration_uri=integration_uri + "/{proxy}")

    api_gw_route = aws.apigatewayv2.Route(
        naming.get('api-gateway-route', application_config['name']),
        api_id=api_gw.id,
        route_key="ANY /" + application_config['name'] + "/{proxy+}",
        target=api_gw_integration.id.apply(lambda integration_id: f"integrations/{integration_id}"),
        authorization_type='JWT',
        authorizer_id=registry.get('main_api_gateway_jwt_autorizer')
    )

    aws.apigatewayv2.Deployment(
        naming.get('api-gateway-deployment', application_config['name']),
        api_id=api_gw.id,
        description='{} deployment'.format(application_config['name']),
        opts=pulumi.ResourceOptions(
            depends_on=[
                api_gw_route
            ]
        )
    )

    pulumi.export(
        '{} Public DNS Record'.format(application_config['name']),
        dns_record.fqdn.apply(lambda fqdn: f"https://{fqdn}")
    )

    api_gateway_config = json.loads(config.require("api-gateway"))
    pulumi.export(
        '{} API Gateway Route'.format(application_config['name']),
        'https://{}/{}'.format(
            api_gateway_config['main']['dns'],
            application_config['name']
        )
    )


def generate_container_definitions(
    repo_name,
    application_config,
    log_group_name,
    _aws_region,
    rds_config,
    rds_host
) -> str:
    return json.dumps([
        {
            "name": application_config['name'],
            "image": repo_name,
            "cpu": application_config['task']['cpu'],
            "memory": application_config['task']['memory'],
            "portMappings": [
                {
                    "containerPort": application_config['task']['container']['port'],
                    "hostPort": application_config['task']['container']['port'],
                    "protocol": "tcp"
                }
            ],
            "essential": True,
            "logConfiguration": {
                "logDriver": "awslogs",
                "secretOptions": None,
                "options": {
                    "awslogs-group": log_group_name,
                    "awslogs-region": _aws_region,
                    "awslogs-stream-prefix": "ecs"
                }
            },
            "environment": [                 # Add your environment variables here
                {"name": "DEBUG", "value": "False"},
                {"name": "PORT", "value": "3306"},
                {"name": "USERNAME", "value": rds_config["database"]["username"]},
                {"name": "USERPASS", "value": rds_config["database"]["password"]},
                {"name": "DATABASE", "value": rds_config["database"]["db_name"]},
                {"name": "HOST", "value": rds_host},
                {"name": "GOOGLE_OAUTH2_KEY", "value": "688579648389-hq3knplkm4a9bdc232ngqct7fqrl416n.apps.googleusercontent.com"},
                {"name": "GOOGLE_OAUTH2_SECRET","value": "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"},
                {"name": "GOOGLE_AD_API_DEVELOPER_TOKEN", "value": "P7Zm5PaLk6bje9AYgpA6Zw"},
                {"name": "GOOGLE_REFRESH_TOKEN", "value": "1//0e5bQK3kcLR_zCgYIARAAGA4SNwF-L9IrgAE9CRuoMXpOvcsptFFHVie5qri79TMlpl2Mpy_l-RZ7M7ody9xUJ9kfiA-f9EICYbg"},

                {"name": "JWT_SECRET_KEY", "value": "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"},
                {"name": "JWT_REFRESH_SECRET_KEY", "value": "P7Zm5PaLk6bje9AYgpA6Zw"},
                {"name": "MY_ORIGIN", "value": "https://geeksnipe.com"},
                {"name": "OPEN_AI_API", "value": "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"},
                {"name": "TYPE", "value": "service_account"},
                {"name": "PROJECT_ID", "value": "pro-variety-402818"},

                {"name": "PRIVATE_KEY_ID", "value": "45c397be2abafab6e7d499b9e85d8d93854f3519"},
                {"name": "PRIVATE_KEY", "value": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2Gi8Q59pdgPt6\nTYqmJMiaSSb9FXIa4Kje0sDKb3johk6dzZ9WU/8YcKR4HRJmnvT2pK3y54O4VdJz\nbhPk7t1rcWCD0otRkmrttX7cixQSsLkkLkaK5T9Rr8ycgW4LNEqoT0qkxRgcDgWc\nXL9QMQqsR6ya1ln0u5AYCN92cb5o9vDtd+dzYh6myAm0EOBdTvP8NEWOQuRI4IfE\nKdDtRrfz5MPzhLMbjMxNWq5VsOoUjaeRmesWHfAj2jDsc6q3fO64JlKB1yJghUxj\n8o41b83XILNkF+/JnV2TnZmKMGTNWld05EXP5cK31PJYO02QfTIDWkiCJtpf2JDF\npWr0aHgdAgMBAAECggEAC4maqEtMTEbPCBdwHKkxdYcDe573eQj5Yg6/zMOlyTOz\nOO/Nc9qEC9AdN4f+Abb6BcN2yvBMqen0GMClbYiNylAnYYq+LXelozRv2njMV4fP\nXyG4cfXm3l3RTKwtpPOV9FZ7v/dF2QcxZ1AABgxpZPNwlenVTrpwfXlYcShxPDSn\no2qPUWG3ddsZiONrEfznSzzNyEsMSO1DgemRWLdbDoGynhzYyK7/76OOhEZhTunI\n/UsdYe83FDm3kKMDRcQd/i3UKwr86jQ3Y4uEBZ+7M5u7wEnIsmblbVufz9/W/wyY\nWGViXQH6wi8m9gmXdoTUKQBWOPONUikYfEw+HSLzYQKBgQDshZHpYSC2vfFY9cQP\nITFtdB8lsIpSH/70/037WNG7jqQLhV3VNvQ5XSfjGV0IkxbPHsC3ko2sb3FaBoJF\nkyRhW0ICBeahiQALifUQ+8RvHlgTo5XjQb/KxnmtSvv9Q5fecVrXAZcGgKiox9FC\ng3gG4EEV2i4AMc6SPm3dQIwQoQKBgQDFGVMO5A9CumUCKEUFTo0hqHW755iRa+FA\n8bT2GZW48Jq99b69nZWvLq87RSaDqqx5d4MjQ+aEQmjiGOj4NtVSktWG6qDdfrdb\nORiootGm7YBUKeb2ABljQD5wTvKg2grEiih7f2qZ/OKiLde9ZEXBNjYNoYcdrVfG\nvQ6fBOpp/QKBgQCt8wI/2M4deA5zNbTux6O5cuihaHgiNCPnfYiVrVn6jcp6Kqi6\n8cKmGawHKpUwhDUHOP/VQrRtODzuT9EpaDEeZOZj5IEdFkvxMJIK3o82heOS9gF7\ndNSgRl4gpAA14KtlzopXjHTNNHxWPTbaqyPwMqfLcX3ZaMga6E0Wpq0cYQKBgB0Z\nnBW6vjYP5xHmeCpMarHpeViA3Rm7X8qC5UDgjiZ7/5zER6EfPxZaQizyDLmr3UMh\nzg7K26HzXCDlpJ/hGKXUYApHYfDR4KhrSaS8RU/sCOJkPWFcqmLo/U7/mPr+tlBG\nRavWKBsMJzniotOnllTseBaTHqvXB/qjtyDrTODRAoGAVcfCZMgS/OmYC9igSVW4\n7U42GI2FshueMRI7L0W2+uNRa3bNJjD4USOP0ycpOy6HQAOUm32JoMFsdQAiA09c\ntPP/WSrMh2MydOvrAeeo6l1wp6k5+rdGs13HbjrKtEoilTeuviaNuoy7Xo/vV56z\nUAm1S1b5jBbt1+WD3xkQRho=\n-----END PRIVATE KEY-----\n"},
                {"name": "CLIENT_EMAIL", "value": "google-ads-helper@pro-variety-402818.iam.gserviceaccount.com"},
                {"name": "CLIENT_ID", "value": "106511779660489082427"},

                {"name": "AUTH_URI", "value": "https://accounts.google.com/o/oauth2/auth"},
                {"name": "TOKEN_URI", "value": "https://oauth2.googleapis.com/token"},
                {"name": "AUTH_PROVIDER_CERT_URI", "value": "https://www.googleapis.com/oauth2/v1/certs"},
                {"name": "CLIENT_CERT_URI", "value": "https://www.googleapis.com/robot/v1/metadata/x509/google-ads-helper%40pro-variety-402818.iam.gserviceaccount.com"},
                {"name": "DOMAIN", "value": "googleapis.com"},
                {"name": "DEV_TO_API_KEY", "value": "vBZBLGVTp9P7a6kg2RtnKpaJ"},
            ]
        }
    ])
