__author__ = 'avasilyev2'

from tesera_page_object import CatalogPage
import selenium
from selenium import webdriver
import collect.db_work
from time import sleep

driver = webdriver.Firefox()

catalog_page = CatalogPage(driver)
driver.get("http://tesera.ru/")


CatalogPage.get_products(catalog_page)


collect.db_work.output_from_db()

driver.quit()