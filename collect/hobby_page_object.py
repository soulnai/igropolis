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
        #selenium_grid_url = 'http://172.23.61.44:4444/wd/hub'
        #self.driver = webdriver.Remote(selenium_grid_url, desired_capabilities={'platform': 'ANY', 'browserName': 'firefox', 'version': '', 'javascriptEnabled': True})
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class CatalogPage(BasePage):

    def hover(self, element):
        element_to_show_tooltip = element.find_element_by_class_name("img")
        hov = ActionChains(self.driver).move_to_element(element_to_show_tooltip)
        hov.perform()
        #text = self.driver.find_element_by_xpath('//*[@id="tooltip"]/h3').get_attribute('textContent')
        text = self.driver.find_element_by_class_name('ui-tooltip-content').text
        return text

    def check_if_available(self, prod):
        try:
            av = prod.find_element_by_xpath('.//div[2]').get_attribute("class")
            if av == "stock type0":
                print av
                print prod
                return False
            else:
                return True
        except NoSuchElementException:
            return False
        return True

    def get_products(self):
        products = []
        prods = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-item')))
        for prod in prods:
            product = {"name": prod.find_element_by_xpath(".//img").get_attribute("alt"),
                       "image": prod.find_element_by_xpath(".//img").get_attribute("src"),
                       "price": int(CatalogPage.only_numerics(self, prod.find_element_by_class_name("price").text)),
                       "availability": CatalogPage.check_if_available(self, prod),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "shop": "hobbyworld"}
            db_work.save_to_db(product)
            products.append(product)
            time.sleep(0.1)
        return products

    def next_page(self):
        next_page = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next-page')))
        next_page.click()
        time.sleep(3)

    def check_next_page_exists(self):
        try:
            self.driver.find_element_by_class_name('next-page')
        except NoSuchElementException:
            return False
        return True

    def only_numerics(self, seq):
        if "цена" in seq:
            return 0
        else:
            return filter(type(seq).isdigit, seq)

    def get_top_games(self):
        products = []
        time.sleep(2)
        root = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[1]/div[2]/div[5]/div[2]/section/div[2]/div')))
        prods = root.find_elements_by_xpath(".//li")
        count = 0
        for prod in prods:
            if count == 3:
                time.sleep(2)
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[1]/div[2]/div[5]/div[2]/section/div[2]/a[2]')))
                self.driver.execute_script("arguments[0].click();", element);
                time.sleep(2)
                count = 0
            product = {"name": prod.find_element_by_xpath(".//img").get_attribute("alt"),
                       "image": prod.find_element_by_xpath(".//img").get_attribute("src"),
                       "price": int(CatalogPage.only_numerics(self, prod.find_element_by_class_name("price").text)),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "shop": "hobbyworld"}
            db_work.save_top(product)
            products.append(product)
            count += 1
        return products