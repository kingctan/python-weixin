# -*-coding: utf-8 -*-
# !/usr/bin/env python
from __future__ import unicode_literals

"""
File:   oauth2.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   2015-02-06
Description: Weixin OAuth2
"""


from .json_import import simplejson
from six.moves.urllib.parse import urlencode
import mimetypes
import six

import requests


class OAuth2AuthExchangeError(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        return '%s: %s' % (self, code, self.description)


class OAuth2API(object):
    host = None
    base_path = None
    authorize_url = None
    access_token_url = None
    redirect_uri = None
    # some providers use "oauth_token"
    access_token_field = "access_token"
    protocol = "https"
    # override with 'Instagram', etc
    api_name = "Generic API"

    def __init__(self, appid=None, client_secret=None, client_ips=None,
                 access_token=None, redirect_uri=None):
        self.appid = appid
        self.client_secret = client_secret
        self.client_ips = client_ips
        self.access_token = access_token
        self.redirect_uri = redirect_uri

    def get_authorize_url(self, scope=None):
        req = OAuth2AuthExchangeRequest(self)
        return req.get_authorize_url(scope=scope)

    def get_authorize_login_url(self, scope=None):
        """ scope should be a tuple or list of requested scope access levels """
        req = OAuth2AuthExchangeRequest(self)
        return req.get_authorize_login_url(scope=scope)

    def exchange_code_for_access_token(self, code):
        req = OAuth2AuthExchangeRequest(self)
        return req.exchange_for_access_token(code=code)
