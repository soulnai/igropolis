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

    def get_products(self):
        news = []
        prods = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'newsitem')))
        for prod in prods:
            text_with_date = prod.find_element_by_class_name("texts").text
            date = prod.find_element_by_class_name("date").text
            title = prod.find_element_by_class_name("title").text
            text = text_with_date[len(date):]
            clean_text = text[len(title)+1:]
            print clean_text
            product = {"name": prod.find_element_by_class_name("title").text,
                       "image": prod.find_element_by_xpath(".//img").get_attribute("src"),
                       "link": prod.find_element_by_xpath(".//a").get_attribute("href"),
                       "short_text": clean_text}
            collect.db_work.save_news_to_db(product)
            news.append(product)
        return news
