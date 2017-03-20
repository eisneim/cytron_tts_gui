import tkinter as tk
from tkinter import messagebox
import logging
import time

from uiHandlers import handlers

log = logging.getLogger("cytron")


class CytronTTS:
  def __init__(self, master, ctx):
    # reference to the dispatch function
    self.dispatch = ctx.dispatch
    self.ctx = ctx
    # container.pack(side="top", fill="both", expand=True, bg="#efe")
    # _endAction = { "type": "END_APP" }
    # uu = tk.Button(master, text="Done", command=lambda: dispatch(_endAction))
    # uu.pack(padx=10, pady=10)

    self.frames = {}
    pages = (ConfigPage, MainPage)
    for ff in pages:
      frame = ff(master, self)
      # self.frames[ff] = frame
      self.frames[ff.__name__] = frame
      frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

    # check if token expires
    if ctx.config.get("expireTime") > time.time():
      log.info("token not expired, show main page")
      self.show_frame(MainPage)
    else:
      log.info("token expired, show init page")
      self.show_frame(ConfigPage)

  def show_frame(self, cont):
    name = cont if type(cont) == str else cont.__name__
    frame = self.frames[name]
    frame.tkraise()

  def receive(self, msg):
    log.debug("get message from worker: {}".format(msg))
    mtype = msg["type"]
    if mtype in handlers:
      handlers[mtype](self, msg["payload"], msg)
    else:
      log.info("unhandled ui msg: {}".format(msg))


class ConfigPage(tk.Frame):
  def __init__(self, parent, controller):
    self.controller = controller
    tk.Frame.__init__(self, parent)
    self.configure(bg="#efe")
    self.grid_rowconfigure(0, weight=1)
    # self.grid_rowconfigure(1, weight=1)
    # self.grid_rowconfigure(2, weight=1)
    self.grid_rowconfigure(3, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)

    _label = tk.Label(self, text="setting")
    _label.grid(columnspan=2)

    tk.Label(self, text="AppID").grid(row=1, sticky="e")
    tk.Label(self, text="AppSecret").grid(row=2, sticky="e")
    self._appid = tk.Entry(self)
    self._appid.grid(row=1, column=1, sticky="w")

    self._appsecret = tk.Entry(self)
    self._appsecret.grid(row=2, column=1, sticky="w")
    # set default value
    if self.controller.ctx.config.get("appid"):
      self._appid.configure(text=self.controller.ctx.config.get("appid"))
      self._appsecret.configure(text=self.controller.ctx.config.get("appid"))

    self._confirm = tk.Button(self, text="Confirm",
      command=self.getToken)
    self._confirm.grid(row=3, columnspan=2)

  def getToken(self):
    appid = self._appid.get()
    appsecret = self._appsecret.get()

    if not appid or not appsecret:
      messagebox.showerror("error", "appid and app secret is required!\
        go to http://yuyin.baidu.com/ to get appid and secret")
      return

    self.controller.dispatch({
      "type": "GET_TOKEN",
      "payload": {
        "appid": appid, "appsecret": appsecret,
      }
    })
    # hide comfirm button should show load animation
    self._confirm.grid_remove()

class MainPage(tk.Frame):
  def __init__(self, parent, controller):
    self.controller = controller
    tk.Frame.__init__(self, parent)

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self._text = tk.Text(self, highlightthickness=1)
    self._text.grid(row=0,
      column=0,
      sticky=tk.N+tk.E+tk.S+tk.W,
      padx=5, pady=5)


    # --------------- second column -----
    _rightSection = tk.Frame(self)
    _rightSection.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S)

    self._file = tk.Button(_rightSection, text="select .txt file")
    self._file.grid(row=0)

    self._destFolder = tk.Button(_rightSection, text="dest folder")
    self._destFolder.grid(row=1)

    _lframe = tk.LabelFrame(_rightSection, text="Audio Setting")
    _lframe.grid(row=2)

    self._spd = tk.Scale(_lframe, from_=0, to=10, orient="horizontal", label="speed")
    self._spd.set(5)
    self._spd.grid(row=1, columnspan=2)

    self._pit = tk.Scale(_lframe, from_=0, to=10, orient="horizontal", label="pitch")
    self._pit.set(5)
    self._pit.grid(row=3, columnspan=2)

    self._vol = tk.Scale(_lframe, from_=0, to=10, orient="horizontal", label="volume")
    self._vol.set(5)
    self._vol.grid(row=5, columnspan=2)

    self._per = tk.IntVar()
    tk.Radiobutton(_lframe, text="male",
      value=0,
      variable=self._per).grid(row=6)
    tk.Radiobutton(_lframe, text="female",
      value=1,
      variable=self._per).grid(row=6, column=1)

    # -=----------

    self._confirm = tk.Button(_rightSection,
      text="Generate Mp3")
    self._confirm.grid(row=7, sticky="s", pady=5)


