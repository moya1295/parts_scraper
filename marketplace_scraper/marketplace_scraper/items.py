# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose
from scrapy.loader import ItemLoader



def is_english(text):
    # Check if any non-English characters are present
    return all(ord(char) < 128 for char in text)

def convert_to_english(text):
    # Check if the text is already in English
    if is_english(text):
        return text

    # Define a dictionary to map non-English words to English equivalents
    language_map = {
        'لاکھ': 'lakh',
        'کلو': 'kilo',
        'میٹر': 'meter',
        'ہزار': 'thousand',
    }
    
    # Replace each non-English word with its English equivalent
    for word, translation in language_map.items():
        text = text.replace(word, translation)
    
    # Remove non-breaking space and any other Unicode control characters
    text = ''.join(char for char in text if ord(char) > 31 and ord(char) < 127)
    
    return text.strip()

#This function takes last value from the list
def take_last(values):
    if len(values) >= 1:
        text = (values[-1])
        if 'kilo' in text or 'miles' in text or 'km' in text:
            return text
        else:
            return None
    else:
        return None

# this functions take a url like /v-cars-trucks/mississauga-peel-region/2010-toyota-corolla-le-for-sale-push-to-start/1684035234  and add domain name
def update_url_kijiji(value):
    suffix = "https://www.kijiji.ca"
    if len(value) >= 1:
        url = value[0]
        if "kijiji" in url.lower():    
            return url
        else:
            return suffix+url
    else:
        return None
    
# Same function as above but for facebook marketplace
def update_url_facebook(value):
    suffix = "https://www.facebook.com"
    if len(value) >= 1:
        url = value[0]
        if "facebook" in url.lower():    
            return url
        else:
            return suffix+url
    else:
        return None

# This functions extracts mileage and clean it
def extract_mileage(value):
    if len(value) >= 1:
        for i in value:
            if 'km' in i:
                cleaned_string = ''.join(filter(str.isdigit, i))
                return cleaned_string
    else:
        return None

def convert_currency_to_int(value):

    if len(value) >= 1:
        currency_str = value[0]
    else:
        return None

    # Check if the string is "Please Contact"
    if currency_str.lower() == "please contact":
        return None
    
    # Remove leading currency symbol and commas
    cleaned_str = currency_str.replace('$', '').replace(',', '')
    # Remove decimal points
    #cleaned_str = cleaned_str.replace('.', '')

    # Convert the cleaned string to an integer
    try:
        result = cleaned_str
        return result
    except ValueError:
        return None


class MarketplaceScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class KijiMarketplaceItem(scrapy.Item):
    Listing_Title = scrapy.Field(default=None)
    Listing_Price_CAD = scrapy.Field(default=None, input_processor= Compose(convert_currency_to_int))
    Listing_Location = scrapy.Field(default=None)
    Listing_Url = scrapy.Field(default=None, input_processor = Compose(update_url_kijiji))
    Mileage_KM = scrapy.Field(default=None, input_processor = Compose(extract_mileage))
    Description = scrapy.Field(default=None)

class FacebookMarketplaceItem(scrapy.Item):
    Listing_Title = scrapy.Field()
    Listing_Price_CAD = scrapy.Field(output_processor = TakeFirst())
    Listing_Location = scrapy.Field(output_processor = TakeFirst())
    Listing_Url = scrapy.Field(input_processor = Compose(update_url_facebook))
    Mileage_KM = scrapy.Field(input_processor = Compose(take_last))


