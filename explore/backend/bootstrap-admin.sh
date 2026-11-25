#!/usr/bin/env bash
# One-time role assignment by an administrator already authenticated to AWS.
set -euo pipefail
NLA_REGION=us-west-2
NLA_ACCOUNT=$(aws sts get-caller-identity --query Account --output text --region "$NLA_REGION")
if [[ "$NLA_ACCOUNT" != 432197736886 ]]; then echo 'Switch to the AWS account containing NLA-lib.' >&2; exit 1; fi
NLA_ORCID=${1:-}
if [[ -z "$NLA_ORCID" ]]; then read -r -p 'Your ORCID iD (0000-0000-0000-0000): ' NLA_ORCID; fi
if [[ ! "$NLA_ORCID" =~ ^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$ ]]; then echo 'Enter the ORCID iD from your signed-in NLA-lib profile.' >&2; exit 1; fi
NLA_PERSON_ID=$(python3 - "$NLA_ORCID" <<'PY'
import sys,uuid
print(uuid.uuid5(uuid.NAMESPACE_URL,'https://orcid.org/'+sys.argv[1]))
PY
)
NLA_TABLE=$(aws cloudformation describe-stacks --stack-name nla-lib-auth --region "$NLA_REGION" --query 'Stacks[0].Outputs[?OutputKey==`TableName`].OutputValue | [0]' --output text)
NLA_KEY=$(python3 - "$NLA_PERSON_ID" <<'PY'
import sys,json
print(json.dumps({'pk':{'S':'PERSON#'+sys.argv[1]},'sk':{'S':'PROFILE'}}))
PY
)
NLA_VALUES=$(python3 - "$NLA_ORCID" <<'PY'
import sys,json
print(json.dumps({':orcid':{'S':sys.argv[1]},':active':{'S':'active'},':role':{'S':'admin'}}))
PY
)
# Does not create an account or accept a typed ORCID in lieu of authentication.
aws dynamodb update-item --table-name "$NLA_TABLE" --key "$NLA_KEY" --region "$NLA_REGION" \
 --update-expression 'SET #role=:role' --condition-expression 'orcid=:orcid AND #status=:active' \
 --expression-attribute-names '{"#role":"role","#status":"status"}' --expression-attribute-values "$NLA_VALUES" \
 --return-values NONE
NLA_AUDIT=$(python3 - "$NLA_PERSON_ID" <<'PY'
import sys,json,uuid,time
now=int(time.time());pid=sys.argv[1]
print(json.dumps({'pk':{'S':'PERSON#'+pid},'sk':{'S':'AUDIT#'+str(now)+'#'+str(uuid.uuid4())},'actor_id':{'S':'aws-account-administrator'},'action':{'S':'admin_role_bootstrapped'},'created_at':{'N':str(now)}}))
PY
)
aws dynamodb put-item --table-name "$NLA_TABLE" --item "$NLA_AUDIT" --region "$NLA_REGION"
echo 'Your authenticated account is now an admin. Reload the Explorer to see editorial review tools.'
