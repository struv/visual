#!/bin/bash

# Convert Windows line endings to Unix
sed -i 's/\r$//' ralph-once.sh

echo "=== Ralph Loop (Human-in-the-Loop Mode) ==="
echo "Starting task..."
echo ""

claude --permission-mode acceptEdits -p "Read @PRD.md and @progress.txt. Find the next incomplete task (marked [ ]) and implement it. After implementing, update progress.txt with what you did and mark the task complete in PRD.md. ONLY DO ONE TASK."

echo ""
echo "=== Task complete. Review the changes, then run again for next task. ==="
