
# one by one
aws dynamodb scan --table-name access_tokens | \
  jq -c '.Items[] | { access_token }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name access_tokens --key

aws dynamodb scan --table-name groups | \
  jq -c '.Items[] | { id }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name groups --key

aws dynamodb scan --table-name invited_users | \
  jq -c '.Items[] | { email, auth_type }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name invited_users --key

aws dynamodb scan --table-name permissions | \
  jq -c '.Items[] | { id }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name permissions --key

aws dynamodb scan --table-name aws_accounts | \
  jq -c '.Items[] | { id }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name aws_accounts --key

aws dynamodb scan --table-name user_group_rels | \
  jq -c '.Items[] | { user_id, group_id }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name user_group_rels --key

aws dynamodb scan --table-name users | \
  jq -c '.Items[] | { id }' | \
  tr '\n' '\0' | \
  xargs -0 -n1 -t aws dynamodb delete-item --table-name users --key


# 25 items at a time
#aws dynamodb scan --table-name access_tokens | \
#  jq -c '[.Items | keys[] as $i | { index: $i, value: .[$i]}] | group_by(.index / 25 | floor)[] | { "access_tokens": [.[].value | { "DeleteRequest": { "Key": { access_token }}}] }' | \
#  tr '\n' '\0' | \
#  xargs -0 -n1 -t aws dynamodb batch-write-item --request-items
