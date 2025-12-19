#!/usr/bin/env python3
"""
Test UX improvements - examine current state and identify issues
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Create screenshots directory
os.makedirs('ux_improvements_screenshots', exist_ok=True)

# Setup Firefox (VISIBLE mode)
options = Options()
# DO NOT use headless mode - user wants to see the browser
options.set_preference('devtools.console.stdout.content', True)

driver = webdriver.Firefox(options=options)
driver.set_window_size(1920, 1080)

try:
    print("=" * 80)
    print("UX IMPROVEMENTS TEST - Examining Current State")
    print("=" * 80)
    
    # Step 1: Load frontend
    print("\n[1/10] Loading frontend...")
    driver.get("http://localhost:5173")
    time.sleep(3)
    driver.save_screenshot('ux_improvements_screenshots/01_initial_state.png')
    print("✓ Screenshot: 01_initial_state.png")
    
    # Step 2: Examine header buttons
    print("\n[2/10] Examining header buttons...")
    header_buttons = driver.find_elements(By.CSS_SELECTOR, "header button")
    print(f"Found {len(header_buttons)} buttons in header")
    for i, btn in enumerate(header_buttons):
        text = btn.text or btn.get_attribute('title') or btn.get_attribute('aria-label')
        print(f"  Button {i+1}: {text}")
    driver.save_screenshot('ux_improvements_screenshots/02_header_buttons.png')
    print("✓ Screenshot: 02_header_buttons.png")
    
    # Step 3: Check for "Clear All" button
    print("\n[3/10] Looking for 'Clear All' button...")
    try:
        clear_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear All')]")
        print(f"✓ Found 'Clear All' button: {clear_btn.text}")
        driver.save_screenshot('ux_improvements_screenshots/03_clear_all_button.png')
    except:
        print("✗ 'Clear All' button not found")
    
    # Step 4: Upload sample data
    print("\n[4/10] Creating sample data...")
    # Click "Add Row" button multiple times
    try:
        add_row_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Add Row')]")
        for i in range(3):
            add_row_btn.click()
            time.sleep(0.5)
        print("✓ Added 3 rows")
        driver.save_screenshot('ux_improvements_screenshots/04_sample_data_added.png')
    except Exception as e:
        print(f"✗ Could not add rows: {e}")
    
    # Step 5: Test "Clear All" button
    print("\n[5/10] Testing 'Clear All' button...")
    try:
        clear_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear All')]")
        clear_btn.click()
        time.sleep(1)
        driver.save_screenshot('ux_improvements_screenshots/05_after_clear_all.png')
        
        # Check if data was cleared
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        if len(rows) == 0:
            print("✓ 'Clear All' worked - all rows removed")
        else:
            print(f"✗ 'Clear All' FAILED - {len(rows)} rows still present")
    except Exception as e:
        print(f"✗ Could not test 'Clear All': {e}")
    
    # Step 6: Check tooltips
    print("\n[6/10] Checking for tooltips...")
    buttons_with_tooltips = driver.find_elements(By.CSS_SELECTOR, "button[title]")
    print(f"Found {len(buttons_with_tooltips)} buttons with tooltips")
    for btn in buttons_with_tooltips[:5]:  # Show first 5
        title = btn.get_attribute('title')
        text = btn.text or '(icon only)'
        print(f"  '{text}' → tooltip: '{title}'")
    driver.save_screenshot('ux_improvements_screenshots/06_tooltips_check.png')
    
    # Step 7: Examine button organization
    print("\n[7/10] Examining button organization in header...")
    header = driver.find_element(By.TAG_NAME, "header")
    header_html = header.get_attribute('outerHTML')[:500]
    print(f"Header HTML (first 500 chars):\n{header_html}")
    driver.save_screenshot('ux_improvements_screenshots/07_header_organization.png')
    
    # Step 8: Check for database selector
    print("\n[8/10] Looking for database selector...")
    try:
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"Found {len(selects)} select elements")
        for sel in selects:
            label = sel.get_attribute('aria-label') or sel.get_attribute('name')
            print(f"  Select: {label}")
    except Exception as e:
        print(f"No select elements found: {e}")
    driver.save_screenshot('ux_improvements_screenshots/08_database_selector_check.png')
    
    # Step 9: Login and check authenticated state
    print("\n[9/10] Testing authenticated state...")
    try:
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_btn.click()
        time.sleep(1)
        driver.save_screenshot('ux_improvements_screenshots/09_login_modal.png')
        
        # Close modal
        close_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
        close_btn.click()
        time.sleep(0.5)
    except Exception as e:
        print(f"Could not test login: {e}")
    
    # Step 10: Final state
    print("\n[10/10] Final state...")
    driver.save_screenshot('ux_improvements_screenshots/10_final_state.png')
    
    # Console logs
    print("\n" + "=" * 80)
    print("CONSOLE LOGS")
    print("=" * 80)
    logs = driver.get_log('browser')
    errors = [log for log in logs if log['level'] == 'SEVERE']
    warnings = [log for log in logs if log['level'] == 'WARNING']
    
    print(f"\nTotal console entries: {len(logs)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    
    if errors:
        print("\n⚠️ ERRORS:")
        for err in errors[:5]:
            print(f"  {err['message'][:100]}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print(f"\n✓ 10 screenshots saved to ux_improvements_screenshots/")
    
    # Keep browser open for user to inspect
    print("\n⏸️  Browser window left open for inspection")
    print("Press Ctrl+C to close...")
    time.sleep(300)  # Keep open for 5 minutes

except KeyboardInterrupt:
    print("\n\n✓ Test interrupted by user")
except Exception as e:
    print(f"\n\n✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
    print("\n✓ Browser closed")

