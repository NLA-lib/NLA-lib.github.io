#!/usr/bin/env bash
# Run from AWS CloudShell in the existing account. Never prompts for ORCID secret values.
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c auth.zip.sha256
NLA_REGION=us-west-2
NLA_ACCOUNT=432197736886
NLA_STACK=nla-lib-auth
NLA_SECRET_ARN=arn:aws:secretsmanager:us-west-2:432197736886:secret:nla-lib/production/orcid-6onHMy
NLA_CERTIFICATE_ARN=arn:aws:acm:us-west-2:432197736886:certificate/c8b7502a-c630-4a73-a0b1-199a5332a548
NLA_BUCKET="nla-lib-auth-artifacts-${NLA_ACCOUNT}-${NLA_REGION}"
NLA_CALLER_ACCOUNT=$(aws sts get-caller-identity --query Account --output text --region "$NLA_REGION")
if [[ "$NLA_CALLER_ACCOUNT" != "$NLA_ACCOUNT" ]]; then
  echo 'Wrong AWS account. Switch to the account containing the ORCID secret and certificate.' >&2
  exit 1
fi
aws secretsmanager describe-secret --secret-id "$NLA_SECRET_ARN" --region "$NLA_REGION" --query ARN --output text
NLA_CERT_STATUS=$(aws acm describe-certificate --certificate-arn "$NLA_CERTIFICATE_ARN" --region "$NLA_REGION" --query Certificate.Status --output text)
NLA_CERT_DOMAIN=$(aws acm describe-certificate --certificate-arn "$NLA_CERTIFICATE_ARN" --region "$NLA_REGION" --query Certificate.DomainName --output text)
if [[ "$NLA_CERT_STATUS" != ISSUED || "$NLA_CERT_DOMAIN" != api.nla-lib.org ]]; then
  echo 'The certificate must be Issued for api.nla-lib.org before deployment.' >&2
  exit 1
fi
if aws s3api head-bucket --bucket "$NLA_BUCKET" --expected-bucket-owner "$NLA_ACCOUNT" --region "$NLA_REGION" 2>/dev/null; then
  NLA_PROJECT=$(aws s3api get-bucket-tagging --bucket "$NLA_BUCKET" --expected-bucket-owner "$NLA_ACCOUNT" --region "$NLA_REGION" --query 'TagSet[?Key==`project`].Value | [0]' --output text)
  if [[ "$NLA_PROJECT" != nla-lib-auth ]]; then
    echo 'The artifact bucket already exists without the expected project tag. Stop and check ownership.' >&2
    exit 1
  fi
else
  aws s3api create-bucket --bucket "$NLA_BUCKET" --region "$NLA_REGION" --create-bucket-configuration LocationConstraint="$NLA_REGION"
  aws s3api put-bucket-tagging --bucket "$NLA_BUCKET" --region "$NLA_REGION" --tagging 'TagSet=[{Key=project,Value=nla-lib-auth}]'
fi
aws s3api put-public-access-block --bucket "$NLA_BUCKET" --expected-bucket-owner "$NLA_ACCOUNT" --region "$NLA_REGION" --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket "$NLA_BUCKET" --expected-bucket-owner "$NLA_ACCOUNT" --region "$NLA_REGION" --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
NLA_DIGEST=$(sha256sum auth.zip | cut -d ' ' -f 1)
NLA_KEY="auth/${NLA_DIGEST}.zip"
aws s3 cp auth.zip "s3://${NLA_BUCKET}/${NLA_KEY}" --region "$NLA_REGION" --sse AES256 --only-show-errors
NLA_PARAMETERS=("ArtifactBucket=$NLA_BUCKET" "ArtifactKey=$NLA_KEY")
if [[ -z "${NLA_EXISTING_TABLE:-}" && -f .existing-data-table ]]; then
  NLA_EXISTING_TABLE=$(cat .existing-data-table)
fi
if [[ -n "${NLA_EXISTING_TABLE:-}" ]]; then
  if [[ ! "$NLA_EXISTING_TABLE" =~ ^[A-Za-z0-9_.-]{3,255}$ ]]; then
    echo 'Invalid existing data table name.' >&2
    exit 1
  fi
  NLA_PARAMETERS+=("ExistingDataTableName=$NLA_EXISTING_TABLE")
fi
if ! aws cloudformation deploy --template-file template.yaml --stack-name "$NLA_STACK" --region "$NLA_REGION" --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset --parameter-overrides "${NLA_PARAMETERS[@]}" --tags project=nla-lib-auth; then
  aws cloudformation describe-stack-events --stack-name "$NLA_STACK" --region "$NLA_REGION" --query "StackEvents[?ResourceStatus=='CREATE_FAILED' || ResourceStatus=='UPDATE_FAILED'].{Resource:LogicalResourceId,Reason:ResourceStatusReason}" --output table --no-cli-pager
  echo 'Deployment failed. Resolve the reported failure before retrying.' >&2
  exit 1
fi
aws cloudformation describe-stacks --stack-name "$NLA_STACK" --region "$NLA_REGION" --query 'Stacks[0].Outputs' --output table
