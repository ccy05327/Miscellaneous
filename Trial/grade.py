from bs4 import BeautifulSoup
import time
from selenium import webdriver

CHROME_DRIVE_PATH = ""
EMAIL = ""
PASSWORD = ""

login_url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london?authMode=login"
url = "https://www.coursera.org/degrees/bachelor-of-science-computer-science-london/home"

driver = webdriver.Chrome(executable_path=CHROME_DRIVE_PATH)
driver.get(login_url)

# if the code stops on this line within 3 secs don't debug, do the following:
# 1. wait a few seconds and try again
# 2. restart the kernal and try again
# 3. just keep trying again and again
driver.find_element_by_id("email").send_keys(EMAIL)
driver.find_element_by_id("password").send_keys(PASSWORD)
driver.find_element_by_xpath("//button[@type='submit']").click()

# time for you to be authorized
time.sleep(10)
# redirect to degree homepage
driver.get(url)

# wait a bit and click the left button twice (change later as the week increases)
LEFT_BUTTON_PATH = '//*[@id="home-tabpanel"]/main/div/div/div/div/button[1]'
time.sleep(5)
driver.find_element_by_xpath(LEFT_BUTTON_PATH).click()
driver.find_element_by_xpath(LEFT_BUTTON_PATH).click()
# driver.find_element_by_xpath(LEFT_BUTTON_PATH).click()
# driver.find_element_by_xpath(LEFT_BUTTON_PATH).click()

# Change the following xpath by clicking the respective <a> tag, right click to copy the xPath and paste it here
C1_PATH = ""
C2_PATH = ""
C3_PATH = ""
C4_PATH = ""

c1 = driver.find_element_by_xpath(C1_PATH)
c2 = driver.find_element_by_xpath(C2_PATH)
c3 = driver.find_element_by_xpath(C3_PATH)
c4 = driver.find_element_by_xpath(C4_PATH)


# This last part can be executed separately, but the above has to be one block
print('c1\n', c1.text)
print('c2\n', c2.text)
print('c3\n', c3.text)
print('c4\n', c4.text)

# The output will be something like this:
# PwD
# Graded Assignment: Mid-term programming assignment[001]3hJan 24, 9: 00 PM CST
# In review

# The whole process should be around 30s
