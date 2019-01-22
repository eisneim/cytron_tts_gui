import os
from os.path import join, exists
import json
import uuid
import re

DEFAULTCONF = {
  "token": None,
  "appid": None,
  "appsecret": None,
  "expireTime": 0,
  "cuid": None
}


class CytronConfig:
  def __init__(self):
    self.rootDir = os.path.dirname(os.path.abspath(__file__))
    # check if inside a .app bundle
    match = re.search(r"/[^/]*\.app/", self.rootDir)
    isBundle = False
    if match:
      # '/Users/eisneim/www/pyProject/audioGenerator/python/dist/cytrontts.app/'
      self.rootDir = self.rootDir[0:match.end()]
      self.configPath = join(self.rootDir, "Contents/Resources/config.json")
      isBundle = True
    else:
      # check if config.json exists
      self.configPath = join(self.rootDir, "config.json")

    if not exists(self.configPath):
      self.data = DEFAULTCONF
      # jsonStr = json.dumps(DEFAULTCONF)
    else:
      with open(self.configPath, "r") as fin:
        self.data = json.load(fin)
    # check if cuid is set
    if not self.data["cuid"]:
      # https://docs.python.org/3/library/uuid.html
      self.data["cuid"] = str(uuid.uuid1())

    self.data["isBundle"] = isBundle

  def save(self):
    jsonStr = json.dumps(self.data)
    with open(self.configPath, "w") as fout:
      fout.write(jsonStr)

  def get(self, name):
    return self.data[name]

  def set(self, name, value=None):
    self.data[name] = value
