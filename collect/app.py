# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'avasilyev2'

import db_work
import forms
from flask import Flask, jsonify
import json
from bson import json_util
from bson.json_util import dumps
from flask import render_template, flash, redirect, request, send_from_directory
from forms import SearchForm
import re
import os
import math
import urllib


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('search_results?search_string='+form.search.data+"&av="+str(form.available.data))
    to_print = db_work.output_from_db()
    news = db_work.news_output_from_db()
    news_count = db_work.news_count()
    pages_count = range(int(math.ceil(news_count/24))+1)
    top1 = db_work.top_output_from_db()
    top2 = db_work.top2_output_from_db()
    browser = request.user_agent.browser
    version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
    platform = request.user_agent.platform
    uas = request.user_agent.string
    if browser and version:
        if platform == 'android' or (platform == 'windows' and re.search('Windows Phone', uas)):
            return render_template('index_mobile.html', outs = to_print, news=news, form = form, pages_count=pages_count)
    return render_template("index_mobile.html", outs = to_print, news=news, top1=top1, top2=top2, form = form, pages_count=pages_count)

@app.route('/index_mobile.html', methods = ['GET', 'POST'])
def index_m():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('search_results?search_string='+form.search.data+"&av="+str(form.available.data))
    to_print = db_work.output_from_db()
    news = db_work.news_output_from_db()
    news_count = db_work.news_count()
    pages_count = range(int(math.ceil(news_count/24))+1)
    top1 = db_work.top_output_from_db()
    top2 = db_work.top2_output_from_db()
    browser = request.user_agent.browser
    version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
    platform = request.user_agent.platform
    uas = request.user_agent.string
    return render_template('index_mobile.html', outs = to_print, news=news, form = form, pages_count=pages_count)


@app.route('/news/<int:page>', methods = ['GET', 'POST'])
def news_pages(page):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('search_results?search_string='+form.search.data+"&av="+str(form.available.data))
    to_print = db_work.output_from_db()
    news = db_work.news_output_by_pages(page)
    news_count = db_work.news_count()
    pages_count = range(int(math.ceil(news_count/24))+1)
    top1 = db_work.top_output_from_db()
    top2 = db_work.top2_output_from_db()
    return render_template("index.html", outs = to_print, news=news, top1=top1, top2=top2, form = form, pages_count=pages_count)

@app.route('/all_news', methods = ['GET', 'POST'])
def all_news():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('search_results?search_string='+form.search.data+"&av="+str(form.available.data))
    to_print = db_work.output_from_db()
    news = db_work.all_news()
    news_count = db_work.news_count()
    pages_count = range(int(math.ceil(news_count/24))+1)
    top1 = db_work.top_output_from_db()
    top2 = db_work.top2_output_from_db()
    return render_template("index.html", outs = to_print, news=news, top1=top1, top2=top2, form = form, pages_count=pages_count)

@app.route('/search', methods = ['GET', 'POST'])
def login():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('search_results?search_string='+form.search.data+"&av="+str(form.available.data))
    return render_template('search.html',
        title = 'Search',
        form = form)

@app.route('/search_results', methods = ['GET', 'POST'])
def search_results():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('search_results?search_string='+form.search.data+"&av="+str(form.available.data))
    print request.args.get('av')
    search_string = re.escape(request.args.get('search_string'))
    to_print = db_work.search(search_string, request.args.get('av'))
    top1 = db_work.top_output_from_db()
    top2 = db_work.top2_output_from_db()
    shops = db_work.collection_to_show.distinct("shop")
    return render_template("main.html", outs = to_print, top1=top1, top2=top2, form = form, name=request.args.get('search_string'), shoplist = shops)

@app.route('/catalogue', methods = ['GET', 'POST'])
def catalogue():
    top1 = db_work.top_output_from_db()
    top2 = db_work.top2_output_from_db()
    return render_template("catalogue.html", top1=top1, top2=top2)

@app.route('/_search_ajax', methods = ['GET', 'POST'])
def search_university():
    results = db_work.ajax_search_from_db(request.args.get('q'))
    return json.dumps(results)

@app.route('/_search_catalogue_ajax', methods = ['GET', 'POST'])
def search_catalogue_autocomplete():
    results = db_work.ajax_catalogue_search_from_db(request.args.get('q'))
    return json.dumps(results)

@app.route('/ajax_source', methods = ['GET', 'POST'])
def search_source():
    results = db_work.search_catalogue("")
    json = list(results)
    json_return = '{"aaData":'+dumps(json)+'}'
    print dumps(json)
    return json_return

@app.route('/ajax_source_prices', methods = ['GET', 'POST'])
def search_source_prices():
    order = []
    order_dict = {'asc': 1, 'desc': -1}
    columns = ['name', 'image', 'price', 'availability', 'shop']
    if (request.values['mDataProp_0'] != "" ) and (request.values['iSortingCols'] > 0 ):
        order = []
        for i in range( int(request.values['iSortingCols']) ):
            order.append((columns[ int(request.values['iSortCol_'+str(i)]) ], order_dict[request.values['sSortDir_'+str(i)]]))

    filter_ = {}
    or_filter_on_all_columns = []
    if (request.values.has_key('sSearch') ) and (request.values['sSearch'] != "" ):
        column_filter = {}
        column_filter[columns[0]] = {"$regex": re.escape(request.values['sSearch']), "$options": "i"}
        or_filter_on_all_columns.append(column_filter)
        filter_["$and"] = or_filter_on_all_columns
    if (request.values.has_key('q') ) and (request.values['q'] != "" ):
        column_filter = {}
        column_filter[columns[0]] = {"$regex": re.escape(request.values['q']), "$options": "i"}
        or_filter_on_all_columns.append(column_filter)
        filter_["$and"] = or_filter_on_all_columns
    if (request.values.has_key('sSearch_3') ) and (request.values['sSearch_3'] != "" ):
        column_filter = {}
        bool_val = False
        if request.values['sSearch_3'] == 'true':
            bool_val = True
        elif request.values['sSearch_3'] == 'false':
            bool_val = False
        column_filter[columns[3]] = bool_val
        or_filter_on_all_columns.append(column_filter)
        filter_["$and"] = or_filter_on_all_columns

    if (request.values.has_key('sSearch_4') ) and (request.values['sSearch_4'] != "" ):
        column_filter = {}
        column_filter[columns[4]] = {"$regex": request.values['sSearch_4'], "$options": "i"}
        or_filter_on_all_columns.append(column_filter)
        filter_["$and"] = or_filter_on_all_columns

    print filter_
    results = db_work.ajax_search_main_from_db(request.args.get('q'), request.values['iDisplayStart'], request.values['iDisplayLength'], order, filter_)

    json_ = list(results)
    rows_count = db_work.all_records_count()
    filtered_rows_count = db_work.all_filtered_records_count(request.args.get('q'), order, filter_)

    output = {}
    output['sEcho'] = str(int(request.values['sEcho']))
    output['iTotalRecords'] = str(rows_count)
    output['iTotalDisplayRecords'] = str(filtered_rows_count)
    aaData_rows = json_
    output['aaData'] = aaData_rows
    return dumps(output)

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/price_chart', methods = ['GET', 'POST'])
def chart():
    game_name = urllib.unquote(request.args.get('game'))
    print game_name
    shop = re.escape(request.args.get('shop'))
    items = db_work.get_all_collections(game_name, shop)
    prices = []
    dates = []
    name = ''
    for item in items:
        if ("date" in item):
            prices.append(item["price"])
            dates.append(item["date"])
            name = item["name"]
    return render_template("price-chart.html", prices = prices, dates = dates, name = name)