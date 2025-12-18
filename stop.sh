#!/bin/bash

# Marketplace Bulk Editor - Stop Script
# Ensures clean shutdown with no stray processes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/.vite.pid"

echo "🛑 Stopping Marketplace Bulk Editor..."

# Check if PID file exists
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    
    # Check if process is running
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "   Stopping process (PID: $PID)..."
        kill "$PID" 2>/dev/null
        
        # Wait for graceful shutdown
        for i in {1..5}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "   Force killing process..."
            kill -9 "$PID" 2>/dev/null
        fi
        
        echo "✅ Process stopped"
    else
        echo "⚠️  Process not running (stale PID file)"
    fi
    
    rm -f "$PID_FILE"
else
    echo "⚠️  No PID file found"
fi

# Clean up any remaining vite processes for this project
echo "🧹 Cleaning up any stray processes..."
KILLED=$(pkill -f "vite.*marketplace-bulk-editor" 2>/dev/null && echo "yes" || echo "no")

if [ "$KILLED" = "yes" ]; then
    echo "   Killed stray vite processes"
fi

# Clean up any node processes on port 5173
PORT_PID=$(lsof -ti:5173 2>/dev/null)
if [ -n "$PORT_PID" ]; then
    echo "   Killing process on port 5173 (PID: $PORT_PID)..."
    kill -9 "$PORT_PID" 2>/dev/null
fi

echo "✅ Shutdown complete"

