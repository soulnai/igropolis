# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'avasilyev2'
import db_work
import pymongo
import datetime
import time

now = datetime.datetime.now()
from pymongo import MongoClient
client = MongoClient('mongodb://admin:admin99pass@ds062807.mongolab.com:62807/games')

db = client['games']
collection = db['desktop_temp']

#collection.remove({"shop":"toplay"})
collection.update({},{"$set": {"date":"23/02/2015"}}, multi=True)