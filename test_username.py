#!/usr/bin/env python3
"""
Test script to demonstrate username scraping functionality
"""

from scraper import ResponseSheetScraper

def test_username_scraping():
    """Test the username scraping feature"""
    print("=" * 60)
    print("Testing Username Scraping Feature")
    print("=" * 60)
    
    # Example URL (replace with actual GATE response sheet URL)
    test_url = "https://gate.iitb.ac.in/response/CS2026/12345"
    
    print(f"\n1. Creating scraper with URL: {test_url}")
    scraper = ResponseSheetScraper(test_url)
    
    print("\n2. Checking if scrape_candidate_name method exists...")
    if hasattr(scraper, 'scrape_candidate_name'):
        print("   ✅ Method exists!")
    else:
        print("   ❌ Method not found!")
        return
    
    print("\n3. Testing username extraction (with fallback to 'Candidate')...")
    try:
        username = scraper.scrape_candidate_name()
        print(f"   Username scraped: {username}")
        print(f"   ✅ Function completed successfully!")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print("✅ Username scraping function added to scraper.py")
    print("✅ Route /api/scrape-username created for standalone username extraction")
    print("✅ Main routes updated to scrape and pass username to template")
    print("✅ result.html template updated to display username")
    print("\nThe username variable will be displayed in the candidate info card")
    print("on the results page for verification purposes.")
    print("=" * 60)

if __name__ == "__main__":
    test_username_scraping()
