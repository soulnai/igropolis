__author__ = 'avasilyev2'

from oflex_page_object import CatalogPage
import selenium
from selenium import webdriver
import db_work
from time import sleep

driver = webdriver.PhantomJS(executable_path='C:\Python27\phantomjs.exe')

catalog_page = CatalogPage(driver)
driver.get("http://oflex.ru/")


CatalogPage.get_products(catalog_page)


db_work.output_from_db()

driver.quit()