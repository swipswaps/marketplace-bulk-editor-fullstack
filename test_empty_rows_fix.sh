#!/bin/bash
# Test script to verify empty rows fix

echo "=== Testing Empty Rows Fix ==="
echo ""
echo "Step 1: Finding Firefox window..."
WINDOW_ID=$(DISPLAY=:0 xdotool search --name "marketplace-bulk-editor" | head -1)
echo "Found window: $WINDOW_ID"

echo ""
echo "Step 2: Activating window..."
DISPLAY=:0 xdotool windowactivate $WINDOW_ID
sleep 1

echo ""
echo "Step 3: Opening DevTools Console (F12)..."
DISPLAY=:0 xdotool key F12
sleep 2

echo ""
echo "Step 4: Clearing localStorage..."
DISPLAY=:0 xdotool type "localStorage.clear()"
sleep 0.5
DISPLAY=:0 xdotool key Return
sleep 1

echo ""
echo "Step 5: Reloading page (F5)..."
DISPLAY=:0 xdotool key F5
sleep 3

echo ""
echo "Step 6: Taking screenshot..."
DISPLAY=:0 import -window root /tmp/after_localstorage_clear.png
echo "Screenshot saved to /tmp/after_localstorage_clear.png"

echo ""
echo "Step 7: Running OCR..."
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/after_localstorage_clear.png')
text = pytesseract.image_to_string(img)
print("=== OCR OUTPUT ===")
print(text)
print("")
print("=== CHECKING FOR EMPTY ROWS ===")
if "$0.00" in text:
    count = text.count("$0.00")
    print(f"❌ FOUND {count} instances of '$0.00' (empty rows still present)")
else:
    print("✅ NO '$0.00' found (empty rows fixed!)")
EOF

echo ""
echo "Step 8: Displaying screenshot in VSCode..."
code /tmp/after_localstorage_clear.png

echo ""
echo "=== Test Complete ==="

