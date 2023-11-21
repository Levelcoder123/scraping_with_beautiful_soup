import re

from constants import BASE_URL
from utils import get_soup_by_selenium_driver


def get_product_details(soup):
    # get product details
    name = soup.find('div', id='scroll_car_info').get_text(separator='\n', strip=True).split('\n')[0]

    price = soup.find('div', class_='price-box').get_text(separator=' ', strip=True)

    location = soup.find('p', class_='detail-sub-heading').get_text(strip=True)

    model_year = soup.find('span', class_='engine-icon year').parent.get_text(strip=True)

    mileage = soup.find('span', class_='engine-icon millage').parent.get_text(strip=True)

    seller_name_data = soup.find('div', class_='owner-detail-main').get_text(separator=',', strip=True).split(',')

    # checking "is seller 'Dealer' or not?"
    seller_name = seller_name_data[0]
    if seller_name == 'Dealer:':
        seller_name = seller_name_data[1]

    featured_or_not = soup.find('div', id='myCarousel').get_text(separator=',', strip=True).split(',')[0]
    is_featured = featured_or_not == 'FEATURED'

    images = soup.find('div', id='myCarousel')
    if images:
        all_images = images.find('ul', class_='lSPager lSGallery').findAll('img')
        cover_image_url = all_images[0]['data-original']
        image_1_url = all_images[1]['data-original'] if len(images) > 1 else None
        image_2_url = all_images[2]['data-original'] if len(images) > 2 else None
    else:
        cover_image_url = None
        image_1_url = None
        image_2_url = None

    return {
        'name': name,
        'price': price,
        'location': location,
        'model_year': model_year,
        'mileage': mileage,
        'seller_name': seller_name,
        'is_featured': is_featured,
        'cover_image_url': cover_image_url,
        'image_1_url': image_1_url,
        'image_2_url': image_2_url,
    }


def get_last_page(website_url):
    soup = get_soup_by_selenium_driver(website_url)
    last_page_url_data = soup.find('li', class_='last next')

    if last_page_url_data:
        last_page_url = last_page_url_data.find('a')['href']
        return BASE_URL + last_page_url

    return None


def get_last_page_index(website):
    last_page_url = get_last_page(website)

    # regex (Regular expression) pattern to find the page number
    pattern = r'page=(\d+)$'

    # Search for the pattern
    match = re.search(pattern, last_page_url)

    page_number = match.group(1)

    return int(page_number)


def get_page_urls(page_url):
    website = BASE_URL + page_url
    page_urls_list = [website]
    last_page_url = get_last_page(website)

    if last_page_url:
        last_page_index = get_last_page_index(website)

        for page_num in range(2, last_page_index + 1):
            page_urls_list.append(f'{BASE_URL}{page_url}?page={page_num}')

    return page_urls_list


def get_product_urls(page_urls):
    product_urls_list = []

    for url in page_urls:
        soup = get_soup_by_selenium_driver(url)
        all_product_urls = soup.find_all('a', class_='car-name ad-detail-path')

        for product_url in all_product_urls:
            product_urls_list.append(f'{BASE_URL}{product_url["href"]}')

    return product_urls_list


def get_all_product_details(product_urls_list):
    products = []

    for product_url in product_urls_list:
        soup = get_soup_by_selenium_driver(product_url)
        products.append(get_product_details(soup))

    return products
