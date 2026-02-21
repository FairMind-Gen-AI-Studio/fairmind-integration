#!/usr/bin/env bash
set -euo pipefail

CONTEXT_FILE="$CWD/.fairmind/active-context.json"

if [ -f "$CONTEXT_FILE" ]; then
  jq -r '"FairMind active context: FAIRMIND_BASE=\(.base_path), project_id=\(.project_id), session_mindstreamId=\(.session_mindstreamId)"' "$CONTEXT_FILE"
else
  echo "No .fairmind/active-context.json found. If working with FairMind, engage Atlas (tech-lead) to bootstrap."
fi
