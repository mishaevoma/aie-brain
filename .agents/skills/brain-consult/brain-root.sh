#!/bin/sh
# Prints the root of a local copy of the AI engineering brain. When this machine has none, as
# on the first run of a copied install of this skill, it clones one and prints that.
#
# Where it looks, in order:
#   1. $AIE_BRAIN, when set. If nothing is there yet, the clone goes there.
#   2. The repository this skill sits in or is linked from.
#   3. The current folder and its parents.
#   4. ~/.aie-brain, where the clone goes when AIE_BRAIN is not set.
#
# The copy in ~/.aie-brain, and any copy this script cloned, is brought up to date at most
# once a day. A clone you keep anywhere else is never touched. AIE_BRAIN_REPO names another
# address to clone from, for a fork or a mirror.
#
# Prints the path on stdout and exits 0. Exits 1, with the reason on stderr, when there is no
# copy and none could be cloned.

REPO=${AIE_BRAIN_REPO:-https://github.com/mishaevoma/aie-brain}
STAMP=.git/aie-brain-checked

is_brain() {
  [ -f "$1/index.md" ] && [ -f "$1/glossary.md" ] && [ -d "$1/concepts" ] && [ -d "$1/sources" ]
}

say() {
  echo "brain-root: $*" >&2
}

# Bring the copy up to date, at most once a day, if this script cloned it (it left a stamp) or
# it is the one in ~/.aie-brain. It never fails: a copy that could not be updated still
# answers the question.
refresh() {
  [ -d "$1/.git" ] || return 0
  if [ ! -f "$1/$STAMP" ]; then
    [ -n "$HOME" ] && [ "$(cd "$1" && pwd -P)" = "$(cd "$HOME/.aie-brain" 2>/dev/null && pwd -P)" ] || return 0
  fi
  today=$(date +%Y-%m-%d)
  [ "$(cat "$1/$STAMP" 2>/dev/null)" = "$today" ] && return 0
  echo "$today" > "$1/$STAMP" 2>/dev/null
  git -C "$1" -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=15 pull --quiet --ff-only >/dev/null 2>&1 ||
    say "could not update $1; using it as it is"
}

found() {
  refresh "$1"
  cd "$1" && pwd -P
  exit $?
}

# Clone the brain to $1. The clone is made beside $1 and moved into place when it is complete,
# so an interrupted run leaves nothing that looks like a copy.
clone_to() {
  if [ -e "$1" ] && { [ ! -d "$1" ] || [ -n "$(ls -A "$1" 2>/dev/null)" ]; }; then
    is_brain "$1" && return 0 # another first run may have just finished
    say "'$1' exists and is not the brain. Move it away, or set AIE_BRAIN to another folder."
    return 1
  fi
  if ! command -v git >/dev/null 2>&1; then
    say "git is not installed, so the brain cannot be cloned."
    return 1
  fi
  say "no copy of the brain on this machine yet; cloning $REPO into $1"
  parent=$(dirname "$1")
  mkdir -p "$parent" || return 1
  staging=$(mktemp -d "$parent/.aie-brain-install.XXXXXXXX") || return 1
  clone="$staging/$(basename "$1")"
  if ! git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 clone --quiet --depth 1 "$REPO" "$clone" >&2; then
    rm -rf "$staging"
    say "the clone failed."
    return 1
  fi
  if ! is_brain "$clone"; then
    rm -rf "$staging"
    say "$REPO is not the brain."
    return 1
  fi
  date +%Y-%m-%d > "$clone/$STAMP"
  # Move into the parent under the final basename. If another run wins the
  # rename, mv fails instead of nesting this clone inside the winning clone.
  if ! mv "$clone" "$parent/" 2>/dev/null && ! is_brain "$1"; then
    rm -rf "$staging"
    say "could not put the clone at '$1'."
    return 1
  fi
  rm -rf "$staging"
}

if [ -n "$AIE_BRAIN" ]; then
  if is_brain "$AIE_BRAIN" || clone_to "$AIE_BRAIN"; then found "$AIE_BRAIN"; fi
  exit 1
fi

linked=$(cd "$(dirname "$0")" 2>/dev/null && cd "$(pwd -P)/../../.." 2>/dev/null && pwd -P)
if [ -n "$linked" ] && is_brain "$linked"; then found "$linked"; fi

dir=$(pwd -P)
while [ -n "$dir" ] && [ "$dir" != "/" ]; do
  if is_brain "$dir"; then found "$dir"; fi
  dir=$(dirname "$dir")
done

if [ -z "$HOME" ]; then
  say "HOME is not set. Set AIE_BRAIN to the folder where the brain should live."
  exit 1
fi
if is_brain "$HOME/.aie-brain" || clone_to "$HOME/.aie-brain"; then found "$HOME/.aie-brain"; fi
exit 1
