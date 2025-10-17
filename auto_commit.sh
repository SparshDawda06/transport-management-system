#!/bin/bash

# Auto-commit script to continuously monitor and commit changes
echo "Starting auto-commit monitoring..."

while true; do
    # Check for any changes
    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo "$(date): Changes detected, committing..."
        
        # Add all changes
        git add -A
        
        # Commit with timestamp
        git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
        
        # Push to GitHub
        git push origin cursor/sync-and-clean-github-files-2210
        
        echo "$(date): Changes committed and pushed successfully"
    else
        echo "$(date): No changes detected"
    fi
    
    # Wait 30 seconds before checking again
    sleep 30
done