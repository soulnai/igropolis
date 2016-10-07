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
    return render_template("index.html", outs = to_print, news=news, top1=top1, top2=top2, form = form, pages_count=pages_count)

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
    return render_template("main.html", outs = to_print, top1=top1, top2=top2, form = form, name=request.args.get('search_string'))

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
    results = db_work.ajax_search_main_from_db(request.args.get('q'))
    json = list(results)
    json_return = '{"aaData":'+dumps(json)+'}'
    print dumps(json)
    return json_return

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/price_chart', methods = ['GET', 'POST'])
def chart():
    game_name = re.escape(request.args.get('game'))
    shop = re.escape(request.args.get('shop'))
    items = db_work.get_all_collections(game_name, shop)
    prices = []
    dates = []
    for item in items:
        prices.append(item["price"])
        dates.append(item["date"])
        name = item["name"]
    return render_template("price-chart.html", prices = prices, dates = dates, name = name)

if __name__ == '__main__':
    app.run(host="0.0.0.0")