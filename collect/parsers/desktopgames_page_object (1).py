__author__ = 'avasilyev2'

from selenium.webdriver.common.by import By
import selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import collect.db_work


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class CatalogPage(BasePage):

    def get_all_pages(self):
        pages = []
        root = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page_list')))
        all_links_list = root.find_elements_by_xpath(".//a")
        for link in all_links_list:
            pages.append(link.get_attribute("href"))
        return pages

    def check_if_available(self, prod):
        try:
            prod.find_element_by_xpath('.//a[3]')
        except NoSuchElementException:
            return False
        return True

    def check_if_price_present(self, prod):
        try:
            self, prod.find_element_by_class_name("price").text
        except NoSuchElementException:
            return False
        return True

    def get_products(self):
        products = []
        prods = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product')))
        for prod in prods:
            if CatalogPage.check_if_price_present(self, prod):
                product = {"name": prod.find_element_by_xpath(".//h4").text,
                           "image": prod.find_element_by_xpath(".//img").get_attribute("src"),
                           "price": int(CatalogPage.only_numerics(self, prod.find_element_by_class_name("price").text)),
                           "availability": CatalogPage.check_if_available(self, prod),
                           "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                           "shop": "desktopgames"}
                collect.db_work.save_to_db(product)
                products.append(product)
        return products

    def only_numerics(self, seq):
        return filter(type(seq).isdigit, seq)
