#!/usr/bin/env python3
"""
Continue testing from existing Firefox window
Uses xdotool to find and connect to the open Firefox window
"""

import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create screenshots directory
os.makedirs('firefox_manual_test', exist_ok=True)

# Find Firefox window
print("Finding Firefox window...")
result = subprocess.run(['xdotool', 'search', '--name', 'Firefox'], 
                       capture_output=True, text=True)
if result.stdout.strip():
    window_id = result.stdout.strip().split('\n')[0]
    print(f"✓ Found Firefox window: {window_id}")
    
    # Activate window
    subprocess.run(['xdotool', 'windowactivate', window_id])
    time.sleep(1)
else:
    print("✗ No Firefox window found")
    exit(1)

# Connect to existing Firefox session
# Note: This requires Firefox to be started with remote debugging enabled
# For now, let's just start a new session and document what we see

options = Options()
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)

try:
    print("\n" + "=" * 80)
    print("MANUAL FIREFOX WINDOW TEST")
    print("=" * 80)
    
    # Load the app
    print("\n[1] Loading app...")
    driver.get("http://localhost:5173")
    time.sleep(3)
    driver.save_screenshot('firefox_manual_test/01_loaded.png')
    
    # Check current state
    print("\n[2] Checking authentication state...")
    try:
        # Look for Save/Load buttons (only visible when logged in)
        save_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Save')]")
        load_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Load')]")
        
        if save_btns and load_btns:
            print("  ✓ User is logged in (Save/Load buttons visible)")
            driver.save_screenshot('firefox_manual_test/02_logged_in.png')
        else:
            print("  ✗ User is NOT logged in")
            driver.save_screenshot('firefox_manual_test/02_not_logged_in.png')
    except Exception as e:
        print(f"  Error: {e}")
    
    # Upload sample data
    print("\n[3] Uploading sample data...")
    import pandas as pd
    sample_data = pd.DataFrame({
        'TITLE': ['Solar Panel 300W', 'Battery 12V', 'Inverter 2000W'],
        'PRICE': [150, 80, 200],
        'CONDITION': ['New', 'Used - Like New', 'New'],
        'DESCRIPTION': ['High efficiency', 'Rechargeable', 'Pure sine wave'],
        'CATEGORY': ['Electronics', 'Electronics', 'Electronics'],
        'OFFER SHIPPING': ['Yes', 'Yes', 'No']
    })
    sample_data.to_excel('firefox_test_sample.xlsx', index=False)
    
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(os.path.abspath('firefox_test_sample.xlsx'))
    time.sleep(3)
    driver.save_screenshot('firefox_manual_test/03_data_uploaded.png')
    print("  ✓ Data uploaded")
    
    # Try to save to database
    print("\n[4] Testing Save to Database...")
    try:
        save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
        is_disabled = save_btn.get_attribute('disabled')
        
        if is_disabled:
            print(f"  ✗ Save button is disabled: {is_disabled}")
        else:
            print("  ✓ Save button is enabled")
            print("  Clicking Save button...")
            save_btn.click()
            time.sleep(3)
            driver.save_screenshot('firefox_manual_test/04_save_clicked.png')
            
            # Check for error messages
            try:
                error_msgs = driver.find_elements(By.XPATH, "//*[contains(text(), 'Failed')]")
                if error_msgs:
                    print(f"  ✗ Error found: {error_msgs[0].text}")
                    driver.save_screenshot('firefox_manual_test/05_error_message.png')
                else:
                    print("  ✓ No error messages found")
            except:
                pass
    except Exception as e:
        print(f"  ✗ Error: {e}")
        driver.save_screenshot('firefox_manual_test/04_save_error.png')
    
    # Check console logs
    print("\n[5] Checking console logs...")
    try:
        logs = driver.get_log('browser')
        print(f"  Found {len(logs)} console entries")
        
        errors = [log for log in logs if log['level'] == 'SEVERE']
        warnings = [log for log in logs if log['level'] == 'WARNING']
        
        print(f"  Errors: {len(errors)}")
        print(f"  Warnings: {len(warnings)}")
        
        if errors:
            print("\n  Console Errors:")
            for err in errors[:5]:  # Show first 5
                print(f"    - {err['message'][:100]}")
    except Exception as e:
        print(f"  Could not get console logs: {e}")
    
    # Final screenshot
    driver.save_screenshot('firefox_manual_test/06_final_state.png')
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print(f"\n✓ Screenshots saved to firefox_manual_test/")
    print("\n⏸️  Browser left open for inspection")
    print("Press Ctrl+C to close...")
    time.sleep(300)

except KeyboardInterrupt:
    print("\n\n✓ Test interrupted by user")
except Exception as e:
    print(f"\n\n✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    driver.save_screenshot('firefox_manual_test/ERROR.png')
finally:
    print("\n✓ Closing browser...")
    driver.quit()

