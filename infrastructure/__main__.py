"""An AWS Python Pulumi program"""

import pulumi
from src.infrastructure.network.vpc.main import vpc as main_vpc
import pulumi_awsx as awsx
from src.infrastructure.containers.ecs.main import cluster as main_ecs_cluster
from src.infrastructure.containers.ecr.main import repository as main_ecr
from src.infrastructure.alb.main import alb as main_alb
from src.workload.applications.common import main as applications
from src.infrastructure.dns import primary as primary_dns
from src.infrastructure.acm import main as ssl_cert
from src.infrastructure.api_gateway.main import api_gw as main_api_gateway
from src.infrastructure.cognito.main import user_pool
from src.infrastructure.iam.iam import create_user
import pulumi_aws as aws
import json
import yaml

config = pulumi.Config()
aws_config = pulumi.Config("aws")
aws_region = aws_config.require("region")
aws_env = config.require("env")

# Create main vpc
vpc_config = json.loads(config.require("vpc"))
main_vpc = main_vpc.create(vpc_config['main'])

# Create main cluster ecs
containers_config = json.loads(config.require("containers"))
main_ecs_cluster = main_ecs_cluster.create(containers_config['ecs']['clusters']['main'])

# Create dns zones
dns_zones_config = json.loads(config.require("dns"))
primary_dns_zone = aws.route53.get_zone(name=dns_zones_config['primary']['name'])


# Create ACM certificates
ssl_cert_config = json.loads(config.require("ssl-certs"))
main_ssl_cert = ssl_cert.create(
    ssl_cert_config['main'],
    primary_dns_zone
)

main_ssl_cert_us_east_1 = ssl_cert.create(
    ssl_cert_config['main'],
    primary_dns_zone,
    'us-east-1',
    create_records=False
)

# Create main load balancer resource
alb_config = json.loads(config.require("alb"))
main_alb, https_listener, alb_domain = main_alb.create(
    alb_config['main'],
    main_vpc,
    main_ssl_cert,
    dns_zone=primary_dns_zone
)

primary_dns.create(dns_zones_config['primary'], main_alb)
# Deploy Cognito user pool
cognito_config = json.loads(config.require("cognito"))
main_user_pool, main_user_pool_default_app_client = user_pool.create(
    cognito_config['user_pool']['main'],
    ssl_cert=main_ssl_cert_us_east_1,
    dns_zone=primary_dns_zone,
    alb=main_alb
)

# Provides an IAM access key for setting of credentials that allow API requests to be made as an IAM user.
iam_config = json.loads(config.require("iam"))
for name in iam_config['users']:
    create_user(name, iam_config['pgp_key'])

# Deploy API Gateway
api_gateway_config = json.loads(config.require("api-gateway"))
main_api_gateway = main_api_gateway.create(
    api_gateway_config['main'],
    cognito_user_pool=main_user_pool,
    cognito_default_app_client=main_user_pool_default_app_client,
    ssl_cert=main_ssl_cert,
    dns_zone=primary_dns_zone
)

rds_config = json.loads(config.require("rds"))["main"]

app_config = json.loads(config.require("app"))
security_group = aws.ec2.SecurityGroup(
    "{}-svc-sg".format(app_config["name"]),
    vpc_id=main_vpc.vpc_id,
    description="Enable HTTP 8080 access",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=3306,
                to_port=3306,
                cidr_blocks=[vpc_config['main']['cidr']], # FargateのIPアドレス
            ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=3306,
            to_port=3306,
            cidr_blocks=["159.28.73.98/32"], # 自分たちのIPアドレス
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
)

public_subnet_ids = main_vpc.public_subnet_ids
my_subnet = public_subnet_ids.apply(lambda subnet_id: subnet_id)

# pulumi.export('all_subnets', all_subnets)

rds_subnet_group = aws.rds.SubnetGroup(
    "{}_rds_subnet_group".format(rds_config["database"]['db_name']),
    subnet_ids=my_subnet
)

# Create an RDS instance within the VPC
rds_instance = aws.rds.Instance(
    '{}-rds-instance'.format(rds_config["database"]['db_name']),
    allocated_storage=20,
    storage_type="gp2",
    engine=rds_config["engine"],
    engine_version=rds_config["version"],
    instance_class=rds_config["instance_type"],
    db_name=rds_config["database"]["db_name"],
    username=rds_config["database"]["username"],
    password=rds_config["database"]["password"],  # In a real scenario, use Pulumi's secret handling
    vpc_security_group_ids=[security_group.id],
    db_subnet_group_name=rds_subnet_group.name,
    # Associate the RDS instance with the security group
    skip_final_snapshot=True,
)

pulumi.export('rds_endpoint', rds_instance.endpoint)

# Deploy applications
for application in containers_config['ecs']['applications']:
    # geeksnipe_notification_system_svc
    service_name = application["name"].rsplit('_')[0]
    app_name = application["name"].replace(service_name+'_', '')
    with open(f"src/workload/applications/{service_name}/{app_name}/ecs_application.{aws_env}.yml", "r") as file:
        application_config = yaml.load(file, Loader=yaml.FullLoader)

    # Create ECR repository
    repo_image = main_ecr.create(
        f"{service_name}-{app_name}",
        f"./../{application['dockerfile_root_folder_path']}"
    )

    # Deploy application
    applications.create(
        application=f"{service_name}.{app_name}",
        application_config=application_config,
        ecs_cluster=main_ecs_cluster,
        vpc=main_vpc,
        alb=main_alb,
        https_listener=https_listener,
        dns_zone=primary_dns_zone,
        primary_dns_zone_name=primary_dns_zone.name,
        api_gw=main_api_gateway,
        repo_image=repo_image,
        task_num=containers_config['ecs']['task']["count"],
        security_group=security_group,
        rds_host=rds_instance.endpoint.apply(lambda endpoint: endpoint.split(':')[0]),
        rds_config=rds_config
    )
