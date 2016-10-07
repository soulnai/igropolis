# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'avasilyev2'

from pymongo import MongoClient
client = MongoClient('mongodb://adm:pass@ds062807.mongolab.com:62807/games')

db = client['games']

collection = db['desktop_temp']
collection_catalogue = db['catalogue_temp']
collection_news = db['temp_news25012015']
collection_oflex_news = db['temp_news25012015']
collection_to_show = db['general_collection']
collection_top = db['hobbyworld_top']
collection_top2 = db['planetaigr_top']

#collection.remove()
#collection_news.remove({})
#collection_top.remove()
#collection_top2.remove()
#collection_oflex_news.remove()

def save_to_db(game_to_save):
    collection.save(game_to_save)

def save_news_to_db(game_to_save):
    old_news = collection_news.find()
    entries = {}
    for news in old_news:
        entries[news['name']] = news
    if len(entries) == 0:
        collection_news.save(game_to_save)
    allow_save = True
    for entry in entries:
        if game_to_save['name'] == entry:
            allow_save = False
            break
    if allow_save:
        collection_news.save(game_to_save)

def save_oflex_news_to_db(news_to_save):
    old_news = collection_oflex_news.find()
    entries = {}
    for news in old_news:
        entries[news['name']] = news
    if len(entries) == 0:
        collection_news.save(news_to_save)
    allow_save = True
    for entry in entries:
        if news_to_save['name'] == entry:
            allow_save = False
            break
    if allow_save:
        collection_oflex_news.save(news_to_save)


def save_top(game_to_save):
    collection_top.save(game_to_save)

def save_top2(game_to_save):
    collection_top2.save(game_to_save)

def output_from_db():
    return collection_to_show.find()

def news_output_from_db():
    return collection_news.find().sort("_id", -1).limit(24)

def all_news():
    return collection_news.find().sort("_id", -1)

def news_count():
    return collection_news.find().count()

def news_output_by_pages(offset):
    return collection_news.find().sort("_id", -1).skip(24*offset).limit(24)

def top_output_from_db():
    return collection_top.find()

def top2_output_from_db():
    return collection_top2.find()

def print_from_db():
    res = []
    for item in collection_to_show.find():
        #print '"'+item["name"]+'"'+","
        res.append(item["availability"])
    return res

def ajax_search_from_db(item_to_search):
    res = []
    for item in collection_to_show.find({"name": {"$regex": item_to_search, "$options": "i"}}):
        res.append(item["name"])
    return res

def ajax_catalogue_search_from_db(item_to_search):
    res = []
    for item in collection_catalogue.find({"name": {"$regex": item_to_search, "$options": "i"}}):
        res.append(item["name"])
    return res

def ajax_search_main_from_db(item_to_search, start_from, show_number, order, filter_):
    if (len(filter_) > 0):
        print filter_
        print "all finded records - " + str(collection_to_show.find(filter_, sort = order).count())
        return collection_to_show.find(filter_, sort = order).skip(int(start_from)).limit(int(show_number))
    else:
        return collection_to_show.find({"name": {"$regex": item_to_search, "$options": "i"}}, sort = order).skip(int(start_from)).limit(int(show_number))

def all_records_count():
        return collection_to_show.find().count()

def all_filtered_records_count(item_to_search, order, filter_):
    if (len(filter_) > 0):
        print filter_
        print collection_to_show.find(filter_, sort = order).count()
        return collection_to_show.find(filter_, sort = order).count()
    else:
        return collection_to_show.find({"name": {"$regex": item_to_search, "$options": "i"}}).count()

def search(item_to_search, available):
    if available == 'True':
        return collection_to_show.find({"name": {"$regex": item_to_search, "$options": "i"}, 'availability':True})
    else:
        return collection_to_show.find({"name": {"$regex": item_to_search, "$options": "i"}})

def search_catalogue(item_to_search):
        return collection_catalogue.find({"name": {"$regex": item_to_search, "$options": "i"}})

def get_all_collections(game_name, shop):
    all = db.collection_names()
    sorted_collection = []
    price_list = []
    for coll in all:
        if 'general_collection' in coll:
            sorted_collection.append(coll)
    for collection in sorted_collection:
        temp_collection = db[collection]
        for item in temp_collection.find(
                {
                    "$and":[
                        {"name": game_name},
                        {"shop": {"$regex": shop}}
                            ]
                }
                ):
            price_list.append(item)
    print price_list
    return price_list