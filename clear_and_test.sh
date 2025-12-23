#!/bin/bash
# Clear localStorage and test migration

echo "=== Step 1: Find Firefox window ==="
DISPLAY=:0 xdotool search --name "marketplace-bulk-editor" 2>/dev/null | head -1

WID=$(DISPLAY=:0 xdotool search --name "marketplace-bulk-editor" 2>/dev/null | head -1)
echo "Window ID: $WID"

echo ""
echo "=== Step 2: Open DevTools Console ==="
DISPLAY=:0 xdotool windowactivate $WID
sleep 0.5
DISPLAY=:0 xdotool key F12
sleep 2

echo ""
echo "=== Step 3: Clear localStorage ==="
DISPLAY=:0 xdotool type "localStorage.clear()"
sleep 0.5
DISPLAY=:0 xdotool key Return
sleep 1

echo ""
echo "=== Step 4: Reload page ==="
DISPLAY=:0 xdotool key F5
sleep 5

echo ""
echo "=== Step 5: Take screenshot ==="
DISPLAY=:0 import -window root /tmp/after_clear_test.png

echo ""
echo "=== Step 6: Run OCR ==="
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/after_clear_test.png')
text = pytesseract.image_to_string(img)
print("=== OCR OUTPUT ===")
print(text)
print("")
count = text.count("$0.00")
print(f"Empty rows with $0.00: {count}")
if count == 0:
    print("✅ FIXED! No empty rows")
else:
    print(f"❌ Still has {count} empty rows")
EOF

echo ""
echo "=== Step 7: Display screenshot ==="
code /tmp/after_clear_test.png

