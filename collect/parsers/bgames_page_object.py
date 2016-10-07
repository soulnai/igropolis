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

import db_work


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class CatalogPage(BasePage):
    def next_page(self):
        next_page = self.wait.until(EC.presence_of_element_located((By.XPATH, "//u[contains(.,'ВПЕРЁД>>>')]")))
        next_page.click()
        time.sleep(3)

    def check_next_page_exists(self):
        try:
            self.driver.find_element_by_xpath("//u[contains(.,'ВПЕРЁД>>>')]")
        except NoSuchElementException:
            return False
        return True

    def only_numerics(self, seq):
        return filter(type(seq).isdigit, seq)

    def check_if_available(self, prod):
        try:
            av = prod.find_element_by_xpath('.//div[4]/img').get_attribute("title")
            if av == "Есть в наличии":
                return True
            else:
                return False
        except NoSuchElementException:
            return False
        return True

    def check_if_price_present(self, prod):
        try:
            price = prod.find_element_by_class_name("products_price").text
            if len(price) <= 0:
                return False
            else:
                return True
        except NoSuchElementException:
            return False
        return True

    def get_products(self):
        products = []
        root = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table[2]')))
        prods = root.find_elements_by_xpath('.//td')
        for prod in prods:
            if prod.find_element_by_xpath(".//div/div[3]").text == "!Игра на заказ :)":
                continue
            if CatalogPage.check_if_price_present(self, prod):
                price_text = prod.find_element_by_class_name("products_price").text
                price_num = CatalogPage.only_numerics(self, price_text.strip())
                price_num = price_num[:-2].strip()
            else:
                price_num = 0
            product = {"name": prod.find_element_by_xpath(".//div/div[3]/a").text,
                       "image": prod.find_element_by_xpath(".//div[2]/a/img").get_attribute("src"),
                       "price": int(price_num),
                       "availability": CatalogPage.check_if_available(self, prod),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "shop": "bgames"}
            db_work.save_to_db(product)
            products.append(product)
            time.sleep(0.1)
        return products