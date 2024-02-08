import pulumi_aws as aws
import pulumi
from src.library.common.registry import registry


def create(
        cert_config,
        dns_zone,
        region_name=aws.get_region().name,
        create_records=True
):
    opts = pulumi.ResourceOptions(
        provider=aws.Provider(region_name, region=region_name)
    )
    cert = aws.acm.Certificate(
        '{}-{}'.format(cert_config['name'], region_name),
        domain_name=cert_config['domain'],
        validation_method="DNS",
        subject_alternative_names=cert_config['alternative_names'],
        opts=opts
    )

    if create_records:
        dns_record = aws.route53.Record(
            "{}-cert-dns-record-{}".format(cert_config['name'], region_name),
            name=cert.domain_validation_options[0].resource_record_name,
            records=[
                cert.domain_validation_options[0].resource_record_value
            ],
            ttl=600,
            type=cert.domain_validation_options[0].resource_record_type,
            zone_id=dns_zone.zone_id,
            opts=opts
        )

        certificate_validation = aws.acm.CertificateValidation(
            "{}-cert-validation-{}".format(cert_config['name'], region_name),
            certificate_arn=cert.arn,
            validation_record_fqdns=[dns_record.fqdn],
            opts=opts
        )

        registry.set('main_ssl_cert_dns_record', dns_record)
        registry.set('main_ssl_cert_validation', certificate_validation)

    return cert
