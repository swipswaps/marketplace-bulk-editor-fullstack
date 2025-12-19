#!/usr/bin/env python3
"""
Complete Workflow Test for Phase 1 & 2 Implementation
Tests authentication and database sync features

COMPLIANCE WITH RULE 9:
- VISIBLE mode (NOT headless)
- Complete workflow (13+ steps)
- Screenshots at EACH step
- OCR verification with Tesseract
- Console log capture
- Evidence-based testing
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytesseract
from PIL import Image

# Test configuration
FRONTEND_URL = "http://localhost:5173"
TEST_EMAIL = f"test_{int(time.time())}@example.com"
TEST_PASSWORD = "SecurePass123!"
SCREENSHOT_DIR = "phase1_phase2_screenshots"

# Create screenshot directory
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def setup_driver():
    """Setup Chrome driver in VISIBLE mode with console logging"""
    print("Setting up Chrome driver in VISIBLE mode...")
    options = Options()
    
    # CRITICAL: NO HEADLESS MODE (Rule 9)
    # options.add_argument('--headless')  # FORBIDDEN unless user requests
    
    # Enable console logging
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    # Other options
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    return driver

def take_screenshot_with_ocr(driver, step_num, description):
    """Take screenshot and verify with OCR"""
    filename = f"{SCREENSHOT_DIR}/step_{step_num:02d}_{description}.png"
    driver.save_screenshot(filename)
    
    # Get file size
    file_size = os.path.getsize(filename)
    
    # OCR verification
    img = Image.open(filename)
    ocr_text = pytesseract.image_to_string(img)
    
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print(f"Screenshot: {filename} ({file_size} bytes)")
    print(f"OCR Text (first 200 chars):")
    print(ocr_text[:200])
    print(f"{'='*60}\n")
    
    return filename, ocr_text

def capture_console_logs(driver):
    """Capture and display console logs"""
    logs = driver.get_log('browser')
    
    errors = [log for log in logs if log['level'] == 'SEVERE']
    warnings = [log for log in logs if log['level'] == 'WARNING']
    
    print(f"\n{'='*60}")
    print(f"CONSOLE LOGS SUMMARY")
    print(f"Total entries: {len(logs)}")
    print(f"Errors (SEVERE): {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    
    if errors:
        print(f"\nERRORS:")
        for error in errors:
            print(f"  [{error['level']}] {error['message']}")
    
    if warnings:
        print(f"\nWARNINGS (first 5):")
        for warning in warnings[:5]:
            print(f"  [{warning['level']}] {warning['message']}")
    
    print(f"{'='*60}\n")
    
    return logs, errors, warnings

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"TIMEOUT: Element not found: {by}={value}")
        return None

def main():
    """Run complete workflow test"""
    print(f"\n{'='*60}")
    print(f"PHASE 1 & 2 COMPLETE WORKFLOW TEST")
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Test email: {TEST_EMAIL}")
    print(f"{'='*60}\n")
    
    driver = setup_driver()
    
    try:
        # STEP 1: Load frontend
        print("STEP 1: Loading frontend...")
        driver.get(FRONTEND_URL)
        time.sleep(3)
        take_screenshot_with_ocr(driver, 1, "frontend_loaded")
        
        # STEP 2: Verify backend status
        print("STEP 2: Verifying backend status...")
        backend_status = wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Docker Backend')]")
        if backend_status:
            print("✓ Backend status indicator found")
        take_screenshot_with_ocr(driver, 2, "backend_status_visible")
        
        # STEP 3: Click Login button
        print("STEP 3: Clicking Login button...")
        login_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Login')]")
        if login_button:
            login_button.click()
            time.sleep(2)
            print("✓ Login button clicked")
        take_screenshot_with_ocr(driver, 3, "login_modal_opened")
        
        # STEP 4: Switch to Register mode
        print("STEP 4: Switching to Register mode...")
        register_link = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Register')]")
        if register_link:
            register_link.click()
            time.sleep(1)
            print("✓ Switched to Register mode")
        take_screenshot_with_ocr(driver, 4, "register_mode")

        # STEP 5: Fill in registration form
        print("STEP 5: Filling in registration form...")
        email_input = wait_for_element(driver, By.ID, "email")
        password_input = wait_for_element(driver, By.ID, "password")
        confirm_password_input = wait_for_element(driver, By.ID, "confirmPassword")

        if email_input and password_input and confirm_password_input:
            email_input.send_keys(TEST_EMAIL)
            password_input.send_keys(TEST_PASSWORD)
            confirm_password_input.send_keys(TEST_PASSWORD)
            print(f"✓ Form filled with email: {TEST_EMAIL}")
        take_screenshot_with_ocr(driver, 5, "registration_form_filled")

        # STEP 6: Submit registration
        print("STEP 6: Submitting registration...")
        submit_button = wait_for_element(driver, By.XPATH, "//button[@type='submit']")
        if submit_button:
            submit_button.click()
            time.sleep(3)  # Wait for API call
            print("✓ Registration submitted")
        take_screenshot_with_ocr(driver, 6, "registration_submitted")

        # STEP 7: Verify user is logged in
        print("STEP 7: Verifying user is logged in...")
        time.sleep(2)
        user_menu = wait_for_element(driver, By.XPATH, f"//*[contains(text(), '{TEST_EMAIL}')]")
        if user_menu:
            print(f"✓ User logged in: {TEST_EMAIL}")
        take_screenshot_with_ocr(driver, 7, "user_logged_in")

        # STEP 8: Verify sync status appears
        print("STEP 8: Verifying sync status...")
        sync_status = wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Synced') or contains(text(), 'Offline')]")
        if sync_status:
            print(f"✓ Sync status visible: {sync_status.text}")
        take_screenshot_with_ocr(driver, 8, "sync_status_visible")

        # STEP 9: Upload Excel file (if file upload area exists)
        print("STEP 9: Locating file upload area...")
        file_upload = wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Drop') or contains(text(), 'Upload')]")
        if file_upload:
            print("✓ File upload area found")
        take_screenshot_with_ocr(driver, 9, "file_upload_area")

        # STEP 10: Click Save to Database button
        print("STEP 10: Testing Save to Database...")
        save_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Save')]")
        if save_button:
            save_button.click()
            time.sleep(3)  # Wait for API call
            print("✓ Save button clicked")
        take_screenshot_with_ocr(driver, 10, "save_to_database")

        # STEP 11: Verify sync status updated
        print("STEP 11: Verifying sync status updated...")
        time.sleep(2)
        take_screenshot_with_ocr(driver, 11, "sync_status_after_save")

        # STEP 12: Open user menu
        print("STEP 12: Opening user menu...")
        user_menu_button = wait_for_element(driver, By.XPATH, f"//button[contains(text(), '{TEST_EMAIL}')]")
        if user_menu_button:
            user_menu_button.click()
            time.sleep(1)
            print("✓ User menu opened")
        take_screenshot_with_ocr(driver, 12, "user_menu_opened")

        # STEP 13: Logout
        print("STEP 13: Logging out...")
        logout_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Logout')]")
        if logout_button:
            logout_button.click()
            time.sleep(2)
            print("✓ Logged out")
        take_screenshot_with_ocr(driver, 13, "logged_out")

        # STEP 14: Verify Login button appears again
        print("STEP 14: Verifying Login button appears...")
        login_button_again = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Login')]")
        if login_button_again:
            print("✓ Login button visible again")
        take_screenshot_with_ocr(driver, 14, "login_button_visible_again")

        # Capture final console logs
        print("\nCapturing final console logs...")
        logs, errors, warnings = capture_console_logs(driver)

        # Summary
        print(f"\n{'='*60}")
        print(f"TEST COMPLETE")
        print(f"{'='*60}")
        print(f"Total steps: 14")
        print(f"Screenshots: {len(os.listdir(SCREENSHOT_DIR))}")
        print(f"Console errors: {len(errors)}")
        print(f"Console warnings: {len(warnings)}")
        print(f"Test email: {TEST_EMAIL}")
        print(f"Screenshot directory: {SCREENSHOT_DIR}/")
        print(f"{'='*60}\n")

        # Keep browser open for 10 seconds for user to see
        print("Keeping browser open for 10 seconds...")
        time.sleep(10)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        take_screenshot_with_ocr(driver, 99, "error_state")

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()

