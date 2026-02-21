#!/usr/bin/env bash
set -euo pipefail

FILE_PATH=$(cat | jq -r '.tool_input.file_path // empty')

# Only check .fairmind/ paths
if [[ "$FILE_PATH" != *".fairmind/"* ]]; then
  exit 0
fi

# Allow root-level active-context.json
if [[ "$FILE_PATH" =~ \.fairmind/active-context\.json$ ]]; then
  exit 0
fi

# Check for scoped path: .fairmind/<slug>/<slug>/...
if [[ "$FILE_PATH" =~ \.fairmind/[^/]+/[^/]+/ ]]; then
  exit 0
fi

# Block flat paths
echo "Flat .fairmind/ path not allowed. Read .fairmind/active-context.json for FAIRMIND_BASE and use scoped path." >&2
exit 2
