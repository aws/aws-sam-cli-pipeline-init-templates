#!/bin/bash
ROLE=$1
SESSION_NAME=$2
PROFILE_NAME=$3
PERMISSIONS_PROVIDER=$4
TOKEN=$5

unset AWS_SESSION_TOKEN

if [ "$PERMISSIONS_PROVIDER" = "AWS IAM" ]
then
    aws configure --profile sam-pipeline-user set aws_access_key_id "$PIPELINE_USER_ACCESS_KEY_ID"
    aws configure --profile sam-pipeline-user set aws_secret_access_key "$PIPELINE_USER_SECRET_ACCESS_KEY"

    cred=$(aws sts assume-role --profile sam-pipeline-user \
                            --role-arn "$ROLE" \
                            --role-session-name "$SESSION_NAME" \
                            --query '[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]' \
                            --output text)
else
    # Use assume-role-with-web-identity instead of assume-role
    cred=$(aws sts assume-role-with-web-identity --role-arn "$ROLE" \
                            --role-session-name "$SESSION_NAME" \
                            --web-identity-token "$TOKEN" \
                            --query '[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]' \
                            --output text)
fi

ACCESS_KEY_ID=$(echo "$cred" | awk '{ print $1 }')
aws configure --profile "$PROFILE_NAME" set aws_access_key_id "$ACCESS_KEY_ID"

SECRET_ACCESS_KEY=$(echo "$cred" | awk '{ print $2 }')
aws configure --profile "$PROFILE_NAME" set aws_secret_access_key "$SECRET_ACCESS_KEY"

SESSION_TOKEN=$(echo "$cred" | awk '{ print $3 }')
aws configure --profile "$PROFILE_NAME" set aws_session_token "$SESSION_TOKEN"
