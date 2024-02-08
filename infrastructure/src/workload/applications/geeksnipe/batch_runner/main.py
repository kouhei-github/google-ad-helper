import json
import pulumi_aws as aws
import pulumi
import src.library.common.naming as naming


def ecs_task_attach_policies(
        task_role,
        application_config):
    # Create S3 bucket
    bucket = aws.s3.BucketV2(
        "{}-s3-bucket".format(application_config['name']),
        bucket=application_config['s3']['bucket_name']
    )

    bucket_ownership_controls = aws.s3.BucketOwnershipControls(
        naming.get('bucket-ownership-controls', application_config['name']),
        bucket=bucket.id,
        rule=aws.s3.BucketOwnershipControlsRuleArgs(
            object_ownership="ObjectWriter",
        ))

    bucket_public_access_block = aws.s3.BucketPublicAccessBlock(
        naming.get('bucket-public-access-block', application_config['name']),
        bucket=bucket.id,
        block_public_acls=False,
        block_public_policy=False,
        ignore_public_acls=False,
        restrict_public_buckets=False)

    bucket_acl_v2 = aws.s3.BucketAclV2(
        naming.get('bucket-acl-v2', application_config['name']),
        bucket=bucket.id,
        acl="public-read",
        opts=pulumi.ResourceOptions(depends_on=[
            bucket_ownership_controls,
            bucket_public_access_block,
        ]))

    s3_bucket_policy_document = aws.iam.get_policy_document(
        statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=[
                "s3:*"
            ],
            resources=[
                bucket.arn.apply(lambda bucket_arn: f"{bucket_arn}"),
                bucket.arn.apply(lambda bucket_arn: f"{bucket_arn}/*")
            ]
        )])

    s3_bucket_policy = aws.iam.Policy(
        "{}-s3-bucket-policy".format(application_config['name']),
        description="Policy for managing kyc documents",
        policy=s3_bucket_policy_document.json)

    aws.iam.RolePolicyAttachment(
        "{}-s3-bucket-policy-attachment".format(application_config['name']),
        role=task_role.name,
        policy_arn=s3_bucket_policy.arn)
