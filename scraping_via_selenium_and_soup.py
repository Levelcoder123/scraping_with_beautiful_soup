from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

base_url = 'https://www.pakwheels.com'
page_url = '/used-cars/search/-/ct_lahore/ca_college-road/'


# load website using chrome webdriver
def get_driver(website):
    service = Service('../chromedriver')  # chromedriver path
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    return driver


def get_soup(driver_for_drive):
    # get html from driver and make it soup
    html_data = driver_for_drive.page_source
    soup = BeautifulSoup(html_data, features="html.parser")

    return soup


def get_product_details(delicious_soup):
    # get product details
    car_name_data = delicious_soup.find('div', id='scroll_car_info').get_text(separator='\n', strip=True)
    car_name = car_name_data.split('\n')[0]

    price = delicious_soup.find('strong', class_='generic-green').get_text(separator=' ', strip=True)

    city = delicious_soup.find('p', class_='detail-sub-heading').get_text(separator=' ', strip=True).split()[2]

    location_data = (delicious_soup.find('p', class_='detail-sub-heading')
                     .get_text(separator=',', strip=True).split(',', maxsplit=2))
    location = ','.join(location_data[:2])

    model_year = \
        delicious_soup.find('table', class_='table table-bordered text-center table-engine-detail fs16').get_text(
            separator=',', strip=True).split(',')[0]

    mileage = delicious_soup.find('table', class_='table table-bordered text-center table-engine-detail fs16').get_text(
        separator='-', strip=True).split('-')[1]

    seller_name_index = 0
    seller_name_data = delicious_soup.find('div', class_='owner-detail-main').get_text(separator=',', strip=True).split(
        ',')

    # checking "is seller 'Dealer' or not? "
    if seller_name_data[seller_name_index] == 'Dealer:':
        seller_name_index = 1
    seller_name = seller_name_data[seller_name_index]

    is_featured = False
    featured_or_not = delicious_soup.find('div', id='myCarousel').get_text(separator=',', strip=True).split(',')[0]
    if featured_or_not == 'FEATURED':
        is_featured = True

    images = delicious_soup.find('ul', class_='lSPager lSGallery').find_all('img')
    cover_image_url = images[0]['data-original']

    image_1_url = images[1]['data-original']
    image_2_url = images[2]['data-original'] if len(images) > 2 else None

    return {
        'car_name': car_name,
        'price': price,
        'city': city,
        'location': location,
        'model_year': model_year,
        'mileage': mileage,
        'seller_name': seller_name,
        'is_featured': is_featured,
        'cover_image_url': cover_image_url,
        'image_1': image_1_url,
        'image_2': image_2_url
    }


def get_page_urls():
    page_no = 1
    page_urls_list = []

    while True:
        page_urls_list.append(f'{base_url}{page_url}?page={page_no}')

        if page_no == 3:
            break
        page_no += 1

    return page_urls_list


def get_products_url(page_urls):
    product_urls_list = []

    for page in page_urls:
        ready_driver = get_driver(page)
        soup_for_taste = get_soup(ready_driver)
        all_product_urls = soup_for_taste.find_all('a', class_='car-name ad-detail-path')

        for product_url in all_product_urls:
            product_href = product_url['href']
            product_urls_list.append(base_url + product_href)

    return product_urls_list


def get_all_products_details(product_urls_list):
    details_of_all_products = []

    for product_url in product_urls_list:
        driver_for_ride = get_driver(product_url)
        tasty_soup = get_soup(driver_for_ride)
        details_of_all_products.append(get_product_details(tasty_soup))

    return details_of_all_products


pages_url = get_page_urls()
all_products_url = get_products_url(pages_url)
products_details = get_all_products_details(all_products_url)

df = pd.DataFrame(products_details)
df.to_excel('all_products_details.xlsx', index=False)
