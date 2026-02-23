#!/usr/bin/env python3
"""
Test script to verify serblabs.in integration
This script tests the scraper functionality with serblabs.in
"""

import sys
from scraper import ResponseSheetScraper

def test_serblabs_connection():
    """Test connection to serblabs.in"""
    print("=" * 60)
    print("Testing serblabs.in Integration")
    print("=" * 60)
    
    # Test URL (replace with an actual response sheet URL for testing)
    test_url = input("\nEnter a GATE response sheet URL to test: ").strip()
    
    if not test_url:
        print("❌ No URL provided. Using a dummy URL for connection test...")
        test_url = "https://example.com/dummy-response-sheet"
    
    print(f"\n📋 Response Sheet URL: {test_url}")
    print(f"🌐 Target Website: https://serblabs.in/")
    print("\n" + "-" * 60)
    
    try:
        print("\n🔄 Initializing scraper...")
        scraper = ResponseSheetScraper(test_url, timeout=30)
        
        print("✅ Scraper initialized successfully")
        print(f"   - Response Sheet URL: {scraper.response_sheet_url}")
        print(f"   - Target Website: {scraper.target_website}")
        
        print("\n🔄 Validating URL format...")
        if scraper.validate_url():
            print("✅ URL format is valid")
        else:
            print("❌ Invalid URL format")
            return False
        
        print("\n🔄 Fetching serblabs.in homepage...")
        homepage = scraper.get_serblabs_page()
        print(f"✅ Successfully fetched homepage ({len(homepage)} bytes)")
        print(f"   First 200 characters: {homepage[:200]}...")
        
        print("\n🔄 Submitting URL to serblabs.in...")
        result_html = scraper.submit_to_serblabs()
        print(f"✅ Submission successful ({len(result_html)} bytes)")
        print(f"   First 300 characters of result: {result_html[:300]}...")
        
        print("\n🔄 Parsing result from serblabs.in...")
        result_data = scraper.parse_serblabs_result(result_html)
        
        print("\n" + "=" * 60)
        print("RESULT DATA:")
        print("=" * 60)
        
        if result_data.get('predicted_marks') is not None:
            print(f"\n✅ Predicted Marks: {result_data['predicted_marks']}")
        else:
            print("\n⚠️  No predicted marks found in the result")
            print("    Raw result preview:")
            print(f"    {result_data.get('raw_result', 'N/A')[:500]}")
        
        print(f"\n📊 Statistics:")
        print(f"   - Total Questions: {result_data.get('statistics', {}).get('total_questions', 0)}")
        print(f"   - Attempted: {result_data.get('statistics', {}).get('attempted', 0)}")
        print(f"   - Not Attempted: {result_data.get('statistics', {}).get('not_attempted', 0)}")
        
        if result_data.get('questions'):
            print(f"\n📝 Found {len(result_data['questions'])} question responses")
            print("   First 5 questions:")
            for q in result_data['questions'][:5]:
                print(f"   - Q{q.get('number')}: {q.get('response')} ({q.get('status', 'N/A')})")
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Error occurred during testing:")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print(f"Type: {type(e).__name__}")
        
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        
        return False

def main():
    """Main function"""
    print("\n🧪 GATE Predictor - serblabs.in Integration Test\n")
    
    success = test_serblabs_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Tests failed. Please check the errors above.")
    print("=" * 60 + "\n")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
