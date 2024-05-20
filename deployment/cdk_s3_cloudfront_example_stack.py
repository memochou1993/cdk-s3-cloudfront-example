import json

from aws_cdk import RemovalPolicy, Stack, aws_cloudfront, aws_cloudfront_origins, aws_s3, aws_ssm
from constructs import Construct


class CdkS3CloudfrontExampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.s3_bucket = self.create_s3_bucket()
        self.cloudfront_distribution = self.create_cloudfront_distribution()

    def create_s3_bucket(self):
        s3_bucket = aws_s3.Bucket(
            self,
            "Bucket",
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            access_control=aws_s3.BucketAccessControl.PRIVATE,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        return s3_bucket

    def create_cloudfront_distribution(self):
        cloudfront_distribution = aws_cloudfront.Distribution(
            self,
            "CloudFrontDistribution",
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3Origin(self.s3_bucket),
                compress=True,
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
        )

        return cloudfront_distribution

    def create_ssm_string_param(self):
        ssm_name = '/output/s3-cloudfront-stack'

        ssm_string_param = aws_ssm.StringParameter(
            self,
            'SsmStringParam',
            parameter_name=ssm_name,
            string_value=json.dumps(
                {
                    's3_bucket_name': self.s3_bucket.bucket_name,
                    'cloudfront_distribution_id': self.cloudfront_distribution.distribution_id,
                }
            ),
            tier=aws_ssm.ParameterTier.STANDARD,
        )

        ssm_string_param.apply_removal_policy(RemovalPolicy.DESTROY)

        return ssm_string_param
