from baidutts import Baidutts


def end_app(ctx, payload, _):
  ctx.running = 0

def get_token(ctx, payload, action):
  print("should get token")

  ctx.queue.put({
    "type": "GET_TOKEN_ERROR",
    "payload": "invalid appid"
  })


handlers = {
  "END_APP": end_app,
  "GET_TOKEN": get_token,
}