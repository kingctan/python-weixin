# -*- coding: utf-8 -*-


from weixin.client import WeixinAPI
from weixin.oauth2 import OAuth2AuthExchangeError

APP_ID = 'wxbdc5610cc59c1631'
APP_SECRET = 'your app secret'
REDIRECT_URI = 'https://passport.yhd.com/wechat/callback.do'


code = '021b66a31b7179822b01e7e2c12528cV'

api = WeixinAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)

try:
    print api.get_authorize_login_url(scope=("snsapi_login",))
    print api.exchange_code_for_access_token(code=code)
except OAuth2AuthExchangeError, e:
    print e


access_token = ''

api = WeixinAPI(access_token=access_token)
r = api.user(openid='')
