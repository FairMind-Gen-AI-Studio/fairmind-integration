#!/usr/bin/env bash
set -euo pipefail

CONTEXT_FILE="$CWD/.fairmind/active-context.json"

# No active context → nothing to enforce
if [ ! -f "$CONTEXT_FILE" ]; then
  exit 0
fi

# Only enforce for key agents
AGENT="${CLAUDE_AGENT_NAME:-}"
case "$AGENT" in
  software-engineer|qa-engineer|code-reviewer|cybersec-engineer) ;;
  *) exit 0 ;;
esac

BASE_PATH=$(jq -r '.base_path' "$CONTEXT_FILE")

# Check for recently modified journals (last 30 min)
RECENT=$(find "$CWD/$BASE_PATH/journals" -name "*_journal.md" -mmin -30 2>/dev/null | head -1)
if [ -n "$RECENT" ]; then
  exit 0
fi

# Check if code was actually written (non-.fairmind changes)
CODE_CHANGES=$(git -C "$CWD" diff --name-only HEAD 2>/dev/null | grep -v "^\.fairmind/" | head -1)
if [ -z "$CODE_CHANGES" ]; then
  exit 0
fi

echo "Journal missing. You modified code but did not create a journal. Write your journal at $BASE_PATH/journals/{task_id}_${AGENT}_journal.md before completing." >&2
exit 2
