# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    def check_if_available(self, prod):
        try:
            if prod.find_element_by_class_name('addtocart_button_transparent_box_2').get_attribute('title') == 'Нажмите сюда чтобы добавить товар в корзину':
                return True
            else:
                return False
        except NoSuchElementException:
            return False
        return False

    def get_products(self):
        products = []
        root = self.wait.until(EC.presence_of_element_located((By.ID, 'product_list')))
        prods = root.find_elements_by_class_name("browseProductContainer")
        time.sleep(1)
        for prod in prods:
            product = {"name": prod.find_element_by_xpath(".//a").text,
                       "image": prod.find_element_by_xpath(".//td/a/img").get_attribute("src"),
                       "price": CatalogPage.get_price(self, prod),
                       "availability": CatalogPage.check_if_available(self, prod),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "shop": "hobbygames"}
            collect.db_work.save_to_db(product)
            products.append(product)
        return products

    def next_page(self):
        next_page = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@title,"Следующая")]')))
        next_page.click()
        time.sleep(3)

    def check_next_page_exists(self):
        try:
            self.driver.find_element_by_xpath('//a[contains(@title,"Следующая")]')
        except NoSuchElementException:
            return False
        return True

    def only_numerics(self, seq):
        return filter(type(seq).isdigit, seq)

    def get_price(self, prod):
        try:
            prod.find_element_by_class_name("productPrice")
        except NoSuchElementException:
            return 0
        return int(CatalogPage.only_numerics(self, prod.find_element_by_class_name("productPrice").text)[:-2])
