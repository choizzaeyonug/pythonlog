import requests

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": "665609aea92cb7bb273878834b2ab491",
    "client_secret": "nik4o5TGR78Wt0Zl17SsUPxUtxkbBgeo",   # 반드시 포함
    "redirect_uri": "https://localhost",
    "code": "V6yPY1EAmrp7C9GxLiDu86ouY8l4h69xoCGnHi8EVLPgXu3sBUA0kAAAAAQKDRTdAAABnFGoIOXdCc_9be4aqQ"
}

res = requests.post(url, data=data)
print(res.json())
