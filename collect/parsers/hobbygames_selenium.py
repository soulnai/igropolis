__author__ = 'avasilyev2'

from hobbygames_page_object import CatalogPage
import selenium
from selenium import webdriver
import db_work
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.PhantomJS(executable_path='C:\Python27\phantomjs.exe')



catalog_page = CatalogPage(driver)
driver.get("http://hobbygames.ua/tablegames/all/category/182-vse-nastolnie-igri?limit=15&limitstart=510")


while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    CatalogPage.next_page(catalog_page)


db_work.print_from_db()

#driver.quit()