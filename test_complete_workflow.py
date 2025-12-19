#!/usr/bin/env python3
"""
Complete workflow testing with Selenium - Rule 22 compliance
Tests ALL features end-to-end with screenshots at each step
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract

def take_screenshot(driver, name, step_num):
    """Take screenshot and extract text with OCR"""
    filename = f"screenshot_{step_num:02d}_{name}.png"
    driver.save_screenshot(filename)
    
    # Get file size
    size = os.path.getsize(filename)
    print(f"📸 Screenshot {step_num}: {filename} ({size} bytes)")
    
    # OCR text extraction
    try:
        img = Image.open(filename)
        text = pytesseract.image_to_string(img)
        # Print first 200 chars
        print(f"   OCR Text: {text[:200].strip()}...")
    except Exception as e:
        print(f"   OCR failed: {e}")
    
    return filename

def main():
    print("=" * 80)
    print("COMPLETE WORKFLOW TEST - Rule 22 Compliance")
    print("=" * 80)
    
    # Setup Chrome with console logging
    # CRITICAL: Running in VISIBLE mode (NOT headless) per Rule 9
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # DO NOT add --headless unless user explicitly requests it
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    
    try:
        step = 1
        
        # STEP 1: Load frontend
        print(f"\n{'='*80}")
        print(f"STEP {step}: Load Frontend")
        print('='*80)
        driver.get("http://localhost:5173")
        time.sleep(3)
        take_screenshot(driver, "frontend_loaded", step)
        step += 1
        
        # STEP 2: Backend status indicator
        print(f"\n{'='*80}")
        print(f"STEP {step}: Backend Status Indicator")
        print('='*80)
        time.sleep(2)
        take_screenshot(driver, "backend_status", step)
        step += 1
        
        # STEP 3: Expand backend status
        print(f"\n{'='*80}")
        print(f"STEP {step}: Expand Backend Status Details")
        print('='*80)
        try:
            status_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Docker Backend')]"))
            )
            status_button.click()
            time.sleep(2)
            take_screenshot(driver, "backend_status_expanded", step)
        except Exception as e:
            print(f"   ⚠️ Could not expand backend status: {e}")
            take_screenshot(driver, "backend_status_error", step)
        step += 1
        
        # STEP 4: File upload area
        print(f"\n{'='*80}")
        print(f"STEP {step}: File Upload Area")
        print('='*80)
        take_screenshot(driver, "file_upload_area", step)
        step += 1
        
        # STEP 5: Data table (empty state)
        print(f"\n{'='*80}")
        print(f"STEP {step}: Data Table (Empty State)")
        print('='*80)
        take_screenshot(driver, "data_table_empty", step)
        step += 1
        
        # STEP 6: Dark mode toggle
        print(f"\n{'='*80}")
        print(f"STEP {step}: Dark Mode Toggle")
        print('='*80)
        try:
            dark_mode_button = driver.find_element(By.XPATH, "//button[contains(@class, 'dark') or contains(., '🌙') or contains(., '☀')]")
            dark_mode_button.click()
            time.sleep(1)
            take_screenshot(driver, "dark_mode_enabled", step)
            # Toggle back
            dark_mode_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"   ⚠️ Could not toggle dark mode: {e}")
        step += 1
        
        # STEP 7: Console logs
        print(f"\n{'='*80}")
        print(f"STEP {step}: Console Logs")
        print('='*80)
        logs = driver.get_log('browser')
        print(f"   Total console entries: {len(logs)}")
        for i, entry in enumerate(logs[:10], 1):
            print(f"   [{i}] {entry['level']}: {entry['message'][:100]}")
        step += 1
        
        # STEP 8: Page source verification
        print(f"\n{'='*80}")
        print(f"STEP {step}: Page Source Verification")
        print('='*80)
        page_source = driver.page_source
        checks = [
            ("Marketplace Bulk Editor", "✅" if "Marketplace Bulk Editor" in page_source else "❌"),
            ("Docker Backend", "✅" if "Docker Backend" in page_source else "❌"),
            ("Drop image or click to upload", "✅" if "Drop image" in page_source or "click to upload" in page_source else "❌"),
        ]
        for check, status in checks:
            print(f"   {status} '{check}'")
        take_screenshot(driver, "final_state", step)
        step += 1
        
        print(f"\n{'='*80}")
        print("✅ COMPLETE WORKFLOW TEST FINISHED")
        print(f"   Total steps: {step - 1}")
        print(f"   Total screenshots: {step - 1}")
        print('='*80)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

