#!/bin/bash
REGION=$1
ROLE=$2
SESSION_NAME=$3

unset AWS_SESSION_TOKEN
export AWS_DEFAULT_REGION=$REGION
export AWS_ACCESS_KEY_ID=$PIPELINE_USER_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$PIPELINE_USER_SECRET_ACCESS_KEY

cred=$(aws sts assume-role --role-arn "$ROLE" \
                           --role-session-name "$SESSION_NAME" \
                           --query '[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]' \
                           --output text)

AccessKeyId=$(echo "$cred" | awk '{ print $1 }')
export AWS_ACCESS_KEY_ID=$AccessKeyId

SecretAccessKey=$(echo "$cred" | awk '{ print $2 }')
export AWS_SECRET_ACCESS_KEY=$SecretAccessKey

SessionToken=$(echo "$cred" | awk '{ print $3 }')
export AWS_SESSION_TOKEN=$SessionToken