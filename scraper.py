from constants import page_url, base_url
from utils import get_soup_by_selenium_driver


def get_product_details(soup):
    # get product details
    name = soup.find('div', id='scroll_car_info').get_text(separator='\n', strip=True).split('\n')[0]

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

    is_featured = featured_or_not == 'FEATURED'

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


def get_page_urls(soup):
    page_num = 1
    page_urls_list = []
    last_page_url = get_last_page(soup)

    while True:
        page_urls_list.append(f'{base_url}{page_url}?page={page_num}')

        if last_page_url in page_urls_list:
            break

    return page_urls_list


def get_last_page(soup):
    last_page_url_data = soup.find('li', class_='last next')['href']
    last_page_url = base_url + last_page_url_data

    return last_page_url


def get_product_urls(page_urls):
    product_urls_list = []

    for url in page_urls:
        soup = get_soup_by_selenium_driver(url)
        all_product_urls = soup.find_all('a', class_='car-name ad-detail-path')

        for product_url in all_product_urls:
            product_href = product_url['href']
            product_urls_list.append(base_url + product_href)

    return product_urls_list


def get_all_product_details(product_urls_list):
    products = []

    for product_url in product_urls_list:
        soup = get_soup_by_selenium_driver(product_url)
        products.append(get_all_product_details(soup))

    return products