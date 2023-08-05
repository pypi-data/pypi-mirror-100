import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudcomponents.cdk-codepipeline-slack",
    "version": "1.31.0",
    "description": "Cdk component that provisions a #slack approval workflow and notification messages on codepipeline state changes",
    "license": "MIT",
    "url": "https://github.com/cloudcomponents/cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cloudcomponents/cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudcomponents.cdk_codepipeline_slack",
        "cloudcomponents.cdk_codepipeline_slack._jsii"
    ],
    "package_data": {
        "cloudcomponents.cdk_codepipeline_slack._jsii": [
            "cdk-codepipeline-slack@1.31.0.jsii.tgz"
        ],
        "cloudcomponents.cdk_codepipeline_slack": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway>=1.95.1, <2.0.0",
        "aws-cdk.aws-codebuild>=1.95.1, <2.0.0",
        "aws-cdk.aws-codepipeline-actions>=1.95.1, <2.0.0",
        "aws-cdk.aws-codepipeline>=1.95.1, <2.0.0",
        "aws-cdk.aws-events-targets>=1.95.1, <2.0.0",
        "aws-cdk.aws-events>=1.95.1, <2.0.0",
        "aws-cdk.aws-iam>=1.95.1, <2.0.0",
        "aws-cdk.aws-lambda>=1.95.1, <2.0.0",
        "aws-cdk.aws-s3>=1.95.1, <2.0.0",
        "aws-cdk.aws-sns-subscriptions>=1.95.1, <2.0.0",
        "aws-cdk.aws-sns>=1.95.1, <2.0.0",
        "aws-cdk.core>=1.95.1, <2.0.0",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.26.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
