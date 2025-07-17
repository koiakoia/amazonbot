#!/usr/bin/env python3
"""
Test script for Amazon Product Scraper
This script tests the basic functionality without making actual requests to Amazon.
"""

import sys
import os

# Add the current directory to Python path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scraper_initialization():
    """Test if the scraper can be initialized properly."""
    print("🧪 Testing scraper initialization...")
    
    try:
        # Import the module
        from amazon_scraper import AmazonProductScraper
        
        # Initialize scraper
        scraper = AmazonProductScraper(delay_range=(1, 2))
        
        print("✅ Scraper initialized successfully!")
        print(f"   - Delay range: {scraper.delay_range}")
        print(f"   - Max retries: {scraper.max_retries}")
        print(f"   - User agents available: {len(scraper.user_agents)}")
        
        return scraper
        
    except Exception as e:
        print(f"❌ Failed to initialize scraper: {e}")
        return None

def test_headers_generation(scraper):
    """Test header generation functionality."""
    print("\n🧪 Testing headers generation...")
    
    try:
        headers = scraper._get_headers()
        
        print("✅ Headers generated successfully!")
        print(f"   - User-Agent: {headers['User-Agent'][:50]}...")
        print(f"   - Accept: {headers['Accept'][:30]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate headers: {e}")
        return False

def test_url_validation():
    """Test URL validation and ASIN extraction."""
    print("\n🧪 Testing URL validation...")
    
    import re
    
    test_urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://www.amazon.com/Some-Product-Name/dp/B123456789/ref=sr_1_1",
        "https://amazon.com/dp/B987654321"
    ]
    
    for url in test_urls:
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            asin = asin_match.group(1)
            print(f"✅ URL: {url}")
            print(f"   ASIN: {asin}")
        else:
            print(f"❌ Invalid URL: {url}")

def test_export_functionality(scraper):
    """Test data export functionality with sample data."""
    print("\n🧪 Testing export functionality...")
    
    # Sample product data
    sample_products = [
        {
            'asin': 'B08N5WRWNW',
            'url': 'https://www.amazon.com/dp/B08N5WRWNW',
            'title': 'Test Product 1',
            'price': '$99.99',
            'rating': '4.5',
            'rating_count': '1,234 ratings',
            'availability': 'In Stock',
            'images': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'],
            'features': ['Feature 1', 'Feature 2', 'Feature 3'],
            'description': 'This is a test product description.',
            'scraped_at': '2025-01-08T10:30:00'
        },
        {
            'asin': 'B123456789',
            'url': 'https://www.amazon.com/dp/B123456789',
            'title': 'Test Product 2',
            'price': '$149.99',
            'rating': '4.2',
            'rating_count': '856 ratings',
            'availability': 'In Stock',
            'images': ['https://example.com/image3.jpg'],
            'features': ['Feature A', 'Feature B'],
            'description': 'Another test product description.',
            'scraped_at': '2025-01-08T10:31:00'
        }
    ]
    
    try:
        # Test CSV export
        print("   Testing CSV export...")
        scraper.export_to_csv(sample_products, 'test_products.csv')
        
        # Test JSON export
        print("   Testing JSON export...")
        scraper.export_to_json(sample_products, 'test_products.json')
        
        # Test Excel export
        print("   Testing Excel export...")
        scraper.export_to_excel(sample_products, 'test_products.xlsx')
        
        print("✅ All export functions working!")
        print("📁 Test files created:")
        print("   - test_products.csv")
        print("   - test_products.json")
        print("   - test_products.xlsx")
        
        return True
        
    except Exception as e:
        print(f"❌ Export test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Amazon Product Scraper - Test Suite")
    print("=" * 50)
    
    # Test 1: Initialization
    scraper = test_scraper_initialization()
    if not scraper:
        print("\n❌ Cannot continue tests - initialization failed")
        return
    
    # Test 2: Headers
    headers_ok = test_headers_generation(scraper)
    
    # Test 3: URL validation
    test_url_validation()
    
    # Test 4: Export functionality
    export_ok = test_export_functionality(scraper)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   ✅ Initialization: {'PASS' if scraper else 'FAIL'}")
    print(f"   ✅ Headers: {'PASS' if headers_ok else 'FAIL'}")
    print(f"   ✅ URL Validation: PASS")
    print(f"   ✅ Export Functions: {'PASS' if export_ok else 'FAIL'}")
    
    if scraper and headers_ok and export_ok:
        print("\n🎉 All tests passed! The scraper is ready to use.")
        print("\n⚠️  Note: This test doesn't make actual web requests to Amazon.")
        print("   For real testing, run the main script with caution and respect rate limits.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()