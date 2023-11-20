from scraper import get_page_urls, get_product_urls, get_all_product_details
import pandas as pd

page_urls = get_page_urls()
product_urls = get_product_urls(page_urls)
product_all_details = get_all_product_details(product_urls)

df = pd.DataFrame(product_all_details)
df.to_excel('all_products_details.xlsx', index=False)
