import pulumi_aws as aws
import pulumi_awsx as awsx
from pulumi_aws.ec2.vpc import Vpc


def create(vpc_config: dict) -> Vpc:

    vpc = awsx.ec2.Vpc(
        vpc_config['name'],
        cidr_block=vpc_config['cidr'],
        subnet_specs=[
            awsx.ec2.SubnetSpecArgs(
                type=awsx.ec2.SubnetType.PUBLIC,
                cidr_mask=21,
                name='public-subnet',
            )
        ],
        nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(
            strategy="NONE"
        ),
        instance_tenancy='default',
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags={
            'Name': vpc_config['name'],
            'Author': 'Pulumi'
        },
    )

    return vpc
