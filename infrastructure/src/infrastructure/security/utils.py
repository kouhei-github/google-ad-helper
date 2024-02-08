import pulumi_aws as aws

rule_alb_ingress = [{
    "protocol": "tcp",
    "from_port": 80,
    "to_port": 80,
    "cidr_blocks": ["0.0.0.0/0"],
},
    {
        "protocol": "tcp",
        "from_port": 443,
        "to_port": 443,
        "cidr_blocks": ["0.0.0.0/0"],
    },
    {
        "protocol": "tcp",
        "from_port": 22,
        "to_port": 22,
        "cidr_blocks": ["0.0.0.0/0"],
    }
]
rule_alb_egress = [
    {
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],

    }
]

alb_ingress = [
    aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"],
    ),
    aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=443,
        to_port=443,
        cidr_blocks=["0.0.0.0/0"],
    ),
    aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=22,
        to_port=22,
        cidr_blocks=["0.0.0.0/0"],
    ),
]

alb_egress = [
    aws.ec2.SecurityGroupEgressArgs(
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"],
    )
]

tasks_ingress = [
    aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"],
    ),
    aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=443,
        to_port=443,
        cidr_blocks=["0.0.0.0/0"],
    )
]

tasks_egress = [
    aws.ec2.SecurityGroupEgressArgs(
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"],
    )
]
