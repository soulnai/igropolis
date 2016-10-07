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

    def check_if_available(self, td):
        try:
            td.find_element_by_xpath('.//form')
        except NoSuchElementException:
            return False
        return True

    def get_products(self):
        products = []
        table_root = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div[7]/div/div/div[1]/div/div/div/div/div/div[2]/table/tbody')))
        all_td = table_root.find_elements_by_xpath('.//td')
        for td in all_td:
            if str(td.find_element_by_xpath('.//div/div[2]').get_attribute("class")) == "views-field views-field-sell-price":
                name = td.find_element_by_xpath('.//div/div[3]').text
            else:
                name = td.find_element_by_xpath('.//div/div[4]').text

            if "Пазл" in name or "Раскраска" in name or "Раскраски" in name:
                continue
            price = CatalogPage.only_numerics(self, td.find_element_by_xpath('.//div/div[2]').text)
            link = td.find_element_by_xpath('.//a').get_attribute("href")
            availability = CatalogPage.check_if_available(self, td)
            image = td.find_element_by_xpath('.//img').get_attribute("src")
            product = {"name": name,
                       "image": image,
                       "price": int(price),
                       "availability": availability,
                       "link": link,
                       "shop": "planetaigr"}
            db_work.save_to_db(product)
            products.append(product)
            time.sleep(0.1)

        return products

    def next_page(self):
        next_page = self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='На следующую страницу']")))
        next_page.click()
        time.sleep(3)

    def check_next_page_exists(self):
        try:
            self.driver.find_element_by_xpath("//a[contains(.,'вперед')]")
        except NoSuchElementException:
            return False
        return True

    def only_numerics(self, seq):
        return filter(type(seq).isdigit, seq)

    def get_top(self):
        products = []
        table_root = self.wait.until(EC.presence_of_element_located((By.ID, 'top_games')))
        all_td = table_root.find_elements_by_xpath('.//td')
        for td in all_td:
            name = td.find_element_by_xpath('.//span[3]/span/a').text
            print name
            price = CatalogPage.only_numerics(self, td.find_element_by_xpath('.//span[2]/span').text)
            print price
            link = td.find_element_by_xpath('.//a').get_attribute("href")
            availability = CatalogPage.check_if_available(self, td)
            image = td.find_element_by_xpath('.//img').get_attribute("src")
            product = {"name": name,
                       "image": image,
                       "price": int(price),
                       "availability": availability,
                       "link": link,
                       "shop": "planetaigr"}
            db_work.save_top2(product)
            products.append(product)

        return products