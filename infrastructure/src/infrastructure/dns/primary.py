import pulumi
import pulumi_aws as aws
import src.library.common.naming as naming


def create(dns_config, alb):
    # primary = aws.route53.Zone(
    #     dns_config['name'],
    #     name=dns_config['name']
    # )

    primary = aws.route53.get_zone(name=dns_config['name'])
    record = aws.route53.Record(
        'dns-record',
        zone_id=primary.zone_id,
        name=dns_config['name'],
        type="A",
        aliases=[
        aws.route53.RecordAliasArgs(
            name=alb.dns_name,
            zone_id=alb.zone_id,
            evaluate_target_health=True,
        )
    ])

    return primary, record


