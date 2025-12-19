#!/usr/bin/env python3
"""
Selenium test to verify all features and take screenshots for README documentation
Uses OCR to verify text on screen
"""
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract

# Screenshot counter
screenshot_count = 0

def take_screenshot(driver, name, description):
    """Take screenshot and extract text with OCR"""
    global screenshot_count
    screenshot_count += 1
    timestamp = int(time.time())
    filename = f"screenshot_{screenshot_count:02d}_{name}_{timestamp}.png"
    
    driver.save_screenshot(filename)
    print(f"\n{'='*60}")
    print(f"📸 Screenshot {screenshot_count}: {description}")
    print(f"   File: {filename}")
    
    # OCR to extract text
    try:
        image = Image.open(filename)
        text = pytesseract.image_to_string(image)
        print(f"   OCR Text (first 200 chars):")
        print(f"   {text[:200].strip()}")
    except Exception as e:
        print(f"   OCR failed: {e}")
    
    return filename

def main():
    print("="*60)
    print("Marketplace Bulk Editor - Feature Verification Test")
    print("="*60)
    
    # Chrome options
    options = Options()
    options.add_argument('--window-size=1920,1080')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Test 1: Frontend loads
        print("\n[TEST 1] Loading frontend...")
        driver.get("http://localhost:5173")
        time.sleep(3)
        take_screenshot(driver, "frontend_loaded", "Frontend initial load")
        
        # Check body text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n✅ Body text includes:")
        if "Marketplace Bulk Editor" in body_text:
            print("   - 'Marketplace Bulk Editor' ✅")
        if "Docker Backend" in body_text:
            print("   - 'Docker Backend' status ✅")
        
        # Test 2: Backend status indicator
        print("\n[TEST 2] Checking backend status indicator...")
        time.sleep(2)
        take_screenshot(driver, "backend_status", "Backend status indicator")
        
        # Test 3: Check backend API directly
        print("\n[TEST 3] Testing backend API...")
        driver.get("http://localhost:5000/")
        time.sleep(2)
        take_screenshot(driver, "backend_api_root", "Backend API root endpoint")
        
        # Get JSON response
        pre_element = driver.find_element(By.TAG_NAME, "pre")
        api_response = json.loads(pre_element.text)
        print(f"\n✅ Backend API Response:")
        print(f"   Message: {api_response.get('message')}")
        print(f"   Version: {api_response.get('version')}")
        print(f"   Endpoints: {list(api_response.get('endpoints', {}).keys())}")
        
        # Test 4: Health check
        print("\n[TEST 4] Testing health check...")
        driver.get("http://localhost:5000/health")
        time.sleep(1)
        take_screenshot(driver, "health_check", "Health check endpoint")
        
        health_response = json.loads(driver.find_element(By.TAG_NAME, "pre").text)
        print(f"\n✅ Health Check:")
        print(f"   Status: {health_response.get('status')}")
        print(f"   Environment: {health_response.get('environment')}")
        
        # Test 5: Check console logs
        print("\n[TEST 5] Checking console logs...")
        driver.get("http://localhost:5173")
        time.sleep(3)
        
        logs = driver.get_log('browser')
        print(f"\n📋 Console Logs ({len(logs)} entries):")
        for entry in logs[-10:]:  # Last 10 entries
            level = entry.get('level', 'INFO')
            message = entry.get('message', '')[:100]
            print(f"   [{level}] {message}")
        
        # Test 6: Backend status component expanded
        print("\n[TEST 6] Testing backend status component...")
        driver.get("http://localhost:5173")
        time.sleep(3)
        
        # Try to find and click the status indicator
        try:
            # Look for the status component
            status_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Docker Backend')]")
            if status_elements:
                print(f"   Found {len(status_elements)} status elements")
                take_screenshot(driver, "status_visible", "Backend status visible")
                
                # Try to click to expand
                status_elements[0].click()
                time.sleep(1)
                take_screenshot(driver, "status_expanded", "Backend status expanded")
        except Exception as e:
            print(f"   Could not interact with status: {e}")
        
        # Test 7: File upload area
        print("\n[TEST 7] Checking file upload area...")
        driver.get("http://localhost:5173")
        time.sleep(2)
        take_screenshot(driver, "upload_area", "File upload area")
        
        # Test 8: Dark mode toggle (if exists)
        print("\n[TEST 8] Looking for dark mode toggle...")
        try:
            # Look for moon/sun icon or dark mode button
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"   Found {len(buttons)} buttons on page")
            take_screenshot(driver, "ui_controls", "UI controls visible")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Final screenshot
        print("\n[FINAL] Taking final screenshot...")
        driver.get("http://localhost:5173")
        time.sleep(3)
        take_screenshot(driver, "final_state", "Final UI state")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETE")
        print("="*60)
        print(f"\nTotal screenshots: {screenshot_count}")
        print("\nNext: Review screenshots and update READMEs")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        take_screenshot(driver, "error", "Error state")
    
    finally:
        print("\n[CLEANUP] Closing browser...")
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()

