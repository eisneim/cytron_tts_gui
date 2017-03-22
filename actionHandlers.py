from baidutts import Baidutts
import time
import shutil

ttsInstance = None


def end_app(ctx, payload, _):
  ctx.running = 0


def get_token(ctx, payload, action):
  global ttsInstance
  ttsInstance = Baidutts(payload["appid"], payload["appsecret"])

  err, data = ttsInstance.get_access_token()
  if err:
    ctx.queue.put({
      "type": "GET_TOKEN_ERROR",
      "payload": err
    })
  else:
    # save appid and secret
    ctx.config.set("appid", payload["appid"])
    ctx.config.set("appsecret", payload["appsecret"])
    ctx.config.set("token", data["access_token"])
    expireTime = time.time() + data["expires_in"]
    ctx.config.set("expireTime", expireTime)
    # save to local file
    ctx.config.save()

    ctx.queue.put({
      "type": "GET_TOKEN",
      "payload": data,
    })


def postRequest(ctx, payload, action):
  global ttsInstance
  if not ttsInstance:
    ttsInstance = Baidutts(ctx.config.get("appid"), ctx.config.get("appsecret"))

  token = ctx.config.get("token")
  cuid = ctx.config.get("cuid")
  err, res = ttsInstance.t2a(payload["text"],
    token,
    cuid=cuid,
    spd=payload["spd"],
    pit=payload["pit"],
    per=payload["per"],
    vol=payload["vol"])
  if err:
    ctx.queue.put({
      "type": "POST_REQUEST_ERROR",
      "payload": err,
    })
  # should save to mp3 file
  with open("test.mp3", "wb") as fout:
    # res.raw.decode_content = True
    shutil.copyfileobj(res.raw, fout)

  ctx.queue.put({
    "type": "POST_REQUEST",
    "payload": res,
  })






handlers = {
  "END_APP": end_app,
  "GET_TOKEN": get_token,
  "POST_REQUEST": postRequest,
}