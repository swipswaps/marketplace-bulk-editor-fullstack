#!/bin/bash
# Diagnostic script to check localStorage contents

echo "=== Diagnosing localStorage Contents ==="
echo ""

WINDOW_ID=$(DISPLAY=:0 xdotool search --name "marketplace-bulk-editor" | head -1)
echo "Found window: $WINDOW_ID"

echo ""
echo "Activating window and opening console..."
DISPLAY=:0 xdotool windowactivate $WINDOW_ID
sleep 1
DISPLAY=:0 xdotool key F12
sleep 2

echo ""
echo "Getting localStorage.listings..."
DISPLAY=:0 xdotool type "console.log(JSON.parse(localStorage.getItem('listings') || '[]').slice(0, 3))"
sleep 0.5
DISPLAY=:0 xdotool key Return
sleep 2

echo ""
echo "Taking screenshot of console..."
DISPLAY=:0 import -window root /tmp/console_localstorage.png
code /tmp/console_localstorage.png

echo ""
echo "Check the screenshot to see what's in localStorage!"

