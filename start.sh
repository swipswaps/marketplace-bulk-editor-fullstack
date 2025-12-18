#!/bin/bash

# Marketplace Bulk Editor - Start Script
# Ensures clean startup with no stray processes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/.vite.pid"
LOG_FILE="$SCRIPT_DIR/.vite.log"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "❌ Server is already running (PID: $PID)"
        echo "   Run ./stop.sh first to stop it"
        exit 1
    else
        # Stale PID file, remove it
        rm -f "$PID_FILE"
    fi
fi

# Kill any existing vite processes for this project
echo "🧹 Cleaning up any stray processes..."
pkill -f "vite.*marketplace-bulk-editor" 2>/dev/null || true
sleep 1

# Start the dev server
echo "🚀 Starting Marketplace Bulk Editor..."
echo "📁 Working directory: $SCRIPT_DIR"
echo "📝 Logs: $LOG_FILE"

# Start vite in background and capture PID
nohup npm run dev > "$LOG_FILE" 2>&1 &
VITE_PID=$!

# Save PID
echo "$VITE_PID" > "$PID_FILE"

# Wait a moment for server to start
sleep 2

# Check if process is still running
if ps -p "$VITE_PID" > /dev/null 2>&1; then
    echo "✅ Server started successfully (PID: $VITE_PID)"
    echo ""
    echo "   Local:   http://localhost:5173"
    echo "   Network: Check the log file for network URL"
    echo ""
    echo "📊 To view logs: tail -f $LOG_FILE"
    echo "🛑 To stop: ./stop.sh"
else
    echo "❌ Failed to start server"
    echo "   Check logs: cat $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi

