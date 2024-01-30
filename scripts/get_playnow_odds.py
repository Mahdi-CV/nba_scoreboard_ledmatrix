from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
driver.get('https://www.playnow.com/sports/sports/competition/9132/basketball/north-america/nba/matches')
time.sleep(10)  # Adjust the timing as needed

# Wait for the element to load (if necessary) and find it by class name
element = driver.find_element(By.CLASS_NAME, 'ellipsis-0-3-177 ellipsisSingleLine-0-3-178')

# If the element is found, print it, else print a message saying it wasn't found
if element:
    print(element.text)
else:
    print('Element not found.')

# Close the browser
driver.quit()
