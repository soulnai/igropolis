# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collect import db_work

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

import collect.db_work


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class CatalogPage(BasePage):

    def check_if_available(self, prod):
        try:
            av = prod.find_element_by_xpath(".//div/div[2]/span/a/span")
        except NoSuchElementException:
            return ""
        return av.text

    def get_products(self):
        products = []
        prods = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'game')))
        for prod in prods:
            players = prod.find_element_by_xpath(".//div/ul/li").text
            if "-" in players:
                players_min_max = players.split("-")
                players_min = CatalogPage.only_numerics(self, players_min_max[0])
                players_max = CatalogPage.only_numerics(self, players_min_max[1])
            else:
                players_min = CatalogPage.only_numerics(self, players)
                players_max = CatalogPage.only_numerics(self, players)

            time = prod.find_element_by_xpath(".//div/ul/li[5]").text
            if "-" in time:
                time_min_max = time.split("-")
                time_min = CatalogPage.only_numerics(self, time_min_max[0])
                time_max = CatalogPage.only_numerics(self, time_min_max[1])
            else:
                time_min = CatalogPage.only_numerics(self, time)
                time_max = CatalogPage.only_numerics(self, time)
            product = {"name": prod.find_element_by_xpath(".//a").text,
                       "image": prod.find_element_by_xpath(".//div/div[4]/a/img").get_attribute("src"),
                       "genre": CatalogPage.check_if_available(self, prod),
                       "players min": players_min,
                       "players max": players_max,
                       "age": CatalogPage.only_numerics(self, prod.find_element_by_xpath(".//div/ul/li[3]").text),
                       "rules": CatalogPage.only_numerics(self, prod.find_element_by_xpath(".//div/ul/li[4]").text),
                       "time min": time_min,
                       "time max": time_max,
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href")}
            db_work.save_to_db(product)
            products.append(product)
        return products

    def next_page(self):
        next_page = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@src='/img/br.gif']")))
        next_page.click()
        time.sleep(3)

    def check_next_page_exists(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@src='/img/br.gif']")))
        except NoSuchElementException:
            return False
        return True

    def only_numerics(self, seq):
        return filter(type(seq).isdigit, seq)