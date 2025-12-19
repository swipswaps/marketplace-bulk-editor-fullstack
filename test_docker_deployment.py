#!/usr/bin/env python3
"""
Selenium test for Marketplace Bulk Editor Docker deployment
Tests frontend UI and captures console logs + screenshots
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_marketplace_editor():
    """Test the Marketplace Bulk Editor frontend"""
    
    # Setup Chrome with console logging
    options = Options()
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    # Run in visible mode for debugging
    # options.add_argument('--headless')  # Commented out per Rule 7
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        print("=" * 80)
        print("SELENIUM TEST: Marketplace Bulk Editor Docker Deployment")
        print("=" * 80)
        print()
        
        # Initialize driver
        print("🌐 Starting Chrome browser...")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        
        # Test frontend
        url = "http://localhost:5173"
        print(f"📍 Navigating to: {url}")
        driver.get(url)
        
        # Wait for page load
        print("⏳ Waiting for page to load...")
        time.sleep(3)
        
        # Take screenshot 1: Initial page load
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot1 = f"screenshot_backend_status_initial_{timestamp}.png"
        driver.save_screenshot(screenshot1)
        print(f"📸 Screenshot saved: {screenshot1}")
        
        # Get page title
        title = driver.title
        print(f"📄 Page title: {title}")
        
        # Get page source (first 500 chars)
        page_source = driver.page_source[:500]
        print(f"📝 Page source (first 500 chars):\n{page_source}")
        print()
        
        # Capture console logs
        print("=" * 80)
        print("CONSOLE LOGS")
        print("=" * 80)
        logs = driver.get_log('browser')
        if logs:
            for entry in logs:
                timestamp = entry.get('timestamp', 'N/A')
                level = entry.get('level', 'N/A')
                message = entry.get('message', 'N/A')
                print(f"[{level}] {message}")
        else:
            print("No console logs captured")
        print()
        
        # Check for specific elements
        print("=" * 80)
        print("UI ELEMENT CHECKS")
        print("=" * 80)
        
        # Wait for React app to render
        time.sleep(2)
        
        # Take screenshot 2: After React render
        screenshot2 = f"screenshot_backend_status_rendered_{timestamp}.png"
        driver.save_screenshot(screenshot2)
        print(f"📸 Screenshot saved: {screenshot2}")
        
        # Check for common elements
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            print(f"✅ Body element found")
            print(f"   Body text (first 200 chars): {body.text[:200]}")
        except Exception as e:
            print(f"❌ Body element not found: {e}")
        
        # Check for root div
        try:
            root = driver.find_element(By.ID, "root")
            print(f"✅ Root div found")
        except Exception as e:
            print(f"❌ Root div not found: {e}")
        
        # Get final console logs
        print()
        print("=" * 80)
        print("FINAL CONSOLE LOGS")
        print("=" * 80)
        final_logs = driver.get_log('browser')
        if final_logs:
            for entry in final_logs:
                level = entry.get('level', 'N/A')
                message = entry.get('message', 'N/A')
                print(f"[{level}] {message}")
        else:
            print("No additional console logs")
        
        # Take final screenshot
        screenshot3 = f"screenshot_backend_status_final_{timestamp}.png"
        driver.save_screenshot(screenshot3)
        print(f"📸 Final screenshot saved: {screenshot3}")
        
        print()
        print("=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        print(f"✅ Frontend accessible at {url}")
        print(f"📸 Screenshots: {screenshot1}, {screenshot2}, {screenshot3}")
        print()
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        if driver:
            error_screenshot = f"screenshot_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(error_screenshot)
            print(f"📸 Error screenshot saved: {error_screenshot}")
        raise
    finally:
        if driver:
            print("🛑 Closing browser...")
            driver.quit()

if __name__ == "__main__":
    test_marketplace_editor()

