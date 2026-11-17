#!/bin/sh
# Prints the root of the AI engineering brain.
# Order: the folder named in $AIE_BRAIN, then the folder this skill was installed from.
# The second works when this skill folder is reached through a symlink (for example from
# ~/.claude/skills), and fails when the folder was copied: set AIE_BRAIN in that case.

is_brain() {
  [ -f "$1/index.md" ] && [ -f "$1/glossary.md" ] && [ -d "$1/concepts" ]
}

if [ -n "$AIE_BRAIN" ]; then
  if is_brain "$AIE_BRAIN"; then
    cd "$AIE_BRAIN" && pwd -P
    exit 0
  fi
  echo "brain-root: AIE_BRAIN is set to '$AIE_BRAIN', which is not the brain's root." >&2
fi

root=$(cd "$(dirname "$0")" && cd "$(pwd -P)/../../.." && pwd -P)
if is_brain "$root"; then
  echo "$root"
  exit 0
fi

echo "brain-root: no brain found at '$root'." >&2
echo "Clone it and set AIE_BRAIN to the clone:" >&2
echo "  git clone --depth 1 https://github.com/mishaevoma/ai-engineering-brain" >&2
exit 1
