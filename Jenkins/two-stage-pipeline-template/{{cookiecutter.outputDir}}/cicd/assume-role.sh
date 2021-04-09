#!/bin/sh

REGION=$1
ROLE=$2
SESSION_NAME=$3

# Reset to the Deployer IAM user before assuming the role to avoid assuming a role from another role
# shellcheck disable=SC2154
export AWS_ACCESS_KEY_ID=$aws_access_key_id_
# shellcheck disable=SC2154
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key_
unset AWS_SESSION_TOKEN
export AWS_DEFAULT_REGION=$REGION

# Now assume the role
assumed_cred=$(aws sts assume-role \
           --role-arn "$ROLE" \
           --role-session-name "$SESSION_NAME" \
           --query '[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]' \
           --output text)

assumed_aws_access_key_id=$(echo "$assumed_cred" | awk '{ print $1 }')
assumed_aws_secret_access_key=$(echo "$assumed_cred" | awk '{ print $2 }')
assumed_aws_session_token=$(echo "$assumed_cred" | awk '{ print $3 }')

export AWS_ACCESS_KEY_ID=$assumed_aws_access_key_id
export AWS_SECRET_ACCESS_KEY=$assumed_aws_secret_access_key
export AWS_SESSION_TOKEN=$assumed_aws_session_token
