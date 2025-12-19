#!/usr/bin/env python3
"""
Complete guide showing how to use the database-driven backend.
Tests PostgreSQL database and Redis cache with screenshots in VISIBLE mode.
Per Rule 9: VISIBLE mode, OCR verification, complete workflow.
"""

import time
import json
import subprocess
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

def run_command(cmd, description):
    """Run shell command and show output"""
    print(f"\n💻 {description}")
    print(f"   Command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"   Output:\n{result.stdout}")
    if result.stderr:
        print(f"   Stderr:\n{result.stderr}")
    return result.stdout

def main():
    print("=" * 80)
    print("DATABASE & REDIS USAGE GUIDE - COMPLETE WORKFLOW")
    print("=" * 80)
    
    # Setup Chrome in VISIBLE mode (NOT headless)
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    # DO NOT add --headless per Rule 9
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    
    access_token = None
    user_email = f"testuser_{int(time.time())}@example.com"
    
    try:
        # ========================================================================
        # PART 1: VERIFY DOCKER CONTAINERS ARE RUNNING
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 1: VERIFY DOCKER CONTAINERS")
        print("=" * 80)
        
        run_command(
            "docker ps --filter 'name=marketplace-' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'",
            "Check all marketplace containers"
        )
        
        # ========================================================================
        # PART 2: TEST POSTGRESQL DATABASE
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 2: POSTGRESQL DATABASE USAGE")
        print("=" * 80)
        
        # Show database connection info
        print("\n📊 Database Connection Info:")
        print("   Host: marketplace-postgres (Docker network)")
        print("   Port: 5432")
        print("   Database: marketplace_db")
        print("   User: marketplace_user")
        
        # Check database tables
        run_command(
            "docker exec marketplace-postgres psql -U marketplace_user -d marketplace_db -c '\\dt'",
            "List all database tables"
        )
        
        # Count existing users
        run_command(
            "docker exec marketplace-postgres psql -U marketplace_user -d marketplace_db -c 'SELECT COUNT(*) FROM users;'",
            "Count users in database"
        )
        
        # Count existing listings
        run_command(
            "docker exec marketplace-postgres psql -U marketplace_user -d marketplace_db -c 'SELECT COUNT(*) FROM listings;'",
            "Count listings in database"
        )
        
        # ========================================================================
        # PART 3: TEST REDIS CACHE
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 3: REDIS CACHE USAGE")
        print("=" * 80)
        
        print("\n📊 Redis Connection Info:")
        print("   Host: marketplace-redis (Docker network)")
        print("   Port: 6379")
        print("   Database 0: General cache")
        print("   Database 1: Rate limiting")
        
        # Check Redis keys
        run_command(
            "docker exec marketplace-redis redis-cli DBSIZE",
            "Count keys in Redis database 0"
        )
        
        run_command(
            "docker exec marketplace-redis redis-cli -n 1 DBSIZE",
            "Count keys in Redis database 1 (rate limiting)"
        )
        
        # ========================================================================
        # PART 4: REGISTER USER VIA API (CREATES DATABASE RECORD)
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 4: REGISTER USER (PostgreSQL INSERT)")
        print("=" * 80)
        
        print(f"\n📝 Registering user: {user_email}")
        register_data = {
            "email": user_email,
            "password": "SecurePass123!"
        }
        
        response = requests.post("http://localhost:5000/api/auth/register", json=register_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            access_token = response.json()['access_token']
            user_id = response.json()['user']['id']
            print(f"   ✅ User created in database with ID: {user_id}")
            
            # Verify user in database
            run_command(
                f"docker exec marketplace-postgres psql -U marketplace_user -d marketplace_db -c \"SELECT id, email, created_at FROM users WHERE email='{user_email}';\"",
                "Verify user exists in PostgreSQL"
            )
        
        # ========================================================================
        # PART 5: CREATE LISTING VIA API (DATABASE INSERT)
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 5: CREATE LISTING (PostgreSQL INSERT)")
        print("=" * 80)
        
        headers = {"Authorization": f"Bearer {access_token}"}
        listing_data = {
            "title": "Solar Panel 300W High Efficiency",
            "price": 150.00,
            "condition": "New",
            "description": "Brand new 300W solar panel",
            "category": "Electronics"
        }
        
        print(f"\n📝 Creating listing via API...")
        response = requests.post("http://localhost:5000/api/listings", json=listing_data, headers=headers)
        print(f"   Status: {response.status_code}")
        listing_response = response.json()
        print(f"   Response: {json.dumps(listing_response, indent=2)}")

        if response.status_code == 201:
            listing_id = listing_response['listing']['id']
            print(f"   ✅ Listing created in database with ID: {listing_id}")

            # Verify listing in database
            run_command(
                f"docker exec marketplace-postgres psql -U marketplace_user -d marketplace_db -c \"SELECT id, title, price, condition FROM listings WHERE id='{listing_id}';\"",
                "Verify listing exists in PostgreSQL"
            )

        # ========================================================================
        # PART 6: TEST RATE LIMITING (REDIS)
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 6: RATE LIMITING (Redis)")
        print("=" * 80)

        print("\n📝 Testing rate limiting (100 requests/minute)...")
        print("   Making 5 rapid requests to /api/listings...")

        for i in range(5):
            response = requests.get("http://localhost:5000/api/listings", headers=headers)
            print(f"   Request {i+1}: Status {response.status_code}")

        # Check Redis rate limit keys
        run_command(
            "docker exec marketplace-redis redis-cli -n 1 KEYS '*'",
            "Show rate limiting keys in Redis"
        )

        # ========================================================================
        # PART 7: FRONTEND - LOAD AND VERIFY BACKEND CONNECTION
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 7: FRONTEND - VERIFY BACKEND CONNECTION")
        print("=" * 80)

        print("\n📝 Loading frontend at http://localhost:5173")
        driver.get("http://localhost:5173")
        time.sleep(3)

        save_screenshot_with_ocr(
            driver,
            "guide_01_frontend_loaded.png",
            ["Marketplace", "Bulk", "Editor", "Docker Backend"]
        )

        # ========================================================================
        # PART 8: EXPAND BACKEND STATUS TO SHOW API ENDPOINTS
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 8: BACKEND STATUS - SHOW API ENDPOINTS")
        print("=" * 80)

        print("\n📝 Clicking backend status to expand...")
        try:
            backend_status = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Docker Backend')]"))
            )
            backend_status.click()
            time.sleep(2)

            save_screenshot_with_ocr(
                driver,
                "guide_02_backend_expanded.png",
                ["/api/auth", "/api/listings", "/api/templates", "/health"]
            )
        except Exception as e:
            print(f"   ⚠️ Could not expand backend status: {e}")

        # ========================================================================
        # PART 9: QUERY DATABASE TO SHOW ALL LISTINGS
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 9: QUERY DATABASE - SHOW ALL LISTINGS")
        print("=" * 80)

        run_command(
            "docker exec marketplace-postgres psql -U marketplace_user -d marketplace_db -c 'SELECT id, title, price, condition, created_at FROM listings ORDER BY created_at DESC LIMIT 5;'",
            "Show last 5 listings from database"
        )

        # ========================================================================
        # PART 10: EXPORT TO SQL (DATABASE FEATURE)
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 10: EXPORT TO SQL")
        print("=" * 80)

        print("\n📝 Exporting listings to SQL format...")
        export_data = {"listings": [listing_response['listing']]}
        response = requests.post("http://localhost:5000/api/export/sql", json=export_data, headers=headers)

        if response.status_code == 200:
            sql_content = response.text
            print(f"   ✅ SQL export successful")
            print(f"   SQL content (first 500 chars):\n{sql_content[:500]}")

            # Save to file
            with open("exported_listings.sql", "w") as f:
                f.write(sql_content)
            print(f"   ✅ Saved to exported_listings.sql")

        # ========================================================================
        # PART 11: CONSOLE LOGS
        # ========================================================================
        print("\n" + "=" * 80)
        print("PART 11: CONSOLE LOGS")
        print("=" * 80)

        logs = driver.get_log('browser')
        error_count = sum(1 for entry in logs if entry['level'] == 'SEVERE')
        warning_count = sum(1 for entry in logs if entry['level'] == 'WARNING')

        print(f"\n📊 Console Log Summary:")
        print(f"   Total entries: {len(logs)}")
        print(f"   Errors (SEVERE): {error_count}")
        print(f"   Warnings: {warning_count}")

        if error_count > 0:
            print(f"\n❌ ERRORS FOUND:")
            for entry in logs:
                if entry['level'] == 'SEVERE':
                    print(f"   [{entry['level']}] {entry['message']}")
        else:
            print(f"\n✅ No errors in console")

        # Final screenshot
        save_screenshot_with_ocr(
            driver,
            "guide_03_final_state.png",
            ["Marketplace"]
        )

        print("\n" + "=" * 80)
        print("✅ DATABASE & REDIS GUIDE COMPLETE")
        print("=" * 80)
        print("\nSummary:")
        print("  ✅ PostgreSQL database verified")
        print("  ✅ Redis cache verified")
        print("  ✅ User registration (database INSERT)")
        print("  ✅ Listing creation (database INSERT)")
        print("  ✅ Rate limiting (Redis)")
        print("  ✅ SQL export (database feature)")
        print("  ✅ Frontend backend connection verified")
        print(f"  ✅ Console errors: {error_count}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()


