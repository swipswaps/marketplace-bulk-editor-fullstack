#!/usr/bin/env python3
"""
Complete user workflow test following README.md including backend/database usage.
Per Rule 9: VISIBLE mode, OCR verification, screenshots at EACH step.
"""

import time
import json
import requests
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_screenshot_with_ocr(driver, filename, expected_texts=None):
    """Save screenshot and verify with OCR"""
    driver.save_screenshot(filename)
    print(f"\n📸 Screenshot saved: {filename}")
    
    img = Image.open(filename)
    text = pytesseract.image_to_string(img)
    print(f"   OCR extracted text (first 300 chars): {text[:300]}")
    
    if expected_texts:
        for expected in expected_texts:
            if expected in text:
                print(f"   ✅ Found: '{expected}'")
            else:
                print(f"   ❌ NOT FOUND: '{expected}'")
    
    return text

def main():
    print("=" * 80)
    print("COMPLETE USER WORKFLOW TEST - BACKEND + FRONTEND")
    print("=" * 80)
    
    # Setup Chrome in VISIBLE mode
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    
    access_token = None
    
    try:
        # BACKEND WORKFLOW
        print("\n" + "=" * 80)
        print("BACKEND WORKFLOW - User Registration & Authentication")
        print("=" * 80)
        
        # Step 1: Register User
        print("\n📝 Step 1: Register new user")
        register_data = {
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "full_name": "Test User"
        }
        
        response = requests.post("http://localhost:5000/api/auth/register", json=register_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            access_token = response.json()['access_token']
            print(f"   ✅ Registration successful, got access token")
        else:
            print(f"   ⚠️ Registration failed or user already exists")
            # Try login instead
            login_response = requests.post("http://localhost:5000/api/auth/login", json={
                "email": register_data["email"],
                "password": register_data["password"]
            })
            if login_response.status_code == 200:
                access_token = login_response.json()['access_token']
                print(f"   ✅ Login successful, got access token")
        
        # Step 2: Create Listing via API
        print("\n📝 Step 2: Create listing via API")
        headers = {"Authorization": f"Bearer {access_token}"}
        listing_data = {
            "title": "Solar Panel 300W High Efficiency",
            "price": 150.00,
            "condition": "New",
            "description": "Brand new 300W solar panel with 25-year warranty",
            "category": "Electronics"
        }
        
        response = requests.post("http://localhost:5000/api/listings", json=listing_data, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print(f"   ✅ Listing created successfully")
        
        # Step 3: Get All Listings
        print("\n📝 Step 3: Get all listings from API")
        response = requests.get("http://localhost:5000/api/listings", headers=headers)
        print(f"   Status: {response.status_code}")
        listings_data = response.json()
        listings = listings_data.get('listings', [])
        print(f"   Total listings: {len(listings)}")
        if listings:
            print(f"   First listing: {json.dumps(listings[0], indent=2)}")
        
        # FRONTEND WORKFLOW
        print("\n" + "=" * 80)
        print("FRONTEND WORKFLOW - UI Testing")
        print("=" * 80)
        
        # Step 4: Load Frontend
        print("\n📝 Step 4: Load frontend")
        driver.get("http://localhost:5173")
        time.sleep(3)
        
        save_screenshot_with_ocr(
            driver,
            "workflow_01_frontend_loaded.png",
            ["Marketplace", "Bulk", "Editor"]
        )
        
        # Step 5: Check if page has dark class
        print("\n📝 Step 5: Check current theme")
        html_element = driver.find_element(By.TAG_NAME, "html")
        has_dark_class = "dark" in html_element.get_attribute("class")
        print(f"   Dark mode currently: {'ENABLED' if has_dark_class else 'DISABLED'}")
        
        # Step 6: Open Settings and Toggle Dark Mode
        print("\n📝 Step 6: Open Settings modal")
        settings_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title*='Settings' i]"))
        )
        settings_button.click()
        time.sleep(1)
        
        save_screenshot_with_ocr(
            driver,
            "workflow_02_settings_modal.png",
            ["Settings", "Dark Mode"]
        )
        
        # Step 7: Toggle Dark Mode
        print("\n📝 Step 7: Toggle dark mode")
        # Find the dark mode switch/button
        dark_mode_elements = driver.find_elements(By.CSS_SELECTOR, "button[role='switch']")
        if dark_mode_elements:
            dark_mode_elements[0].click()
            time.sleep(1)
            
            # Verify dark mode is now enabled
            html_element = driver.find_element(By.TAG_NAME, "html")
            has_dark_class_after = "dark" in html_element.get_attribute("class")
            print(f"   Dark mode after toggle: {'ENABLED' if has_dark_class_after else 'DISABLED'}")
            
            save_screenshot_with_ocr(
                driver,
                "workflow_03_dark_mode_toggled.png",
                ["Settings"]
            )
            
            # Close modal
            close_buttons = driver.find_elements(By.CSS_SELECTOR, "button")
            for btn in close_buttons:
                if "×" in btn.text or "Close" in btn.get_attribute("aria-label") or "":
                    try:
                        btn.click()
                        break
                    except:
                        pass
            time.sleep(1)
        
        # Step 8: Final state
        save_screenshot_with_ocr(
            driver,
            "workflow_04_final_state.png",
            ["Marketplace"]
        )
        
        # Console logs
        print("\n" + "=" * 80)
        print("Console Logs")
        print("=" * 80)
        logs = driver.get_log('browser')
        error_count = sum(1 for entry in logs if entry['level'] == 'SEVERE')
        print(f"Total: {len(logs)}, Errors: {error_count}")
        
        print("\n✅ COMPLETE USER WORKFLOW TEST FINISHED")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

