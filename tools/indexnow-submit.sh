#!/bin/zsh
# IndexNow submitter for aglaconsulting.com
#
# Tells Bing (and other IndexNow search engines, e.g. Yandex, Seznam, Naver) that
# pages changed, so they re-crawl within hours instead of waiting for the next crawl.
#
# Usage (run from the repo root AFTER pushing to main and GitHub Pages has deployed):
#   ./tools/indexnow-submit.sh                 # submit every URL in sitemap.xml
#   ./tools/indexnow-submit.sh https://aglaconsulting.com/some-page   # submit specific URLs
#
# The key is public by design: search engines verify it by fetching the key file
# hosted at the site root (https://aglaconsulting.com/<key>.txt).

set -euo pipefail

HOST="aglaconsulting.com"
KEY="d4a90fd57ed99b42091ec16b814ca5cb"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
ENDPOINT="https://api.indexnow.org/indexnow"
SCRIPT_DIR="${0:A:h}"
SITEMAP="${SCRIPT_DIR}/../sitemap.xml"

# 1. URLs to submit: command-line arguments, or every <loc> in sitemap.xml
if (( $# > 0 )); then
  urls=("$@")
else
  urls=(${(f)"$(grep -o '<loc>[^<]*</loc>' "$SITEMAP" | sed -e 's#<loc>##' -e 's#</loc>##')"})
fi
if (( ${#urls} == 0 )); then
  echo "No URLs found to submit." >&2
  exit 1
fi

# 2. Make sure the live key file is reachable and correct, or the submission is rejected
live_key="$(curl -fsS "$KEY_LOCATION" || true)"
if [[ "$live_key" != "$KEY" ]]; then
  echo "Key file not live yet at $KEY_LOCATION (has GitHub Pages finished deploying?)." >&2
  exit 1
fi

# 3. Build the JSON payload safely and submit
payload="$(python3 -c '
import json, sys
host, key, loc = sys.argv[1:4]
print(json.dumps({"host": host, "key": key, "keyLocation": loc, "urlList": sys.argv[4:]}))
' "$HOST" "$KEY" "$KEY_LOCATION" "${urls[@]}")"

echo "Submitting ${#urls} URL(s) to IndexNow:"
printf '  %s\n' "${urls[@]}"

status="$(curl -sS -o /tmp/indexnow-response.txt -w '%{http_code}' \
  -X POST "$ENDPOINT" \
  -H 'Content-Type: application/json; charset=utf-8' \
  --data "$payload")"

case "$status" in
  200|202) echo "Accepted (HTTP $status). Bing should re-crawl shortly." ;;
  400) echo "HTTP 400: bad request (check URL format)." >&2 ;;
  403) echo "HTTP 403: key not valid (key file missing or mismatched)." >&2 ;;
  422) echo "HTTP 422: URLs don't belong to $HOST or key doesn't match." >&2 ;;
  429) echo "HTTP 429: too many requests, try again later." >&2 ;;
  *)   echo "Unexpected HTTP $status:" >&2; cat /tmp/indexnow-response.txt >&2 ;;
esac
rm -f /tmp/indexnow-response.txt
[[ "$status" == 200 || "$status" == 202 ]]
