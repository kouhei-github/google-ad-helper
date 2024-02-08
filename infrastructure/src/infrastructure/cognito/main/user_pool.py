import pulumi
import pulumi_aws as aws
import src.library.common.naming as naming
from src.library.common.registry import registry


def create(
        user_pool_config,
        ssl_cert,
        dns_zone,
        alb
):
    pool = aws.cognito.UserPool(
        naming.get('cognito-user-pool', user_pool_config['name']),
        schemas=[
            aws.cognito.UserPoolSchemaArgs(
                attribute_data_type="String",
                name="userId",
                mutable=True,
                string_attribute_constraints=aws.cognito.UserPoolSchemaStringAttributeConstraintsArgs(
                    max_length="256",
                    min_length="1"
                )
            )
        ],
        opts=pulumi.ResourceOptions(ignore_changes=["schemas"])
    )

    dns_record = aws.route53.Record(
        naming.get('cognito-user-pool-dns-record', user_pool_config['name']),
        name=user_pool_config['domain']['dns_record'],
        zone_id=dns_zone.zone_id,
        type="CNAME",
        records=[alb.dns_name],
        ttl=600)
    
    user_pool_domain = aws.cognito.UserPoolDomain(
        naming.get('cognito-user-pool-domain', user_pool_config['name']),
        domain=dns_record.fqdn,
        certificate_arn=ssl_cert.arn.apply(lambda ssl_cert_arn: ssl_cert_arn),
        user_pool_id=pool.id,
        opts=pulumi.ResourceOptions(
            depends_on=[
                ssl_cert,
                registry.get('main_ssl_cert_dns_record'),
                registry.get('main_ssl_cert_validation')
            ],
            custom_timeouts=pulumi.CustomTimeouts(create='5m')
        )
    )

    geeksnipe_resource_server = aws.cognito.ResourceServer(
        naming.get('cognito-user-pool-resource-server', user_pool_config['name']),
        identifier="geeksnipe",
        scopes=[
            aws.cognito.ResourceServerScopeArgs(
                scope_name="write",
                scope_description="Create/Update geeksnipe resources",
            ),
            aws.cognito.ResourceServerScopeArgs(
                scope_name="read",
                scope_description="Read Geeksnipe resources",
            ),
        ],
        user_pool_id=pool.id,
        opts=pulumi.ResourceOptions(delete_before_replace=True)
    )

    default_client = aws.cognito.UserPoolClient(
        naming.get('cognito-user-pool-client', user_pool_config['name']),
        user_pool_id=pool.id,
        callback_urls=user_pool_config['callback_urls'],
        allowed_oauth_flows_user_pool_client=True,
        generate_secret=True,
        allowed_oauth_flows=[
            "client_credentials"
        ],
        allowed_oauth_scopes=[
            'geeksnipe/write',
            'geeksnipe/read',
        ],
        supported_identity_providers=["COGNITO"],
        opts=pulumi.ResourceOptions(depends_on=[
            geeksnipe_resource_server,
        ])
    )

    pulumi.export("cognito_dns_record_name", dns_record.fqdn)
    registry.set('main_cognito_user_pool_default_client', default_client)

    return pool, default_client
