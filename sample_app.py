from flask import Flask
from flask import Markup
from flask import redirect
from flask import request
from flask import jsonify

from weixin.client import WeixinAPI
from weixin.oauth2 import OAuth2AuthExchangeError

app = Flask(__name__)

APP_ID = 'wx6d8c79fb64de6c08'
APP_SECRET = '8ea887f70c67b682c62676e1b5f01c49'
REDIRECT_URI = 'http://localhost.com/authorization'


@app.route("/authorization")
def authorization():
    code = request.args.get('code')
    api = WeixinAPI(appid=APP_ID,
                    app_secret=APP_SECRET,
                    redirect_uri=REDIRECT_URI)
    auth_info = api.exchange_code_for_access_token(code=code)
    api = WeixinAPI(access_token=auth_info['access_token'])
    resp = api.user(openid=auth_info['openid'])
    return jsonify(resp)


@app.route("/login")
def login():
    api = WeixinAPI(appid=APP_ID,
                    app_secret=APP_SECRET,
                    redirect_uri=REDIRECT_URI)
    redirect_uri = api.get_authorize_login_url(scope=("snsapi_login",))
    return redirect(redirect_uri)


@app.route("/")
def hello():
    return Markup('<a href="%s">weixin login!</a>') % '/login'

if __name__ == "__main__":
    app.run(debug=True)
