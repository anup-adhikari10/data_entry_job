import time

import requests
from selenium import webdriver
import re

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
Google_sheet = "https://forms.gle/vdxxaCUSDAGchVjq8"
URL_LINK = 'https://appbrewery.github.io/Zillow-Clone/'


def get_driver(uri_data):
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_experimental_option("detach", True)
    chrome_option.add_argument("disable-infobars")
    chrome_option.add_argument("start-maximized")
    chrome_option.add_argument("disable-dev-shm-usage")
    chrome_option.add_argument("no-sandbox")
    chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_option.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_option)
    driver.get(uri_data)
    return driver


def request_url_href_link(url):
    response = requests.get(url)
    response.raise_for_status()
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')
    return soup.select(".List-c11n-8-84-3-photo-cards li")


def all_link(link):
    href_link = []
    for _ in link:
        for items in _.find_all('a', href=True, class_="StyledPropertyCardDataArea-anchor"):
            href_link.append(items.get("href"))
    return href_link


def all_price(link):
    href_link = []
    for _ in link:
        for items in _.select('span.PropertyCardWrapper__StyledPriceLine'):
            href_link.append(re.sub('[^0-9 \n]', '', items.get_text()).split(" 1")[0])
            # re.sub => only symbols in [^xxxxx]0-9-a-zA-Z..v...v...
    return href_link


def all_address(link):
    href_link = []
    for _ in link:
        for items in _.select('address'):
            href_link.append(items.get_text().strip())
    return href_link


def render_link(link, price, address):
    driver = get_driver(Google_sheet)
    time.sleep(2)
    for n in range(len(link)):
        time.sleep(1)
        item_01 = driver.find_element(By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        item_02 = driver.find_element(By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        item_03 = driver.find_element(By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        item_01.send_keys(f"{link[n]}")
        item_02.send_keys(f"{price[n]}")
        item_03.send_keys(f"{address[n]}")
        button.click()
        time.sleep(2)
        driver.find_element(By.XPATH, value="/html/body/div[1]/div[2]/div[1]/div/div[4]/a").click()
    driver.quit()


def main():
    data = request_url_href_link(URL_LINK)
    link = all_link(data)
    price = (all_price(data))
    address = (all_address(data))
    render_link(link, price, address)


main()
print('Success....!')