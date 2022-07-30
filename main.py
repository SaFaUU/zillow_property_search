import driver as driver
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Add your form link
FORM_LINK = "..."

# Chromerdriver Linking
ser = Service("C://Selenium/chromedriver.exe")

# Making chrome not close
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("window-size=1200x600")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)

# Header for website bot detection bypass

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
with requests.Session() as s:
    city = 'San Francisco, CA/'  # *****change this city to what you want*****
    url = 'https://www.zillow.com/homes/for_rent/' + city
    response = requests.get(url, headers=req_headers)

Contents = response.text
Soup = BeautifulSoup(Contents, features="html.parser")

time.sleep(5)

property_listings_link_retrieved = Soup.select(selector=".list-card-link")
property_listings_price_retrieved = Soup.select(selector=".list-card-price")
property_listings_addr_retrieved = Soup.select(selector=".list-card-addr")

property_listings_link = []
property_listings_price = []
property_listings_addr = []

for link in property_listings_link_retrieved[0:-1]:
    property_listings_link.append(link.get("href"))
print(property_listings_link)

for link in property_listings_price_retrieved:
    property_listings_price.append(link.getText())
print(property_listings_price)

for link in property_listings_addr_retrieved:
    property_listings_addr.append(link.getText())
print(property_listings_addr)



for element in range(0,len(property_listings_link)):
    driver.get(FORM_LINK)
    driver.implicitly_wait(10)

    address_box = driver.find_element(By.XPATH,
                                      '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(address_box))
    address_box.click()
    address_box.send_keys(property_listings_addr[element])

    price_per_month = driver.find_element(By.XPATH,
                                          '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_per_month.send_keys(property_listings_price[element])

    link_to_property = driver.find_element(By.XPATH,
                                           '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_to_property.send_keys(property_listings_link[element])

    submit_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

