from baidutts import Baidutts
import time
import shutil
from os.path import join
import uuid
import re

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


def splitText(text, maxBytes):
  # remove extra newline
  text = re.sub(r"\n+", "\n", text)
  # every chinese char == 3 bytes
  maxChineseChar = maxBytes // 3 + 1
  idx = 0
  parts = []
  while idx < len(text):
    parts.append(text[idx : (idx + maxChineseChar)])
    idx += maxChineseChar
  return parts

def postRequest(ctx, payload, action):
  global ttsInstance
  if not ttsInstance:
    ttsInstance = Baidutts(ctx.config.get("appid"), ctx.config.get("appsecret"))

  token = ctx.config.get("token")
  cuid = ctx.config.get("cuid")
  tex = payload["text"]
  fileName = str(uuid.uuid1()) + ".mp3"
  filePath = join(payload["dest"], fileName)
  # check if text is too long, if so, split it
  if len(tex.encode("utf-8")) < 1024:
    err, res = ttsInstance.t2a(payload["text"],
      token,
      cuid=cuid,
      spd=payload["spd"],
      pit=payload["pit"],
      per=payload["per"],
      vol=payload["vol"])
    if err:
      return (err, False)
    # should save to mp3 file
    # http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    with open(filePath, "wb") as fout:
      # res.raw.decode_content = True
      shutil.copyfileobj(res.raw, fout)
  else:
    textList = splitText(tex, 1024)
    rawResList = []
    for idx, tx in enumerate(textList):
      err, res = ttsInstance.t2a(tx,
        token,
        cuid=cuid,
        spd=payload["spd"],
        pit=payload["pit"],
        per=payload["per"],
        vol=payload["vol"])
      if err:
        return (err, False)
      # save raw resonponse
      rawResList.append(res)
      ctx.queue.put({
        "type": "POST_REQUEST_PROGRESS",
        "payload": (idx + 1) / len(textList),
      })
    # concat all mp3 binary
    with open(filePath, "wb") as fout:
      # res.raw.decode_content = True
      # shutil.copyfileobj(binary, fout)
      for res in rawResList:
        for chunk in res.iter_content(chunk_size=1024):
          fout.write(chunk)

  ctx.queue.put({
    "type": "POST_REQUEST_DONE",
    "payload": {
      "filePath": filePath,
    },
  })



handlers = {
  "END_APP": end_app,
  "GET_TOKEN": get_token,
  "POST_REQUEST": postRequest,
}