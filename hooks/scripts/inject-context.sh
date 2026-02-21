#!/usr/bin/env bash
set -eo pipefail

CWD="${CWD:-$PWD}"
CONTEXT_FILE="$CWD/.fairmind/active-context.json"

# No context file → silent exit (Atlas hasn't run yet, or not a FairMind project)
[ -f "$CONTEXT_FILE" ] || exit 0

jq -r '"FairMind active context: FAIRMIND_BASE=\(.base_path), project_id=\(.project_id), session_mindstreamId=\(.session_mindstreamId)"' "$CONTEXT_FILE"
