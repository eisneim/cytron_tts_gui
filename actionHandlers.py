from baidutts import Baidutts

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
    ctx.queue.put({
      "type": "GET_TOKEN",
      "payload": data
    })


handlers = {
  "END_APP": end_app,
  "GET_TOKEN": get_token,
}