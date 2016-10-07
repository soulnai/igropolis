# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'avasilyev2'
import pymongo
from pymongo import MongoClient
import datetime
import time

now = datetime.datetime.now()


client = MongoClient('mongodb://admin:admin99pass@ds062807.mongolab.com:62807/games')

db = client['games']
collection = db['desktop_temp']
collection.update({},{"$set": {"date":time.strftime("%d/%m/%Y")}}, multi=True)
collection_to_backup = db['general_collection']

collection_to_backup.rename('general_collection'+str(now.day)+str(now.month)+str(now.year))
collection.rename('general_collection')

