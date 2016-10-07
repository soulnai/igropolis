__author__ = 'avasilyev2'

from hobby_page_object import CatalogPage
import selenium
from selenium import webdriver
import db_work
import time

driver = webdriver.Firefox() #webdriver.PhantomJS(executable_path='C:\Python27\phantomjs.exe')

catalog_page = CatalogPage(driver)
driver = catalog_page.driver
driver.get("http://hobbygames.biz/")
time.sleep(3)
CatalogPage.get_top_games(catalog_page)
time.sleep(3)

driver.get("http://hobbygames.biz/?route=product/provider/index")


while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    time.sleep(2)
    CatalogPage.next_page(catalog_page)



#db_work.print_from_db()
driver.quit()