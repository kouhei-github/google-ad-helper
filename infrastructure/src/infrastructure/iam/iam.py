from pulumi_aws import iam
import pulumi
import src.library.common.naming as naming


def create_role(config: dict, aws_service):
    return iam.Role(
        "%s%s" % (config['name'], config['sv_name']),
        assume_role_policy="""{
                "Version": "2012-10-17",
                "Statement": [
                    {
                    "Action": "sts:AssumeRole",
                    "Principal": {
                        "Service": "%s"
                    },
                    "Effect": "Allow",
                    "Sid": ""
                    }
                ]
                }
        
                """ % (aws_service),
    )


def attach_policy(name, arn_policy, arn_user):
    iam.RolePolicyAttachment(
        name,
        policy_arn=arn_policy,
        role=arn_user,
    )


def create_policy(name, json_policy):
    return iam.Policy(
        'policy' + name,
        name='policy' + name,
        path='/',
        policy=json_policy,
    )


def create_user(name: str, pgp_key: str):
    user = iam.User(
        name,
        path='/',
        tags={'Name': name},
    )
    user_access_key = iam.AccessKey(
        naming.get(name, 'key'),
        user=user.name,
        pgp_key=pgp_key
    )

    # pulumi.export(
    #    '{} secret'.format(name),
    #    user_access_key.encrypted_secret
    # )
