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


import requests
from six.moves.urllib.parse import urlencode


from .json_import import simplejson
from .helper import error_parser, get_encoding


class OAuth2AuthExchangeError(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.code, self.description)


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

    def __init__(self, appid=None, app_secret=None, client_ips=None,
                 access_token=None, redirect_uri=None):
        self.appid = appid
        self.app_secret = app_secret
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


class OAuth2AuthExchangeRequest(object):
    def __init__(self, api):
        self.api = api

    def _url_for_authorize(self, scope=None):
        client_params = {
            "appid": self.api.appid,
            "response_type": "code",
            "redirect_uri": self.api.redirect_uri
        }
        if scope:
            client_params.update(scope=' '.join(scope))
        url_params = urlencode(client_params)
        return "%s?%s" % (self.api.authorize_url, url_params)

    def _data_for_exchange(self, code=None, scope=None):
        app_params = {
            "appid": self.api.appid,
            "secret": self.api.app_secret,
            "redirect_uri": self.api.redirect_uri,
            "grant_type": "authorization_code"
        }
        if code:
            app_params.update(code=code)
            if scope:
                app_params.update(scope=' '.join(scope))
        url_params = urlencode(app_params)
        return "%s?%s" % (self.api.access_token_url, url_params)

    def get_authorize_url(self, scope=None):
        return self._url_for_authorize(scope=scope)

    def get_authorize_login_url(self, scope=None):
        url = self._url_for_authorize(scope=scope)
        response = requests.get(url)
        headers = response.headers
        if int(headers.get('content-length', 384)) < 500:
            # 微信 参数错误返回html页面 http 状态码也是200
            # 暂时只能根据数据大小判断
            encoding = get_encoding(headers=headers)
            error_data = error_parser(response.content, encoding)
            if error_data:
                raise OAuth2AuthExchangeError(
                    error_data.get("errcode", ""),
                    error_data.get("errmsg", ""))
        return url

    def exchange_for_access_token(self, code=None, scope=None):
        access_token_url = self._data_for_exchange(code, scope=scope)
        response = requests.get(access_token_url)
        parsed_content = simplejson.loads(response.content.decode())
        if parsed_content.get('errcode', None):
            raise OAuth2AuthExchangeError(
                parsed_content.get("errcode", ""),
                parsed_content.get("errmsg", ""))
        return parsed_content
