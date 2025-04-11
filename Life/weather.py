
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re, math

CHROMEDRIVER_PATH = r"D:\Downloads\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

driver.get("https://www.cwa.gov.tw/V8/C/W/Town/Town.html?TID=6300300")

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')

table = soup.find("table", id="TableId3hr")
tbody = table.find("tbody")

time_row = tbody.find("tr", class_="time")
time_cells = time_row.find_all("th")[1:]
times = [time_cell.text.strip() for time_cell in time_cells]

forecast_rows = tbody.find_all("tr")

temp = [cell.text.strip()[:2] for cell in forecast_rows[1].find_all("td")]
feels = [cell.text.strip()[:2] for cell in forecast_rows[2].find_all("td")]
humidities = [cell.text.strip() for cell in forecast_rows[3].find_all("td")]


# Parse times like '14:00' -> 14
first_hour = int(re.match(r"\d{1,2}", times[0]).group())

# Rain chunks from the 3-hour forecast row (skip first cell)
rain_chunks = [cell.text.strip()
               for cell in forecast_rows[5].find_all("td")[1:]]

# Calculate how many hours until the next 3-hour block
offset = first_hour % 3
rains = []

# 1. If offset > 0, the first rain value only covers that many hours
if offset > 0:
    rains.extend([rain_chunks[0]] * (3 - offset))  # Fill to next block
    chunk_index = 1  # Next rain chunk index
else:
    chunk_index = 0

# 2. Fill the rest using full 3-hour groups
while len(rains) < len(times):
    if chunk_index < len(rain_chunks):
        rains.extend([rain_chunks[chunk_index]] * 3)
        chunk_index += 1
    else:
        # If we run out of rain data, repeat the last known value
        rains.append(rains[-1])

# 3. Trim to match number of time slots
rains = rains[:len(times)]


num_forecast_hours = len(times)

# Print the results
print("台北市 大安區：未來 12 小時天氣預報")
print("時間  | 溫度 | 體感 | 濕度 | 降雨機率")

for i in range(min(num_forecast_hours, 19)):
    time_str = times[i]
    temp_str = temp[i][:2]
    feel_str = feels[i][:2]
    humidity = humidities[i]
    rain = rains[i]
    
    print(f"{time_str} | {temp_str}°C | {feel_str}°C | {humidity} | {rain}")

driver.quit()
