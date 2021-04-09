REGION=$1
ROLE=$2
SESSION_NAME=$3
# Reset to the Deployer IAM user before assuming the role to avoid assuming a role from another role
export AWS_ACCESS_KEY_ID=$aws_access_key_id_
export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key_
unset AWS_SESSION_TOKEN
export AWS_DEFAULT_REGION=$REGION
# Now assume the role
cred=$(aws sts assume-role \
           --role-arn $ROLE \
           --role-session-name $SESSION_NAME)
export AWS_ACCESS_KEY_ID=$(echo "${cred}" | jq ".Credentials.AccessKeyId" --raw-output)
export AWS_SECRET_ACCESS_KEY=$(echo "${cred}" | jq ".Credentials.SecretAccessKey" --raw-output)
export AWS_SESSION_TOKEN=$(echo "${cred}" | jq ".Credentials.SessionToken" --raw-output)