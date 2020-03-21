from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("https://www.expedia.com/Flights-Search?flight-type=on&starDate=03%2F19%2F2020&mode=search&trip=oneway&leg1=from%3ALondon%2C+England%2C+UK+%28LON-All+Airports%29%2Cto%3AZurich%2C+Switzerland+%28ZRH%29%2Cdeparture%3A03%2F19%2F2020TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY")

#driver = webdriver.Chrome(options=options)
#driver.get("https://www.youtube.com/")
#element_text = driver.find_element_by_id("title").text
#print(element_text)


try:
    element_text = driver.find_element(By.XPATH,'//img[@class = " needsclick"]')
    print(element_text[0])
except:
    prices = driver.find_elements_by_xpath('//div')

for i in range(len(prices)):
    print(prices[i].text)


#print("prices element is:" +str(prices[0].text))


#test file
