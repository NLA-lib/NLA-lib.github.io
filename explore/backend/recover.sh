#!/usr/bin/env bash
# Recovery for the specific failed first deployment. Never deletes DynamoDB data.
set -euo pipefail
cd "$(dirname "$0")"
NLA_REGION=us-west-2
NLA_ACCOUNT=432197736886
NLA_FAILED_STACK=arn:aws:cloudformation:us-west-2:432197736886:stack/nla-lib-auth/15592920-e8b7-11f1-aff0-0affcd16f033
NLA_RETAINED_TABLE=nla-lib-auth-Data-TFOFBP4JELM9
sha256sum -c auth.zip.sha256
NLA_CALLER=$(aws sts get-caller-identity --region "$NLA_REGION" --query Account --output text)
if [[ "$NLA_CALLER" != "$NLA_ACCOUNT" ]]; then
  echo 'Wrong AWS account; no changes made.' >&2
  exit 1
fi
NLA_SCHEMA=$(aws dynamodb describe-table --table-name "$NLA_RETAINED_TABLE" --region "$NLA_REGION" --query 'Table.[TableStatus,KeySchema,AttributeDefinitions]' --output json)
printf '%s' "$NLA_SCHEMA" | python3 -c 'import json,sys;status,keys,attributes=json.load(sys.stdin);assert status=="ACTIVE", "Retained table is not active";assert {x["AttributeName"]:x["KeyType"] for x in keys}=={"pk":"HASH","sk":"RANGE"}, "Unexpected key schema";assert {x["AttributeName"]:x["AttributeType"] for x in attributes}=={"pk":"S","sk":"S"}, "Unexpected key types"'
NLA_STATUS=$(aws cloudformation describe-stacks --stack-name "$NLA_FAILED_STACK" --region "$NLA_REGION" --query 'Stacks[0].StackStatus' --output text)
if [[ "$NLA_STATUS" == ROLLBACK_COMPLETE ]]; then
  NLA_STACK_TABLE=$(aws cloudformation describe-stack-resource --stack-name "$NLA_FAILED_STACK" --logical-resource-id Data --region "$NLA_REGION" --query 'StackResourceDetail.[PhysicalResourceId,ResourceStatus]' --output text)
  read -r NLA_ACTUAL_TABLE NLA_TABLE_STATUS <<< "$NLA_STACK_TABLE"
  if [[ "$NLA_ACTUAL_TABLE" != "$NLA_RETAINED_TABLE" || "$NLA_TABLE_STATUS" != DELETE_SKIPPED ]]; then
    echo 'The failed stack does not match the expected retained-table state. Stop for review.' >&2
    exit 1
  fi
  printf '%s\n' "$NLA_RETAINED_TABLE" > .existing-data-table
  echo 'Removing the failed stack record; keeping its retained DynamoDB table.'
  aws cloudformation delete-stack --stack-name "$NLA_FAILED_STACK" --region "$NLA_REGION"
  aws cloudformation wait stack-delete-complete --stack-name "$NLA_FAILED_STACK" --region "$NLA_REGION"
elif [[ "$NLA_STATUS" == DELETE_COMPLETE ]]; then
  printf '%s\n' "$NLA_RETAINED_TABLE" > .existing-data-table
else
  echo "The original stack is $NLA_STATUS, not the expected failed/deleted state. No stack deleted." >&2
  exit 1
fi
NLA_EXISTING_TABLE="$NLA_RETAINED_TABLE" bash ./deploy.sh
