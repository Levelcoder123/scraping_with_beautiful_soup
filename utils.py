from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# load website using chrome webdriver
def get_driver():
    service = Service('../../chromedriver')  # chromedriver path
    driver = webdriver.Chrome(service=service)

    return driver


def get_soup_by_selenium_driver(user_url):
    driver = get_driver()
    driver.get(user_url)

    # get html from driver and make it soup
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, features="html.parser")

    return soup
