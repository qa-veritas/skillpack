#!/usr/bin/env bash
# Cheap, read-only proof that this skill's prerequisites work: the tools
# it relies on (df) are present and parseable. Exits 0 on success.
set -euo pipefail

if ! command -v df >/dev/null 2>&1; then
  echo "df not available" >&2
  exit 1
fi

# A real mount with a numeric use% confirms the data shape the skill parses.
df -P / | awk 'NR==2 { gsub("%","",$5); if ($5 ~ /^[0-9]+$/) { print "df parseable: / at " $5 "%"; exit 0 } else { exit 1 } }'
