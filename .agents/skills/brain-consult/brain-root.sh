#!/bin/sh
# Prints the root of a local copy of the AI engineering brain, or exits 1 if there is none.
# Looks in: the repository this skill is linked from, the current folder and its parents,
# and the path in the AI_ENGINEERING_BRAIN environment variable.
# A copied install of this skill is not inside the brain, so every candidate is checked.

is_brain() {
  [ -f "$1/index.md" ] && [ -f "$1/glossary.md" ] && [ -d "$1/concepts" ]
}

found() {
  (cd "$1" && pwd -P)
  exit 0
}

linked=$(cd "$(dirname "$0")" 2>/dev/null && cd "$(pwd -P)/../../.." 2>/dev/null && pwd -P)
if [ -n "$linked" ] && is_brain "$linked"; then found "$linked"; fi

dir=$(pwd -P)
while [ -n "$dir" ] && [ "$dir" != "/" ]; do
  if is_brain "$dir"; then found "$dir"; fi
  dir=$(dirname "$dir")
done

if [ -n "$AI_ENGINEERING_BRAIN" ] && is_brain "$AI_ENGINEERING_BRAIN"; then found "$AI_ENGINEERING_BRAIN"; fi

echo "No local copy of the AI engineering brain found." >&2
echo "Set AI_ENGINEERING_BRAIN to the path of a clone, or read the public copy:" >&2
echo "https://github.com/mishaevoma/ai-engineering-brain" >&2
exit 1
