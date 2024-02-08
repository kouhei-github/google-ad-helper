import pulumi_aws as aws
from pulumi import Output
from pulumi_aws.ec2.security_group import SecurityGroup


def create(
        sg_config: dict,
        vpc_id: Output[str],
        rule_ingress: list,
        rule_egress: list
) -> SecurityGroup:
    return aws.ec2.SecurityGroup(
        "sg_{}".format(sg_config['name']),
        description="Allow TLS inbound traffic",
        vpc_id=vpc_id,
        ingress=rule_ingress,
        egress=rule_egress,
        tags={
            'Name': "sg_{}".format(sg_config['name']),
        },
        revoke_rules_on_delete=False
    )
