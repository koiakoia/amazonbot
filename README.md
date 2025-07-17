# Amazon Product Scraper v2.0 🚀

A modern, ethical Python package for extracting product data from Amazon with built-in anti-detection measures and multiple export formats.

## ⚠️ Legal Notice

**Important**: This tool is for educational and research purposes only. Always respect Amazon's Terms of Service and implement proper rate limiting. The user is responsible for complying with all applicable laws and website terms of service.

## 🌟 Features

- **Comprehensive Data Extraction**: Product titles, prices, ratings, images, features, and descriptions
- **Anti-Detection Measures**: User agent rotation, random delays, and request retry logic
- **Multiple Export Formats**: CSV, JSON, and Excel support
- **Search Functionality**: Find products by keyword across multiple pages
- **Robust Error Handling**: Comprehensive logging and graceful failure handling
- **Rate Limiting**: Built-in delays to respect server resources
- **Modern Python**: Type hints, clean architecture, and best practices

## 📦 Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd amazon-scraper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper**
   ```bash
   python amazon_scraper.py
   ```

## 🚀 Quick Start

### Basic Usage

```python
from amazon_scraper import AmazonProductScraper

# Initialize the scraper
scraper = AmazonProductScraper(delay_range=(2, 4))

# Search for products
product_urls = scraper.search_products("wireless headphones", pages=1)

# Scrape product data
products = scraper.scrape_multiple_products(product_urls[:5])

# Export to different formats
scraper.export_to_csv(products)
scraper.export_to_json(products)
scraper.export_to_excel(products)
```

### Scrape Single Product

```python
# Scrape a specific product
product_url = "https://www.amazon.com/dp/B08N5WRWNW"
product_data = scraper.scrape_product(product_url)

print(f"Product: {product_data['title']}")
print(f"Price: {product_data['price']}")
print(f"Rating: {product_data['rating']}")
```

## 📊 Data Structure

Each scraped product returns a dictionary with the following fields:

```json
{
    "asin": "B08N5WRWNW",
    "url": "https://www.amazon.com/dp/B08N5WRWNW",
    "title": "Product Title",
    "price": "$99.99",
    "rating": "4.5",
    "rating_count": "1,234 ratings",
    "availability": "In Stock",
    "images": ["https://image1.jpg", "https://image2.jpg"],
    "features": ["Feature 1", "Feature 2"],
    "description": "Product description...",
    "scraped_at": "2025-01-08T10:30:00"
}
```

## ⚙️ Configuration Options

### Scraper Initialization

```python
scraper = AmazonProductScraper(
    delay_range=(1, 3),    # Random delay between requests (seconds)
    max_retries=3          # Maximum retries for failed requests
)
```

### Search Parameters

```python
product_urls = scraper.search_products(
    keyword="laptop",      # Search term
    pages=2               # Number of search result pages to scrape
)
```

## 📈 Export Options

### CSV Export
```python
scraper.export_to_csv(products, filename="my_products.csv")
```

### JSON Export
```python
scraper.export_to_json(products, filename="my_products.json")
```

### Excel Export
```python
scraper.export_to_excel(products, filename="my_products.xlsx")
```

## 🛡️ Best Practices

### 1. Respect Rate Limits
- Use appropriate delays between requests (2-5 seconds recommended)
- Don't overwhelm Amazon's servers with too many concurrent requests

### 2. Legal Compliance
- Only scrape publicly available data
- Respect Amazon's robots.txt file
- Don't scrape personal or sensitive information
- Consider using Amazon's official API for commercial use

### 3. Error Handling
- Monitor the logs for blocked requests or errors
- Implement proper retry logic for failed requests
- Handle CAPTCHA challenges gracefully

### 4. Data Management
- Regularly backup your scraped data
- Validate data quality and completeness
- Implement data deduplication if needed

## 🔧 Advanced Usage

### Custom User Agents
The scraper automatically rotates between multiple user agents, but you can customize them:

```python
scraper.user_agents = [
    'Your-Custom-User-Agent-1',
    'Your-Custom-User-Agent-2'
]
```

### Logging Configuration
Monitor scraper activity with detailed logging:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 🚨 Troubleshooting

### Common Issues

1. **Getting blocked by Amazon**
   - Increase delay between requests
   - Use residential proxies
   - Reduce scraping frequency

2. **Empty or missing data**
   - Amazon may have changed their HTML structure
   - Check the logs for parsing errors
   - Update CSS selectors if needed

3. **CAPTCHA challenges**
   - Reduce request frequency
   - Use different IP addresses
   - Implement CAPTCHA solving services

### Error Codes

- **503 Service Unavailable**: Amazon is temporarily blocking requests
- **CAPTCHA detected**: Anti-bot measures triggered
- **Connection timeout**: Network or server issues

## 📋 Requirements

- Python 3.7+
- Internet connection
- Required packages (see `requirements.txt`)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for:

- Complying with Amazon's Terms of Service
- Respecting rate limits and server resources
- Following applicable laws and regulations
- Using the tool ethically and responsibly

The developers of this tool are not responsible for any misuse or legal issues arising from its use.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed correctly
4. Consider the legal and ethical implications of your use case

## 🔄 Updates

### Version 2.0 (2025)
- Complete rewrite with modern Python practices
- Enhanced anti-detection measures
- Multiple export formats
- Improved error handling and logging
- Better data extraction accuracy
- Rate limiting and ethical scraping practices

---

**Remember**: Always scrape responsibly and ethically! 🌟