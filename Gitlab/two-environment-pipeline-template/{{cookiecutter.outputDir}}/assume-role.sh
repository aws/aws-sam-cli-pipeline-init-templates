#!/bin/bash
ROLE=$1
SESSION_NAME=$2

unset AWS_SESSION_TOKEN
export AWS_ACCESS_KEY_ID=$PIPELINE_USER_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$PIPELINE_USER_SECRET_ACCESS_KEY

cred=$(aws sts assume-role --role-arn "$ROLE" \
                           --role-session-name "$SESSION_NAME" \
                           --query '[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]' \
                           --output text)

ACCESS_KEY_ID=$(echo "$cred" | awk '{ print $1 }')
export AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID

SECRET_ACCESS_KEY=$(echo "$cred" | awk '{ print $2 }')
export AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY

SESSION_TOKEN=$(echo "$cred" | awk '{ print $3 }')
export AWS_SESSION_TOKEN=$SESSION_TOKEN
