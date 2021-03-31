import boto3


def get_context(provider):
    return {"provider": provider, "aws_profiles": boto3.session.Session().available_profiles}