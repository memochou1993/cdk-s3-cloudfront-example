import os

import aws_cdk

from deployment.cdk_s3_cloudfront_example_stack import CdkS3CloudfrontExampleStack

app = aws_cdk.App()

env = aws_cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION"),
)

CdkS3CloudfrontExampleStack(app, "CdkS3CloudfrontExampleStack", env=env)

app.synth()
