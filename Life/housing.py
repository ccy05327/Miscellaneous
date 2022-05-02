import click
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime

URL = r"https://lvr.land.moi.gov.tw/"
CHROME_DRIVE_PATH = r"C:\\Users\\hanna\\Downloads\\chromedriver.exe"
# CHROME_DRIVE_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    time.sleep(3)
    driver = webdriver.Chrome(CHROME_DRIVE_PATH)
    driver.get(URL)
    time.sleep(10)

    # print(driver.find_elements(by=By.TAG_NAME,
    #       value='form'))

    country_dropdown = driver.find_element(by=By.ID, value='p_city')
    time.sleep(3)
    # country_dropdown
    # driver.find_element(by=By.CSS_SELECTOR, value='#p_city')

    # country_dropdown.select_by_visible_text('基隆市')
    # country_dropdown = driver.find_elements(
    # by=By.XPATH, value='/html/body/section[1]/div[2]/div/form/div/div[1]/select/option[2]')
    # for country in country_dropdown:
    print(country_dropdown)
    # country_dropdown.select_by_value("C")

    # district_dropdown = Select(driver.find_element_by_id("p_town"))
    # driver.find_element_by_xpath('//*[@id="p_city"]/option[text()="安樂區"]').click()
    # district_dropdown.select_by_value("C06")
    # driver.find_element(
    # by=By.XPATH, value='/html/body/section[1]/div[2]/div/form/div/div[2]/select')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # GBP1 = soup.find('table').find('td', id='_GBP_rs')
    time.sleep(2)

    print(soup)


if __name__ == "__main__":
    main()
