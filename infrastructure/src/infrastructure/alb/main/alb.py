import pulumi_aws as aws
from pulumi_aws.lb.load_balancer import LoadBalancer
import src.library.common.naming as naming
import pulumi


def create(alb_config: dict, vpc, ssl_cert, dns_zone):
    security_group_name = '{}-alb-sg'.format(alb_config['name'])
    security_group = aws.ec2.SecurityGroup(
        security_group_name,
        vpc_id=vpc.vpc_id,
        description="Enable HTTP access",
        ingress=[
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
        ],
        egress=[aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )],
    )

    alb = aws.lb.LoadBalancer(
        alb_config['name'],
        security_groups=[security_group.id],
        subnets=vpc.public_subnet_ids,
    )

    http_listener_name = '{}-alb-http-listener'.format(alb_config['name'])
    aws.lb.Listener(
        http_listener_name,
        load_balancer_arn=alb.arn,
        port=80,
        default_actions=[aws.lb.ListenerDefaultActionArgs(
            type="redirect",
            redirect=aws.lb.ListenerDefaultActionRedirectArgs(
                port="443",
                protocol="HTTPS",
                status_code="HTTP_301",
            ),
        )]
    )

    https_listener_name = '{}-alb-https-listener'.format(alb_config['name'])
    https_listener = aws.lb.Listener(
        https_listener_name,
        load_balancer_arn=alb.arn,
        port=443,
        protocol="HTTPS",
        ssl_policy="ELBSecurityPolicy-2016-08",
        certificate_arn=ssl_cert.arn.apply(lambda ssl_cert_arn: ssl_cert_arn),
        default_actions=[aws.lb.ListenerDefaultActionArgs(
            type="fixed-response",
            fixed_response=aws.lb.ListenerDefaultActionFixedResponseArgs(
                content_type="text/plain",
                message_body="Welcome to GEEKSNIPE Gateway API",
                status_code="200",
            ),
        )],
        opts=pulumi.ResourceOptions(depends_on=[ssl_cert]))
    
    alb_domain = aws.route53.Record(
        naming.get('dev-domain-cname-record', alb_config['name']),
        name=f"dev.{alb_config['name']}",
        zone_id=dns_zone.zone_id,
        type="CNAME",
        records=[alb.dns_name],
        ttl=600)
    
    return alb, https_listener, alb_domain
