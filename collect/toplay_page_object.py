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
from selenium import webdriver

import db_work


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class CatalogPage(BasePage):

    def check_if_available(self, prod):
        try:
            prod.find_element_by_xpath(".//form/a")
        except NoSuchElementException:
            return False
        return True

    def check_if_old_price_exists(self, prod):
        try:
            prod.find_element_by_class_name("old")
        except NoSuchElementException:
            return False
        return True

    def get_products(self):
        products = []
        root = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div/section/div[2]')))
        prods = root.find_elements_by_class_name('products__item')
        print len(prods)
        for prod in prods:
            price = 0
            '''if prod.find_element_by_xpath(".//a").get_attribute("data-post") != None:
                continue

            if CatalogPage.check_if_available(self, prod):
                price = CatalogPage.only_numerics(self, prod.find_element_by_class_name("variants").text)
            else:
                price = CatalogPage.only_numerics(self, prod.find_element_by_class_name("price").text)

            if CatalogPage.check_if_old_price_exists(self, prod):
                price_new = CatalogPage.only_numerics(self, prod.find_element_by_class_name("variants").text)
                old_price = CatalogPage.only_numerics(self, prod.find_element_by_class_name("old").text)
                price = CatalogPage.only_numerics(self,price_new[:-len(old_price)])
                print price_new
                print old_price
                print price
            '''
            product = {"name": prod.find_element_by_xpath(".//a").get_attribute("title"),
                       "image": prod.find_element_by_xpath(".//img").get_attribute("src"),
                       "price": int(CatalogPage.only_numerics(self,prod.find_element_by_xpath(".//strong").text)),
                       "availability": CatalogPage.check_if_available(self, prod),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "shop": "toplay"}
            db_work.save_to_db(product)
            products.append(product)
            time.sleep(0.1)
        return products

    def next_page(self):
        next_page = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div/section/div[3]/ol/li[last()]/a')))
        #next_page = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next_page_link')))
        next_page.click()
        time.sleep(3)

    def check_next_page_exists(self):
        try:
            link = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div/section/div[3]/ol/li[last()]/a')))
            print link.get_attribute("src")
        except NoSuchElementException:
            return False
        return True

    def only_numerics(self, seq):
        return filter(type(seq).isdigit, seq)