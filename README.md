# python-weixin
======
A Python client for the Weixin REST APIs

# Installation

TODO

# Requires
-----
* requests
* simplejson
* six


# Authentication
-----

Weixin API uses the OAuth2 protocol for authentication, but not all functionality requires authentication.
See the docs for more information: https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&lang=zh_CN


### Authenticating a user

(TODO)The provided sample app shows a simple OAuth flow for authenticating a user and getting an access token for them.


### Using an access token

Once you have an access token (whether via the script or from the user flow), you can  pass that token into the WeixinAPI constructor:

``` python
from weixin.client import WeixinAPI

access_token = "YOUR_ACCESS_TOKEN"
api = WeixinAPI(access_token=access_token)
```

