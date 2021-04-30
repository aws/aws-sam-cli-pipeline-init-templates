REGION=$1
ROLE=$2
SESSION_NAME=$3

unset AWS_SESSION_TOKEN
export AWS_DEFAULT_REGION=$REGION

export AWS_ACCESS_KEY_ID=$(echo $AWS_ACCESS_KEY_ID_)
export AWS_SECRET_ACCESS_KEY=$(echo $AWS_SECRET_ACCESS_KEY_)

cred=$(aws sts assume-role --role-arn "$ROLE" \
                           --role-session-name "$SESSION_NAME" \
                           --query '[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]' \
                           --output text)

export AWS_ACCESS_KEY_ID=$(echo $cred | awk '{ print $1 }')
export AWS_SECRET_ACCESS_KEY=$(echo $cred | awk '{ print $2 }')
export AWS_SESSION_TOKEN=$(echo $cred | awk '{ print $3 }')