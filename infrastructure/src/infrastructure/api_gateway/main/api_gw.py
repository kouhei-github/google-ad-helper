import pulumi
import pulumi_aws as aws
import src.library.common.naming as naming
from src.library.common.registry import registry

config = pulumi.Config()
aws_env = config.require("env")
aws_config = pulumi.Config("aws")
aws_region = aws_config.require("region")


def create(
        api_gw_config,
        cognito_user_pool,
        cognito_default_app_client,
        ssl_cert,
        dns_zone
):
    api = aws.apigatewayv2.Api(
        naming.get('api-gateway', api_gw_config['name']),
        protocol_type="HTTP")

    stage = aws.apigatewayv2.Stage(
        naming.get('api-gateway-stage', api_gw_config['name']),
        name=api_gw_config['stage'],
        api_id=api.id)

    api_domain_name = aws.apigatewayv2.DomainName(
        naming.get('api-gw-dns', api_gw_config['name']),
        domain_name=api_gw_config['dns'],
        domain_name_configuration=aws.apigatewayv2.DomainNameDomainNameConfigurationArgs(
            certificate_arn=ssl_cert.arn.apply(lambda ssl_cert_arn: ssl_cert_arn),
            endpoint_type="REGIONAL",
            security_policy="TLS_1_2",
        ), opts=pulumi.ResourceOptions(
            depends_on=[
                ssl_cert,
                registry.get('main_ssl_cert_dns_record'),
                registry.get('main_ssl_cert_validation')
            ],
            custom_timeouts=pulumi.CustomTimeouts(create='5m')
        )
    )
    aws.route53.Record(
        naming.get('api-gw-dns-record', api_gw_config['name']),
        name=api_domain_name.domain_name,
        type="A",
        zone_id=dns_zone.zone_id,
        aliases=[aws.route53.RecordAliasArgs(
            name=api_domain_name.domain_name_configuration.target_domain_name,
            zone_id=api_domain_name.domain_name_configuration.hosted_zone_id,
            evaluate_target_health=False,
        )])

    aws.apigatewayv2.ApiMapping(
        naming.get('api-gw-dns-mapping', api_gw_config['name']),
        api_id=api.id,
        domain_name=api_domain_name.domain_name,
        stage=stage.id)

    authorizer = aws.apigatewayv2.Authorizer(
        naming.get('api-gw-authorizer', api_gw_config['name']),
        api_id=api.id,
        authorizer_type="JWT",
        identity_sources=['$request.header.Authorization'],
        jwt_configuration=aws.apigatewayv2.AuthorizerJwtConfigurationArgs(
            audiences=[cognito_default_app_client.id],
            issuer=cognito_user_pool.id.apply(
                lambda pool_id: f"https://cognito-idp.{aws_region}.amazonaws.com/{pool_id}")
        )
    )

    registry.set('main_api_gateway_jwt_autorizer', authorizer)

    pulumi.export('Main API Gateway URL', api.api_endpoint)
    return api
