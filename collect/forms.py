# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'avasilyev2'

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class SearchForm(Form):
    search = StringField('Search')
    available = BooleanField('В наличии', default = False)