from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

base_url = 'https://www.pakwheels.com'
page_url = '/used-cars/search/-/ct_lahore/ca_college-road/'


# load website using chrome webdriver
def get_driver():
    service = Service('../../chromedriver')  # chromedriver path
    driver = webdriver.Chrome(service=service)

    return driver


def get_soup_by_selenium_driver(website):
    driver = get_driver()
    driver.get(website)

    # get html from driver and make it soup
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, features="html.parser")

    return soup


def get_product_details(soup):
    # get product details
    name_data = soup.find('div', id='scroll_car_info').get_text(separator='\n', strip=True)
    name = name_data.split('\n')[0]

    price = soup.find('div', class_='price-box').get_text(separator=' ', strip=True)

    location_data = (soup.find('p', class_='detail-sub-heading')
                     .get_text(separator=',', strip=True).split(',', maxsplit=2))
    location = ','.join(location_data[:2])

    model_year = \
        soup.find('span', class_='engine-icon year').parent.get_text(strip=True)

    mileage = soup.find('span', class_='engine-icon millage').parent.get_text(strip=True)

    seller_name_data = soup.find('div', class_='owner-detail-main').get_text(separator=',', strip=True).split(
        ',')

    # checking "is seller 'Dealer' or not? "
    seller_name = seller_name_data[0]
    if seller_name == 'Dealer:':
        seller_name = seller_name_data[1]

    featured_or_not = soup.find('div', id='myCarousel').get_text(separator=',', strip=True).split(',')[0]

    is_featured = (True if featured_or_not == 'FEATURED' else False)

    images = soup.find('div', id='myCarousel').find('ul', class_='lSPager lSGallery').findAll('img')

    cover_image_url = images[0]['data-original']
    image_1_url = images[1]['data-original'] if len(images) > 1 else None
    image_2_url = images[2]['data-original'] if len(images) > 2 else None

    return {
        'name': name,
        'price': price,
        'location': location,
        'model_year': model_year,
        'mileage': mileage,
        'seller_name': seller_name,
        'is_featured': is_featured,
        'cover_image_url': cover_image_url,
        'image_1': image_1_url,
        'image_2': image_2_url,
    }


def get_page_urls(last_page):
    page_urls_list = []

    for page_num in range(1, len(last_page)):
        page_urls_list.append(f'{base_url}{page_url}?page={page_num}')

    return page_urls_list


def get_products_urls(page_urls):
    products_urls_list = []

    for url in page_urls:
        soup = get_soup_by_selenium_driver(url)
        all_product_urls = soup.find_all('a', class_='car-name ad-detail-path')

        for product_url in all_product_urls:
            product_href = product_url['href']
            products_urls_list.append(base_url + product_href)

    return products_urls_list


def get_products_details(product_urls_list):
    products_details = []

    for product_url in product_urls_list:
        soup = get_soup_by_selenium_driver(product_url)
        products_details.append(get_product_details(soup))

    return products_details


pages_urls = get_page_urls(last_page='')
products_urls = get_products_urls(pages_urls)
products_all_details = get_products_details(products_urls)

df = pd.DataFrame(products_all_details)
df.to_excel('all_products_details.xlsx', index=False)
