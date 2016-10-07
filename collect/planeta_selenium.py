__author__ = 'avasilyev2'

from planeta_page_object import CatalogPage
import selenium
from selenium import webdriver
import db_work
from time import sleep

driver = webdriver.PhantomJS(executable_path='C:\Python27\phantomjs.exe')

catalog_page = CatalogPage(driver)
driver.get("http://www.planetaigr.com/catalog")

CatalogPage.get_top(catalog_page)
sleep(1)

while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    sleep(1)
    CatalogPage.next_page(catalog_page)


#db_work.print_from_db()

#driver.quit()