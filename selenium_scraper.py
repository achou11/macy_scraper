from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import re

# set up driver
driver = webdriver.Chrome()
url = 'https://www.macys.com/?cm_sp=navigation-_-top_nav-_-macys_icon'
driver.get(url)

# attempt to remove ad if it appears when entering site
try:
    ad = driver.find_element_by_css_selector('area.close.agree').click()

except NoSuchElementException:
    pass

# press home button
home_button = driver.find_element_by_link_text('HOME').click()

# press Home Decor link
home_decor_link = driver.find_element_by_link_text('Home Decor').click()

#
# Time to scrape!!!
#

# create collection
collection = []

# initialize page number
current_page = 1

# components of page url
base_url = "https://www.macys.com/shop/for-the-home/home-decor/Pageindex/"
end_url = "?id=55971"

# get total number of pages
num_pages = int(driver.find_element_by_xpath('//*[@id="paginateTop"]/a[5]').text)

while current_page <= num_pages:

    # get list of products on page
    product_list = driver.find_elements_by_css_selector('div.textWrapper')

    # extract data for each product
    for p in product_list:
        document = {"name": None,
                    "original_price": {"min": None,
                                       "max": None},
                    "sale_price": {"min": None,
                                   "max": None}
                    }
        document['name'] = p.find_element_by_css_selector('div.shortDescription').text

        # all items have an original price
        original_min = p.find_element_by_css_selector('span.first-range').text

        # if price exceeds $999.00, remove comma
        if re.search(',', original_min):
            original_min = re.sub(',', '', original_min)

        document['original_price']['min'] = float(re.search('\d+\.?\d*', original_min).group())

        # test for whether item has sale price
        try:
            sale_min = p.find_element_by_css_selector('span.first-range.priceSale').text

            if re.search(',', sale_min):
                sale_min = re.sub(',', '', sale_min)

            document['sale_price']['min'] = float(re.search('\d+\.?\d*', sale_min).group())

        except NoSuchElementException:
            pass

        # test for whether item has price range for either original or sale
        try:
            original_max = p.find_element_by_css_selector('span.second-range').text

            if re.search(',', original_max):
                original_max = re.sub(',', '', original_max)

            document['original_price']['max'] = float(re.search('\d+\.?\d*', original_max).group())

        except NoSuchElementException:
            pass

        try:
            if document['sale_price']['min'] is None:
                pass
            else:
                sale_max = p.find_element_by_css_selector('span.second-range.priceSale ').text

                if re.search(',', sale_max):
                    sale_max = re.sub(',', '', sale_max)

                document['sale_price']['max'] = float(re.search('\d+\.?\d*', sale_max).group())

        except NoSuchElementException:
            pass

        # print item information
        print(f"Item Name: {document['name']}")
        print(f"Original Min Price: {document['original_price']['min']}\nOriginal Max Price: {document['original_price']['max']}")
        print(f"Sale Min Price: {document['sale_price']['min']}\nSale Max Price: {document['sale_price']['max']}")
        print()

        # populate collection
        collection.append(document)

    # go to next page
    current_page += 1
    driver.get(base_url + str(current_page) + end_url)

print(f'Number of items scraped: {len(collection)}')

driver.quit()

#
# Add data to MongoDB!!!
#

client = MongoClient()

# if database already exists, remove it
try:
    client.drop_database('macy_scrape')

except TypeError:
    pass

# create new database
db = client.macy_scrape

# initialize collection
items_collection = db.items

# add item data to collection
added_items = items_collection.insert_many(collection)

# confirm that insertion into Mongo worked
print('Added collection to database!')
print(f'Number of items added to collection: {len(added_items.inserted_ids)}')

client.close()
print('Client closed.')
