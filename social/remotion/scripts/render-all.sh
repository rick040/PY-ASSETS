#!/usr/bin/env bash
# Renders every item (reel + feed + cover) with motion blur. Usage: scripts/render-all.sh [browser-executable]
set -euo pipefail
cd "$(dirname "$0")/.."
B=${1:+--browser-executable=$1}
node scripts/sync-assets.mjs
for i in ig-002 ig-017 ig-018 ig-021 ig-028 ig-064; do
  echo "== $i $(date +%T)"
  npm run -s render:$i -- $B --log=error --concurrency=4
  npm run -s render:$i:feed -- $B --log=error --concurrency=4
  npm run -s still:$i -- $B --log=error
done
echo "== done $(date +%T)"
