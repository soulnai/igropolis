__author__ = 'avasilyev2'

from hobbygames_page_object import CatalogPage
import selenium
from selenium import webdriver
import collect.db_work

driver = webdriver.Firefox()

catalog_page = CatalogPage(driver)
driver.get("http://hobbygames.ua/tablegames/all")


while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    CatalogPage.next_page(catalog_page)


collect.db_work.print_from_db()

#driver.quit()