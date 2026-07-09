#!/bin/bash
# backup-skill.sh - Backup skill files before applying updates
# Part of skill-improver

# Usage: ./backup-skill.sh <skill-path>
# Example: ./backup-skill.sh ~/.codex/skills/git-workflow

set -euo pipefail

# Check if path provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <skill-path>"
    echo "Example: $0 ~/.codex/skills/git-workflow"
    exit 1
fi

SKILL_PATH="$1"
SKILL_NAME=$(basename "$SKILL_PATH")
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$HOME/.codex/skills/backup/${SKILL_NAME}-${TIMESTAMP}"

# Check if skill path exists
if [ ! -d "$SKILL_PATH" ]; then
    echo "Error: Skill path not found: ${SKILL_PATH}"
    exit 1
fi

# Create backup directory
echo "Creating backup directory: ${BACKUP_DIR}"
mkdir -p "$BACKUP_DIR"

# Copy entire skill directory
echo "Backing up skill: ${SKILL_NAME}"
cp -R "$SKILL_PATH"/* "$BACKUP_DIR/"

# Keep backups restorable without making them discoverable as active skills.
# Codex skill discovery scans SKILL.md files recursively under ~/.codex/skills.
if [ -f "$BACKUP_DIR/SKILL.md" ]; then
    mv "$BACKUP_DIR/SKILL.md" "$BACKUP_DIR/SKILL.snapshot.md"
fi

# Create backup manifest
cat > "$BACKUP_DIR/backup-manifest.txt" <<EOF
Backup Manifest
==============
Skill Name: ${SKILL_NAME}
Source Path: ${SKILL_PATH}
Backup Date: $(date)
Timestamp: ${TIMESTAMP}

Files Backed Up:
$(find "$BACKUP_DIR" -type f ! -name "backup-manifest.txt" | sed "s|$BACKUP_DIR/||")

Restore Instructions:
-------------------
To restore this backup, run:
  cp -R ${BACKUP_DIR}/* ${SKILL_PATH}/
  if [ -f ${SKILL_PATH}/SKILL.snapshot.md ]; then mv ${SKILL_PATH}/SKILL.snapshot.md ${SKILL_PATH}/SKILL.md; fi

Discovery Note:
---------------
This backup stores SKILL.md as SKILL.snapshot.md so historical snapshots do not
appear as active skills in future Codex sessions.
EOF

echo "Backup complete!"
echo "Backup location: ${BACKUP_DIR}"
echo "Files backed up: $(find "$BACKUP_DIR" -type f ! -name "backup-manifest.txt" | wc -l)"
