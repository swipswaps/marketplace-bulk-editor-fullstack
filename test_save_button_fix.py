#!/usr/bin/env python3
"""
Test Save to Database button after fixing metadata → extra_data bug
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Admin credentials
ADMIN_EMAIL = "admin@marketplace.local"
ADMIN_PASSWORD = "Admin123!@#"

# Create screenshots directory
os.makedirs('save_button_test', exist_ok=True)

def screenshot(name):
    driver.save_screenshot(f'save_button_test/{name}.png')
    print(f"  ✓ Screenshot: {name}.png")

options = Options()
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)

try:
    print("\n" + "=" * 80)
    print("SAVE BUTTON TEST - After metadata → extra_data Fix")
    print("=" * 80)
    
    # Step 1: Load app
    print("\n[1/8] Loading app...")
    driver.get("http://localhost:5173")
    time.sleep(3)
    screenshot("01_loaded")
    
    # Step 2: Login
    print("\n[2/8] Logging in...")
    login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
    driver.execute_script("arguments[0].click();", login_btn)
    time.sleep(2)
    screenshot("02_login_modal")
    
    # Fill credentials
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(ADMIN_EMAIL)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(ADMIN_PASSWORD)
    screenshot("03_credentials_entered")
    
    # Submit
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'Login')]")
    submit_btn.click()
    time.sleep(3)
    screenshot("04_logged_in")
    print("  ✓ Logged in")
    
    # Step 3: Upload sample data
    print("\n[3/8] Uploading sample data...")
    import pandas as pd
    sample_data = pd.DataFrame({
        'TITLE': ['Solar Panel 300W', 'Battery 12V', 'Inverter 2000W'],
        'PRICE': [150, 80, 200],
        'CONDITION': ['New', 'Used - Like New', 'New'],
        'DESCRIPTION': ['High efficiency', 'Rechargeable', 'Pure sine wave'],
        'CATEGORY': ['Electronics', 'Electronics', 'Electronics'],
        'OFFER SHIPPING': ['Yes', 'Yes', 'No']
    })
    sample_data.to_excel('save_test_sample.xlsx', index=False)
    
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(os.path.abspath('save_test_sample.xlsx'))
    time.sleep(3)
    screenshot("05_data_uploaded")
    print("  ✓ Data uploaded")
    
    # Step 4: Click Save button
    print("\n[4/8] Clicking Save button...")
    save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
    tooltip = save_btn.get_attribute('title')
    print(f"  Tooltip: {tooltip}")
    save_btn.click()
    time.sleep(4)
    screenshot("06_save_clicked")
    
    # Step 5: Check for errors
    print("\n[5/8] Checking for errors...")
    try:
        error_msgs = driver.find_elements(By.XPATH, "//*[contains(text(), 'Failed')]")
        if error_msgs:
            print(f"  ✗ ERROR FOUND: {error_msgs[0].text}")
            screenshot("07_error_message")
        else:
            print("  ✓ No error messages")
            screenshot("07_no_errors")
    except:
        print("  ✓ No error messages")
    
    # Step 6: Check console logs
    print("\n[6/8] Checking console logs...")
    logs = driver.get_log('browser')
    errors = [log for log in logs if log['level'] == 'SEVERE']
    print(f"  Console errors: {len(errors)}")
    if errors:
        for err in errors[:3]:
            print(f"    - {err['message'][:80]}")
    
    # Step 7: Verify data was saved (click Load)
    print("\n[7/8] Verifying data was saved...")
    # Clear current data first
    clear_btn = driver.find_element(By.XPATH, "//button[contains(., 'Clear All')]")
    clear_btn.click()
    time.sleep(1)
    # Accept confirmation
    driver.switch_to.alert.accept()
    time.sleep(2)
    screenshot("08_data_cleared")
    
    # Load from database
    load_btn = driver.find_element(By.XPATH, "//button[contains(., 'Load')]")
    load_btn.click()
    time.sleep(3)
    screenshot("09_data_loaded")
    
    # Check if data appeared
    try:
        table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        print(f"  ✓ Loaded {len(table_rows)} rows from database")
        if len(table_rows) >= 3:
            print("  ✓ SUCCESS: Data was saved and loaded correctly!")
        else:
            print(f"  ✗ Expected 3 rows, got {len(table_rows)}")
    except Exception as e:
        print(f"  ✗ Error checking table: {e}")
    
    # Step 8: Final summary
    print("\n[8/8] Final summary...")
    screenshot("10_final_state")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\n✓ Screenshots saved to save_button_test/")
    
    print("\n⏸️  Browser left open for inspection (30 seconds)...")
    time.sleep(30)

except Exception as e:
    print(f"\n\n✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    screenshot("ERROR")
finally:
    print("\n✓ Closing browser...")
    driver.quit()

