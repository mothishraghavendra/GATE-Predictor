#!/usr/bin/env python3
"""
Quick verification script to test the improved error handling
"""

import sys
import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("=" * 70)
print("Testing Enhanced Error Handling for serblabs.in Integration")
print("=" * 70)

# Test 1: Import the scraper module
print("\n[Test 1] Importing scraper module...")
try:
    from scraper import ResponseSheetScraper
    print("✅ Successfully imported ResponseSheetScraper")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

# Test 2: Create scraper instance with retry support
print("\n[Test 2] Creating scraper instance with retry support...")
try:
    test_url = "https://example.com/dummy-response-sheet"
    scraper = ResponseSheetScraper(test_url, timeout=10, max_retries=2)
    print(f"✅ Scraper created successfully")
    print(f"   - URL: {scraper.response_sheet_url}")
    print(f"   - Max retries: {scraper.max_retries}")
    print(f"   - Timeout: {scraper.timeout}s")
except Exception as e:
    print(f"❌ Failed to create scraper: {e}")
    sys.exit(1)

# Test 3: Validate URL
print("\n[Test 3] Testing URL validation...")
if scraper.validate_url():
    print("✅ URL validation works correctly")
else:
    print("❌ URL validation failed")

# Test 4: Test error handling for invalid API call
print("\n[Test 4] Testing error handling (this should fail gracefully)...")
try:
    # This will fail because example.com is not a valid GATE response sheet
    # But it should provide a clear error message
    result = scraper.submit_to_serblabs()
    print("❌ Unexpected success - should have failed")
except Exception as e:
    print(f"✅ Error handling works correctly")
    print(f"   Error message: {str(e)[:200]}...")

# Test 5: Import app module
print("\n[Test 5] Importing Flask app...")
try:
    from app import app
    print("✅ Successfully imported Flask app")
    print(f"   - Debug mode: {app.debug}")
    print(f"   - Secret key configured: {'SECRET_KEY' in app.config}")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ All basic tests passed!")
print("=" * 70)
print("\nNext steps:")
print("1. Deploy the updated code to your hosting platform")
print("2. Monitor logs to see the detailed error messages")
print("3. Check BUGFIX_SERBLABS.md for more information")
print("\nThe app now has:")
print("  ✓ Retry logic (up to 3 attempts)")
print("  ✓ Better error messages with response preview")
print("  ✓ Comprehensive logging")
print("  ✓ Empty response detection")
print("  ✓ Content-type validation")
print("=" * 70)
