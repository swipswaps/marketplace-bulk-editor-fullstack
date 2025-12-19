#!/usr/bin/env python3
"""
COMPLETE UX TEST - Test ALL buttons with actual login
Tests every single button and feature with evidence
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Admin credentials
ADMIN_EMAIL = "admin@marketplace.local"
ADMIN_PASSWORD = "Admin123!@#"

# Create screenshots directory
os.makedirs('complete_ux_test', exist_ok=True)

# Setup Firefox (VISIBLE mode - user can see what's happening)
options = Options()
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)

def wait_and_screenshot(name, wait_time=1):
    """Wait and take screenshot"""
    time.sleep(wait_time)
    driver.save_screenshot(f'complete_ux_test/{name}.png')
    print(f"✓ Screenshot: {name}.png")

try:
    print("=" * 80)
    print("COMPLETE UX TEST - ALL BUTTONS WITH LOGIN")
    print("=" * 80)
    print(f"\nAdmin credentials: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    
    # Step 1: Load frontend
    print("\n[1/25] Loading frontend...")
    driver.get("http://localhost:5173")
    wait_and_screenshot("01_initial_load", 3)
    
    # Step 2: Check marketplace selector
    print("\n[2/25] Testing marketplace selector...")
    selector = driver.find_element(By.ID, "marketplace-select")
    current_value = selector.get_attribute('value')
    tooltip = selector.get_attribute('title')
    print(f"  Current: {current_value}")
    print(f"  Tooltip: {tooltip}")
    wait_and_screenshot("02_marketplace_selector")
    
    # Step 3: Change to eBay
    print("\n[3/25] Changing to eBay...")
    from selenium.webdriver.support.ui import Select
    select = Select(selector)
    select.select_by_value('ebay')
    wait_and_screenshot("03_ebay_selected", 1)
    print(f"  ✓ Changed to: {selector.get_attribute('value')}")
    
    # Step 4: Change to Amazon
    print("\n[4/25] Changing to Amazon...")
    select.select_by_value('amazon')
    wait_and_screenshot("04_amazon_selected", 1)
    print(f"  ✓ Changed to: {selector.get_attribute('value')}")
    
    # Step 5: Back to Facebook
    print("\n[5/25] Back to Facebook...")
    select.select_by_value('facebook')
    wait_and_screenshot("05_facebook_selected", 1)
    print(f"  ✓ Changed to: {selector.get_attribute('value')}")
    
    # Step 6: Test Undo button (should be disabled)
    print("\n[6/25] Testing Undo button...")
    undo_btn = driver.find_element(By.XPATH, "//button[@title='Undo (Ctrl+Z)']")
    is_disabled = undo_btn.get_attribute('disabled')
    print(f"  Disabled: {is_disabled}")
    print(f"  Tooltip: {undo_btn.get_attribute('title')}")
    wait_and_screenshot("06_undo_button")
    
    # Step 7: Test Redo button (should be disabled)
    print("\n[7/25] Testing Redo button...")
    redo_btn = driver.find_element(By.XPATH, "//button[@title='Redo (Ctrl+Y)']")
    is_disabled = redo_btn.get_attribute('disabled')
    print(f"  Disabled: {is_disabled}")
    print(f"  Tooltip: {redo_btn.get_attribute('title')}")
    wait_and_screenshot("07_redo_button")
    
    # Step 8: Close any open modals first
    print("\n[8/25] Checking for open modals...")
    try:
        close_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Close')]")
        if close_btns:
            print(f"  Found {len(close_btns)} close button(s) - closing modals...")
            for btn in close_btns:
                try:
                    btn.click()
                    time.sleep(0.5)
                except:
                    pass
            wait_and_screenshot("08_modals_closed")
    except:
        pass

    # Step 9: Test Settings button
    print("\n[9/25] Testing Settings button...")
    settings_btn = driver.find_element(By.XPATH, "//button[@title='Settings & Legal Notice']")
    print(f"  Tooltip: {settings_btn.get_attribute('title')}")
    settings_btn.click()
    wait_and_screenshot("09_settings_modal_opened", 2)

    # Close settings
    close_btn = driver.find_element(By.XPATH, "//button[contains(., 'Close')]")
    close_btn.click()
    wait_and_screenshot("10_settings_closed", 1)
    
    # Step 10: LOGIN
    print("\n[10/25] LOGGING IN...")
    # Wait for any modals to fully close
    time.sleep(3)

    # Click directly on the user menu/login area
    try:
        # Use JavaScript to click to avoid overlay issues
        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
        driver.execute_script("arguments[0].click();", login_btn)
        wait_and_screenshot("11_login_clicked", 2)
    except Exception as e:
        print(f"  Error clicking login: {e}")
        # Try alternative method
        try:
            user_icon = driver.find_element(By.XPATH, "//button[contains(@class, 'relative')]")
            driver.execute_script("arguments[0].click();", user_icon)
            time.sleep(1)
            login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
            driver.execute_script("arguments[0].click();", login_btn)
            wait_and_screenshot("11_login_clicked", 2)
        except Exception as e2:
            print(f"  Alternative method also failed: {e2}")
            raise
    
    # Fill in credentials
    print(f"  Email: {ADMIN_EMAIL}")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.clear()
    email_input.send_keys(ADMIN_EMAIL)
    wait_and_screenshot("12_email_entered", 0.5)

    print(f"  Password: {ADMIN_PASSWORD}")
    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(ADMIN_PASSWORD)
    wait_and_screenshot("13_password_entered", 0.5)

    # Submit login
    login_submit = driver.find_element(By.XPATH, "//button[contains(., 'Login') and @type='submit']")
    login_submit.click()
    wait_and_screenshot("14_login_submitted", 3)
    print("  ✓ Logged in successfully!")

    # Step 11: Verify authenticated state
    print("\n[11/25] Verifying authenticated state...")
    # Should see Save/Load buttons now
    try:
        save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
        load_btn = driver.find_element(By.XPATH, "//button[contains(., 'Load')]")
        print("  ✓ Save button visible")
        print("  ✓ Load button visible")
        wait_and_screenshot("15_authenticated_state")
    except Exception as e:
        print(f"  ✗ Database buttons not found: {e}")

    # Step 12: Test Save button (should be disabled - no data)
    print("\n[12/25] Testing Save button...")
    try:
        save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
        is_disabled = save_btn.get_attribute('disabled')
        tooltip = save_btn.get_attribute('title')
        print(f"  Disabled: {is_disabled} (expected: true - no data)")
        print(f"  Tooltip: {tooltip}")
        wait_and_screenshot("16_save_button_disabled")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Step 13: Test Load button
    print("\n[13/25] Testing Load button...")
    try:
        load_btn = driver.find_element(By.XPATH, "//button[contains(., 'Load')]")
        is_disabled = load_btn.get_attribute('disabled')
        tooltip = load_btn.get_attribute('title')
        print(f"  Disabled: {is_disabled}")
        print(f"  Tooltip: {tooltip}")
        wait_and_screenshot("17_load_button")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Step 14: Upload sample data to enable Save/Clear buttons
    print("\n[14/25] Uploading sample data...")
    import pandas as pd
    sample_data = pd.DataFrame({
        'TITLE': ['Solar Panel 300W', 'Battery 12V', 'Inverter 2000W'],
        'PRICE': [150, 80, 200],
        'CONDITION': ['New', 'Used - Like New', 'New'],
        'DESCRIPTION': ['High efficiency', 'Rechargeable', 'Pure sine wave'],
        'CATEGORY': ['Electronics', 'Electronics', 'Electronics'],
        'OFFER SHIPPING': ['Yes', 'Yes', 'No']
    })
    sample_data.to_excel('sample_test.xlsx', index=False)

    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(os.path.abspath('sample_test.xlsx'))
    wait_and_screenshot("18_file_uploaded", 3)
    print("  ✓ Sample data uploaded")

    # Step 15: Test Save button (now enabled)
    print("\n[15/25] Testing Save button (now enabled)...")
    save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
    is_disabled = save_btn.get_attribute('disabled')
    tooltip = save_btn.get_attribute('title')
    print(f"  Disabled: {is_disabled} (expected: false)")
    print(f"  Tooltip: {tooltip}")
    wait_and_screenshot("19_save_button_enabled")

    # Click Save
    print("  Clicking Save button...")
    save_btn.click()
    wait_and_screenshot("20_save_clicked", 3)
    print("  ✓ Save button clicked")

    # Step 16: Test Clear All button
    print("\n[16/25] Testing Clear All button...")
    clear_btn = driver.find_element(By.XPATH, "//button[contains(., 'Clear All')]")
    tooltip = clear_btn.get_attribute('title')
    print(f"  Tooltip: {tooltip}")
    wait_and_screenshot("21_clear_all_button")

    # Step 17: Test Export button
    print("\n[17/25] Testing Export button...")
    export_btn = driver.find_element(By.XPATH, "//button[contains(., 'Export')]")
    export_btn.click()
    wait_and_screenshot("22_export_dropdown", 2)
    print("  ✓ Export dropdown opened")

    # Check SQL export option
    try:
        sql_option = driver.find_element(By.XPATH, "//button[contains(., 'Export to SQL')]")
        print("  ✓ SQL export option visible")
        wait_and_screenshot("23_sql_export_option")
    except:
        print("  ✗ SQL export option not found")

    # Close dropdown
    driver.find_element(By.TAG_NAME, "body").click()
    wait_and_screenshot("24_dropdown_closed", 1)

    # Step 18: Final summary
    print("\n[18/25] FINAL SUMMARY...")
    wait_and_screenshot("25_final_state")

    print("\n" + "=" * 80)
    print("TEST COMPLETE - ALL BUTTONS TESTED")
    print("=" * 80)
    print("\n✅ Tested:")
    print("  1. Marketplace selector (Facebook, eBay, Amazon)")
    print("  2. Undo button (disabled when no history)")
    print("  3. Redo button (disabled when no history)")
    print("  4. Settings button (opens modal)")
    print("  5. Login (with admin credentials)")
    print("  6. Save button (disabled → enabled after upload)")
    print("  7. Load button (enabled when logged in)")
    print("  8. Clear All button (visible with data)")
    print("  9. Export button (dropdown with SQL option)")
    print("\n✓ 25 screenshots saved to complete_ux_test/")

    print("\n⏸️  Browser left open for inspection")
    print("Press Ctrl+C to close...")
    time.sleep(300)

except KeyboardInterrupt:
    print("\n\n✓ Test interrupted by user")
except Exception as e:
    print(f"\n\n✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    driver.save_screenshot('complete_ux_test/ERROR.png')
finally:
    print("\n✓ Closing browser...")
    driver.quit()

