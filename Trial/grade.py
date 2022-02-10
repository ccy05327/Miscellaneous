import time
from selenium import webdriver
from bs4 import BeautifulSoup

CHROME_DRIVE_PATH = ""
EMAIL = ""
PASSWORD = ""

login_url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london?authMode=login"
url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london/home"

driver = webdriver.Chrome(executable_path=CHROME_DRIVE_PATH)
driver.get(login_url)

driver.find_element_by_id("email").send_keys(EMAIL)
driver.find_element_by_id("password").send_keys(PASSWORD)
driver.find_element_by_xpath("//button[@type='submit']").click()

# wait for page to be ready and redirect to degree homepage
time.sleep(10)
driver.get(url)

# wait again and click the left button twice (change later when the week increases)
time.sleep(5)
driver.find_element_by_xpath(
    '//*[@id="home-tabpanel"]/main/div/div/div/div/button[1]').click()
driver.find_element_by_xpath(
    '//*[@id="home-tabpanel"]/main/div/div/div/div/button[1]').click()

# get the page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Change the following xpath by clicking the respective <a> tag, right click to copy the xPath and paste it here
c1 = driver.find_element_by_xpath(
    '//*[@id="home-tabpanel"]/main/div/ul/li[1]/a[2]')
c2 = driver.find_element_by_xpath(
    '//*[@id="home-tabpanel"]/main/div/ul/li[2]/a[2]')
c3 = driver.find_element_by_xpath(
    '//*[@id="home-tabpanel"]/main/div/ul/li[5]/a[2]')
c4 = driver.find_element_by_xpath(
    '//*[@id="home-tabpanel"]/main/div/ul/li[5]/a[3]')

# This last part can be executed separately, but the above has to be one block
print('ADS1\n', c1.text)
print('PwD\n', c2.text)
print('WD-1\n', c3.text)
print('WD-2\n', c4.text)

# The output will be something like this:
# PwD
# Graded Assignment: Mid-term programming assignment[001]3hJan 24, 9: 00 PM CST
# In review
