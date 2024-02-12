"""
This is the first scraper of the project.
This scraper will scrape kijiji.ca with given keywords and return a csv file containing
Listing_url, Listing_title, Listing_price, Listing_location
Author: Muhammad Owais
Dated: 01-Feb-24
"""

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse, Request
from time import sleep
from scrapy.loader import ItemLoader
from marketplace_scraper.items import KijiMarketplaceItem

class KijiMarketSpider(scrapy.Spider):
    name = 'kiji_market'
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["Listing_Title", "Listing_Location", "Listing_Price_CAD", "Mileage_KM", "Description", "Listing_Url"]
    }

    def __init__(self, year=None, make=None, model=None,city=None, keyword_1='', keyword_2='', *args, **kwargs):
        super(KijiMarketSpider, self).__init__(*args, **kwargs)

        self.year = year
        self.make = make
        self.model = model
        self.city = city
        self.keyword_1 = keyword_1
        self.keyword_2 = keyword_2

        # Set up Selenium options
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # Run Chrome in headless mode (without GUI)
        chrome_options.add_argument("--lang=en")
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_requests(self):
        yield scrapy.Request(f"https://www.kijiji.ca/b-canada/{self.year}-{self.make}-{self.model}-{self.keyword_1}-{self.keyword_2}/k0l0?dc=true")

    def parse(self, response):
        # Use Selenium to interact with the page and get the dynamically loaded content
        self.driver.get(response.url)
        sleep(5)  # Adjust this delay based on your needs, allow time for dynamic content to load

        # Create a new response with the content generated by JavaScript
        sel_response = HtmlResponse(
            url=self.driver.current_url,
            body=self.driver.page_source,
            encoding='utf-8',
        )

        # Now you can use Scrapy selectors on the Selenium-generated response
        div_elements = sel_response.css('div.bHKVfX')
        
        for listing in div_elements:

            l = ItemLoader(item=KijiMarketplaceItem(), selector=listing)

            l.add_css("Listing_Title", 'a[data-testid="autos-cross-promo-listing-card-link"]::text, a[data-testid="listing-link"]::text')

            #l.add_css("Listing_Price_CAD", 'p[data-testid="listing-price"]::text' )
            l.add_xpath("Listing_Price_CAD", './/p[contains(@data-testid, "listing-price")]/text()')
            l.add_css("Listing_Location", 'p[data-testid="listing-location"]::text, div.eMzKxK p.dvzUfQ::text')
    
            l.add_css("Listing_Url", 'a[data-testid="autos-cross-promo-listing-card-link"]::attr(href), a[data-testid="listing-link"]::attr(href)')
            
            #l.add_css('Mileage_KM', 'p.jWZAHd ::text')
            l.add_xpath('Mileage_KM', './/p[contains(@class, "jWZAHd")]/text()')

            l.add_css('Description', 'p[data-testid="listing-description"]::text')

            # Check if make model in listing title then load, else reject

            #title = l.get_css('a[data-testid="autos-cross-promo-listing-card-link"]::text, a[data-testid="listing-link"]::text')
            
            #if self.make.lower() in title[0].lower() and self.model.lower() in title[0].lower():
            #    yield l.load_item()

            item = l.load_item()
            title = item.get('Listing_Title')
            location = item.get('Listing_Location')
            if title:
                title_lower = title[0].lower()
                if all(term.lower() in title_lower for term in [self.year, self.make, self.model]) \
                    and (self.keyword_1.lower() in title_lower or self.keyword_2.lower() in title_lower):
                    yield item

        # Follow the next page if available
        next_page = sel_response.css('a.garPwt::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def closed(self, reason):
        # Close the Selenium WebDriver when the spider is closed
        self.driver.quit()
