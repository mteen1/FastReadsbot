import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#TODO: crawl the ketab.ir to get the info of farsi books to db

book_name = "5 صبحی ها"  # Replace with desired book name
url = f"https://ketab.ir/search?search={book_name}"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


# Get all search result items

def find_element(driver, xpath):
    """Finds the first occurrence of an element using the given XPath."""
    element = driver.find_element_by_xpath(xpath)
    return element


print(find_element(soup, '/html/body/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/a/img'))
