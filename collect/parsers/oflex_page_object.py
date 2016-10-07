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

    def check_if_img_exists(self, img_root):
        try:
            img_root.find_element_by_xpath(".//img")
        except NoSuchElementException:
            return False
        return True

    def get_products(self):
        news = []
        prods = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'post')))
        for prod in prods:
            text = prod.find_element_by_class_name("entry").text
            short_text = text[:-10]
            img_root = prod.find_element_by_class_name("entry")
            if CatalogPage.check_if_img_exists(self, img_root) == False:
                continue
            product = {"name": prod.find_element_by_tag_name("h2").text,
                       "image": img_root.find_element_by_xpath(".//img").get_attribute("src"),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "short_text": short_text}
            db_work.save_oflex_news_to_db(product)
            news.append(product)
        return news
