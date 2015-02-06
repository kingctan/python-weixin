# -*- coding: utf-8 -*-


from weixin.client import WeixinAPI

APP_ID = 'wxbdc5610cc59c1631'
APP_SECRET = 'your app secret'
REDIRECT_URI = 'https://passport.yhd.com/wechat/callback.do'

code = ''

api = WeixinAPI(appid=APP_ID,
                client_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)

print api.get_authorize_url(scope=("snsapi_login",))
print api.exchange_code_for_access_token(code=code)
