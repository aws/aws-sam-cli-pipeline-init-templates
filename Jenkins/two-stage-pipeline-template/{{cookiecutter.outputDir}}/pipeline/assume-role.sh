#!/bin/sh

ROLE=$1
SESSION_NAME=$2

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
