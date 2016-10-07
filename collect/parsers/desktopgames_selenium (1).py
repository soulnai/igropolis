__author__ = 'avasilyev2'

from desktopgames_page_object import CatalogPage
import selenium
from selenium import webdriver
import collect.db_work
import time

driver = webdriver.Firefox()

catalog_page = CatalogPage(driver)
driver.get("http://desktopgames.com.ua/all_1_bg.html")

pages = CatalogPage.get_all_pages(catalog_page)

for page in pages:
    driver.get(page)
    CatalogPage.get_products(catalog_page)
    time.sleep(1)

"""
while CatalogPage.check_next_page_exists(catalog_page):
    CatalogPage.get_products(catalog_page)
    CatalogPage.next_page(catalog_page)



db_work.print_from_db()

#driver.quit()
"""