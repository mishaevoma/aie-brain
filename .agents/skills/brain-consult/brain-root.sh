#!/bin/sh
# Prints the root of the AI engineering brain.
# Works when this skill folder is reached through a symlink (for example from ~/.claude/skills).
cd "$(dirname "$0")" && cd "$(pwd -P)/../../.." && pwd -P
