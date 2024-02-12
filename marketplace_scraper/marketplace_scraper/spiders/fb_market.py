"""
This is the 2nd scraper of the project.
This scraper will scrape facebook marketplace with given keywords and return a csv file containing
Listing_url, Listing_title, Listing_price, Listing_location
I am testing this script using splinter
Author: Muhammad Owais
Dated: 05-Feb-24
"""

import scrapy
import time
from typing import Any, Iterable
from scrapy.http import HtmlResponse, Request, Response
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from marketplace_scraper.items import FacebookMarketplaceItem


class FacebookMarketSpider(Spider):
    name = 'fb_market'
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["Listing_Title", "Listing_Location", "Listing_Price_CAD", "Mileage_KM", "Listing_Url"]
    }
    start_urls = []

    
    def __init__(self, year=None, make=None, model=None, city=None, keyword_1='', keyword_2='', *args, **kwargs):
        super(FacebookMarketSpider, self).__init__(*args, **kwargs)

        self.year = year
        self.make = make
        self.model = model
        self.city = city
        self.keyword_1 = keyword_1
        self.keyword_2 = keyword_2

    def start_requests(self):
        url = f"https://web.facebook.com/marketplace/{self.city}/search?sortBy=creation_time_descend&query={self.year}%20{self.make}%20{self.model}%20{self.keyword_1}%20{self.keyword_2}&language=en"
        headers = {'Accept-Language': 'en-US,en;q=0.9'}
        yield Request(url, headers=headers)

    def parse(self, response):
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--headless=new")
        # Start splinter browser
        with webdriver.Chrome(options=chrome_options) as browser:
            # Visit URL
            browser.get(response.url)

            # Scroll down to load more results
            scroll_count = 10
            scroll_delay = 5
            for _ in range(scroll_count):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_delay)

            # Get the HTML content of the page
            html_content = browser.page_source

        # Parse the HTML content with Scrapy
        scrapy_response = HtmlResponse(url=response.url, body=html_content, encoding='utf-8')

        # Extract data from each listing container
        for listing in scrapy_response.xpath('//div[contains(@class, "x9f619") and contains(@class, "x78zum5") and contains(@class, "x1r8uery") and contains(@class, "xdt5ytf") and contains(@class, "x1iyjqo2") and contains(@class, "xs83m0k") and contains(@class, "x1e558r4") and contains(@class, "x150jy0e") and contains(@class, "x1iorvi4") and contains(@class, "xjkvuk6") and contains(@class, "xnpuxes") and contains(@class, "x291uyu") and contains(@class, "x1uepa24")]'):
            loader = ItemLoader(item=FacebookMarketplaceItem(), selector=listing)

            # Load data into item fields
            loader.add_xpath('Listing_Title', './/span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6"]/text()')
            loader.add_xpath('Listing_Location', './/div[contains(@class, "x1iorvi4")]//span[contains(@class, "x1lliihq") and contains(@class, "x6ikm8r") and contains(@class, "x10wlt62") and contains(@class, "x1n2onr6") and contains(@class, "xlyipyv") and contains(@class, "xuxw1ft")]/text()')
            loader.add_xpath('Listing_Price_CAD', './/span[contains(@class, "x193iq5w")]/text()')
            loader.add_xpath('Mileage_KM', './/div[contains(@class, "x1iorvi4")]//span[contains(@class, "x1lliihq") and contains(@class, "x6ikm8r") and contains(@class, "x10wlt62") and contains(@class, "x1n2onr6") and contains(@class, "xlyipyv") and contains(@class, "xuxw1ft")]/text()')
            loader.add_xpath('Listing_Url', './/a[contains(@class, "x1i10hfl")]/@href')

            item = loader.load_item()

            # Check if all fields are null
            if all(value is None for value in item.values()):
                continue  # Skip yielding this item
            
            # Check if make,model,keywords present in title
            title = item.get('Listing_Title')
            if title:
                title_lower = title[0].lower()
                if all(term.lower() in title_lower for term in [self.year, self.make, self.model]) \
                    and (self.keyword_1.lower() in title_lower or self.keyword_2.lower() in title_lower):
                    yield item