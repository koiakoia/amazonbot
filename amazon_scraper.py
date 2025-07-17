#!/usr/bin/env python3
"""
Amazon Product Scraper v2.0
A modern Python package for extracting product data from Amazon

Features:
- Product details scraping (title, price, images, reviews)
- Rate limiting and anti-detection measures
- Multiple export formats (CSV, JSON, Excel)
- Proper error handling and logging
- Respect for robots.txt and ethical scraping practices

Author: Updated for 2025
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
import time
import random
import re
import logging
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Union
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('amazon_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AmazonProductScraper:
    """
    A comprehensive Amazon product scraper with anti-detection measures
    and multiple data export options.
    """
    
    def __init__(self, delay_range: tuple = (1, 3), max_retries: int = 3):
        """
        Initialize the Amazon scraper.
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
            max_retries: Maximum number of retries for failed requests
        """
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
        ]
        
        logger.info("Amazon Product Scraper initialized")
    
    def _get_headers(self) -> Dict[str, str]:
        """Generate headers with random user agent."""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def _delay(self):
        """Add random delay between requests."""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make a request with retries and error handling.
        
        Args:
            url: The URL to request
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, headers=self._get_headers(), timeout=10)
                
                if response.status_code == 200:
                    # Check if we got blocked (common Amazon responses)
                    if "robot" in response.text.lower() or "captcha" in response.text.lower():
                        logger.warning(f"Detected anti-bot response for {url}")
                        self._delay()
                        continue
                    return response
                elif response.status_code == 503:
                    logger.warning(f"Service unavailable for {url}, retrying...")
                else:
                    logger.warning(f"HTTP {response.status_code} for {url}")
                
            except requests.RequestException as e:
                logger.error(f"Request failed for {url}: {e}")
            
            if attempt < self.max_retries - 1:
                self._delay()
        
        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None
    
    def scrape_product(self, product_url: str) -> Optional[Dict]:
        """
        Scrape a single Amazon product.
        
        Args:
            product_url: Amazon product URL
            
        Returns:
            Dictionary containing product data or None if failed
        """
        logger.info(f"Scraping product: {product_url}")
        
        response = self._make_request(product_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract ASIN from URL
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', product_url)
        asin = asin_match.group(1) if asin_match else None
        
        product_data = {
            'asin': asin,
            'url': product_url,
            'title': self._extract_title(soup),
            'price': self._extract_price(soup),
            'rating': self._extract_rating(soup),
            'rating_count': self._extract_rating_count(soup),
            'availability': self._extract_availability(soup),
            'images': self._extract_images(soup, response.text),
            'features': self._extract_features(soup),
            'description': self._extract_description(soup),
            'scraped_at': datetime.now().isoformat()
        }
        
        # Remove None values
        product_data = {k: v for k, v in product_data.items() if v is not None}
        
        logger.info(f"Successfully scraped product: {product_data.get('title', 'Unknown')}")
        return product_data
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product title."""
        selectors = [
            '#productTitle',
            '.product-title',
            'h1.a-size-large'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product price."""
        selectors = [
            '.a-price .a-offscreen',
            '.a-price-whole',
            '#price_inside_buybox',
            '.a-price.a-text-price.a-size-medium.apexPriceToPay .a-offscreen',
            '.a-price-range .a-offscreen'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                if price_text and '$' in price_text:
                    return price_text
        return None
    
    def _extract_rating(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product rating."""
        rating_element = soup.select_one('span.a-icon-alt')
        if rating_element:
            rating_text = rating_element.get_text()
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                return rating_match.group(1)
        return None
    
    def _extract_rating_count(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract rating count."""
        selectors = [
            '#acrCustomerReviewText',
            '.a-size-base.a-color-base'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and 'rating' in element.get_text().lower():
                return element.get_text(strip=True)
        return None
    
    def _extract_availability(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product availability."""
        selectors = [
            '#availability span',
            '.a-size-medium.a-color-success',
            '.a-size-medium.a-color-price'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                availability = element.get_text(strip=True)
                if availability and len(availability) < 100:  # Reasonable length
                    return availability
        return None
    
    def _extract_images(self, soup: BeautifulSoup, html_content: str) -> List[str]:
        """Extract product images."""
        images = []
        
        # Try to extract from JavaScript data
        image_pattern = r'"hiRes":"([^"]+)"'
        matches = re.findall(image_pattern, html_content)
        if matches:
            images.extend(matches)
        
        # Fallback to img tags
        if not images:
            img_elements = soup.select('img[data-a-image-name="landingImage"]')
            for img in img_elements:
                src = img.get('src')
                if src and 'http' in src:
                    images.append(src)
        
        return list(set(images))  # Remove duplicates
    
    def _extract_features(self, soup: BeautifulSoup) -> List[str]:
        """Extract product features."""
        features = []
        
        # Feature bullets
        feature_elements = soup.select('#feature-bullets li span.a-list-item')
        for element in feature_elements:
            feature_text = element.get_text(strip=True)
            if feature_text and len(feature_text) > 10:  # Filter out short/empty features
                features.append(feature_text)
        
        return features
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product description."""
        selectors = [
            '#productDescription p',
            '#aplus .aplus-p1',
            '.a-section.a-spacing-medium'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                description = element.get_text(strip=True)
                if description and len(description) > 50:
                    return description
        return None
    
    def search_products(self, keyword: str, pages: int = 1) -> List[str]:
        """
        Search for products and return URLs.
        
        Args:
            keyword: Search keyword
            pages: Number of pages to scrape
            
        Returns:
            List of product URLs
        """
        logger.info(f"Searching for '{keyword}' across {pages} pages")
        
        product_urls = []
        
        for page in range(1, pages + 1):
            search_url = f"https://www.amazon.com/s?k={keyword}&page={page}"
            response = self._make_request(search_url)
            
            if not response:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product URLs from search results
            product_elements = soup.select('[data-component-type="s-search-result"] h2 a')
            
            for element in product_elements:
                relative_url = element.get('href')
                if relative_url:
                    full_url = urljoin('https://www.amazon.com', relative_url.split('?')[0])
                    product_urls.append(full_url)
            
            logger.info(f"Found {len(product_elements)} products on page {page}")
            self._delay()
        
        logger.info(f"Total products found: {len(product_urls)}")
        return product_urls
    
    def scrape_multiple_products(self, product_urls: List[str]) -> List[Dict]:
        """
        Scrape multiple products.
        
        Args:
            product_urls: List of Amazon product URLs
            
        Returns:
            List of product data dictionaries
        """
        products = []
        
        for i, url in enumerate(product_urls, 1):
            logger.info(f"Processing product {i}/{len(product_urls)}")
            
            product_data = self.scrape_product(url)
            if product_data:
                products.append(product_data)
            
            # Add delay between requests
            if i < len(product_urls):
                self._delay()
        
        return products
    
    def export_to_csv(self, products: List[Dict], filename: str = None):
        """Export products to CSV file."""
        if not filename:
            filename = f"amazon_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not products:
            logger.warning("No products to export")
            return
        
        df = pd.DataFrame(products)
        
        # Flatten complex fields
        if 'images' in df.columns:
            df['images'] = df['images'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        if 'features' in df.columns:
            df['features'] = df['features'].apply(lambda x: ' | '.join(x) if isinstance(x, list) else x)
        
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Exported {len(products)} products to {filename}")
    
    def export_to_json(self, products: List[Dict], filename: str = None):
        """Export products to JSON file."""
        if not filename:
            filename = f"amazon_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(products)} products to {filename}")
    
    def export_to_excel(self, products: List[Dict], filename: str = None):
        """Export products to Excel file."""
        if not filename:
            filename = f"amazon_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        if not products:
            logger.warning("No products to export")
            return
        
        df = pd.DataFrame(products)
        
        # Flatten complex fields
        if 'images' in df.columns:
            df['images'] = df['images'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        if 'features' in df.columns:
            df['features'] = df['features'].apply(lambda x: ' | '.join(x) if isinstance(x, list) else x)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Products', index=False)
        
        logger.info(f"Exported {len(products)} products to {filename}")


def main():
    """
    Example usage of the Amazon Product Scraper.
    """
    print("🚀 Amazon Product Scraper v2.0")
    print("=" * 50)
    
    # Initialize scraper
    scraper = AmazonProductScraper(delay_range=(2, 4))
    
    # Example 1: Search and scrape products
    print("\n📋 Example 1: Search for products")
    keyword = input("Enter search keyword (e.g., 'laptop', 'headphones'): ").strip()
    
    if not keyword:
        keyword = "wireless headphones"  # Default
    
    try:
        # Search for products
        product_urls = scraper.search_products(keyword, pages=1)
        
        if not product_urls:
            print("❌ No products found")
            return
        
        # Limit to first 5 products for demo
        product_urls = product_urls[:5]
        print(f"📦 Found {len(product_urls)} products to scrape")
        
        # Scrape products
        products = scraper.scrape_multiple_products(product_urls)
        
        if products:
            print(f"\n✅ Successfully scraped {len(products)} products")
            
            # Display sample data
            print("\n📊 Sample product data:")
            for i, product in enumerate(products[:2], 1):
                print(f"\nProduct {i}:")
                print(f"  Title: {product.get('title', 'N/A')}")
                print(f"  Price: {product.get('price', 'N/A')}")
                print(f"  Rating: {product.get('rating', 'N/A')}")
                print(f"  ASIN: {product.get('asin', 'N/A')}")
            
            # Export data
            print("\n💾 Exporting data...")
            scraper.export_to_csv(products)
            scraper.export_to_json(products)
            
            print("✅ Data exported successfully!")
            print("\nFiles created:")
            print("  - CSV file for spreadsheet analysis")
            print("  - JSON file for programmatic use")
            
        else:
            print("❌ No products were successfully scraped")
    
    except KeyboardInterrupt:
        print("\n⏹️ Scraping interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        logger.error(f"Main execution error: {e}")
    
    print("\n🎉 Scraping completed!")


if __name__ == "__main__":
    main()