import toplay_page_object

__author__ = 'avasilyev2'

from toplay_page_object import CatalogPage, BasePage
import selenium
from selenium import webdriver
import db_work
from time import sleep

#base = BasePage()


driver = webdriver.Firefox() #webdriver.PhantomJS(executable_path='C:\Python27\phantomjs.exe')

catalog_page = CatalogPage(driver)
driver.get("http://toplay.com.ua/catalog/nastolnye-igry?page=all")
CatalogPage.get_products(catalog_page)
'''while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    sleep(1)
    CatalogPage.next_page(catalog_page)
'''

db_work.print_from_db()

driver.quit()