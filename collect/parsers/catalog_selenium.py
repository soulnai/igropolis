__author__ = 'avasilyev2'

from tesera_catalog_page_object import CatalogPage
import selenium
from selenium import webdriver
import collect.db_work
import time

driver = webdriver.Firefox()

catalog_page = CatalogPage(driver)
driver.get("http://tesera.ru/games/all/851/")
time.sleep(3)


while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    CatalogPage.next_page(catalog_page)



#driver.quit()