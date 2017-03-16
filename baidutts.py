import requests
import logging as log


URL_TOKEN = "https://openapi.baidu.com/oauth/2.0/token?\
  grant_type=client_credentials&client_id={}&\
  client_secret={}&"

URL_TARGET = "http://tsn.baidu.com/text2audio"


# default settings
LAN = "zh"
CTP = 1 # client type, web = 1
CUID = None # client user id
SPD = 5 # speed: 0-9
PIT = 5 # pitch: 0-9
VOL = 5 # volumn: 0-9
PERSON = 1 # 发音人选择，取值 0-1 ;0 为女声，1 为男声，默认为女声


def t2a(tex, tok, lan=LAN, cuid=CUID, ctp=CTP, spd=SPD, pit=PIT, per=PERSON, vol=VOL):
  assert len(tex) > 0
  # make sure tex is less than 1024 bites
  assert len(tex.encode("utf-8")) < 1024

  payload = {
    "tex": tex,
    "lan": lan,
    "cuid": cuid,
    "ctp": ctp,
    "spd": spd,
    "pit": pit,
    "per": per,
    "vol": vol,
    "tok": tok,
  }
  # data will automatically be form-encoded when the request is made
  rr = requests.post(URL_TARGET, data=payload)
  if rr.status_code == 500:
    print("不支持输入")
  else if rr.status_code == 501:
    print("输入参数不正确")
  else if rr.status_code == 502:
    print("token 验证失败")
  else if rr.status_code == 503:
    print("合成后端错误")

  ctype = rr.headers["content-type"]
  print('response type: {}'.print(ctype))
  if ctype.find("audio"):
    print("deal with raw audio file")
  else if ctype.find("json"):
    print("show response error: {}".format(rr.text))


def get_access_token(id, secret):
  """
  {
  6. "access_token": "1.a6b7dbd428f731035f771b8d*******",
  7. "expires_in": 86400,
  8. "refresh_token": "2.385d55f8615fdfd9edb7c4b******",
  9. "scope": "public",
  10. "session_key": "ANXxSNjwQDugf8615Onqeik********CdlLx n",
  11. "session_secret": "248APxvxjCZ0VEC********aK4oZExMB ",
  12. }
  """
  url = URL_TOKEN.format(id, secret)
  r = requests.get(url)
  return r.json()




if __name__ = "__main__":
  log.basicConfig(level=logging.DEBUG)
  log.info("Started")

