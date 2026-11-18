#!/bin/sh
# Prints the root of a local copy of the AI engineering brain, or exits 1 if there is none.
# Order: the folder named in $AIE_BRAIN, the repository this skill is linked from, then the
# current folder and its parents.
# A copied install of this skill is not inside the brain, so every candidate is checked.

is_brain() {
  [ -f "$1/index.md" ] && [ -f "$1/glossary.md" ] && [ -d "$1/concepts" ]
}

found() {
  (cd "$1" && pwd -P)
  exit 0
}

if [ -n "$AIE_BRAIN" ]; then
  if is_brain "$AIE_BRAIN"; then found "$AIE_BRAIN"; fi
  echo "brain-root: AIE_BRAIN is set to '$AIE_BRAIN', which is not the brain's root." >&2
fi

linked=$(cd "$(dirname "$0")" 2>/dev/null && cd "$(pwd -P)/../../.." 2>/dev/null && pwd -P)
if [ -n "$linked" ] && is_brain "$linked"; then found "$linked"; fi

dir=$(pwd -P)
while [ -n "$dir" ] && [ "$dir" != "/" ]; do
  if is_brain "$dir"; then found "$dir"; fi
  dir=$(dirname "$dir")
done

echo "brain-root: no local copy of the AI engineering brain found." >&2
echo "Clone it and set AIE_BRAIN to the clone:" >&2
echo "  git clone --depth 1 https://github.com/mishaevoma/ai-engineering-brain" >&2
exit 1
