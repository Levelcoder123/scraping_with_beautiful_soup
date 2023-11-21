from datetime import datetime

import pandas as pd

from scraper import get_page_urls, get_product_urls, get_all_product_details

latest_date_time = datetime.now()
formatted_datetime = latest_date_time.strftime("%Y_%m_%d_%H_%M")

page_url = '/used-cars/search/-/ct_lahore/ca_college-road/'
page_urls = get_page_urls(page_url)
product_urls = get_product_urls(page_urls)
product_all_details = get_all_product_details(product_urls)

df = pd.DataFrame(product_all_details)
df.to_excel(f'pakwheels_data_{formatted_datetime}.xlsx', index=False)
