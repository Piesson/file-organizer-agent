#!/bin/bash

# File Organizer Agent - Installation Script
# Installs the /organize command to Claude Code

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"

echo "=== File Organizer Agent Installer ==="
echo ""

# Create commands directory if it doesn't exist
if [ ! -d "$CLAUDE_COMMANDS_DIR" ]; then
    echo "Creating $CLAUDE_COMMANDS_DIR..."
    mkdir -p "$CLAUDE_COMMANDS_DIR"
fi

# Copy organize.md to commands directory
echo "Installing /organize command..."
cp "$SCRIPT_DIR/organize.md" "$CLAUDE_COMMANDS_DIR/organize.md"

# Verify installation
if [ -f "$CLAUDE_COMMANDS_DIR/organize.md" ]; then
    echo ""
    echo "Installation successful!"
    echo ""
    echo "Usage: In Claude Code, type /organize to run the file organizer"
    echo ""
    echo "Installed files:"
    echo "  - $CLAUDE_COMMANDS_DIR/organize.md"
else
    echo "Error: Installation failed"
    exit 1
fi
