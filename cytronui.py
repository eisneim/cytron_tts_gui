import tkinter as tk
from tkinter import messagebox
import logging

log = logging.getLogger("cytron")


class CytronTTS:
  def __init__(self, master, dispatch):
    # reference to the dispatch function
    self.dispatch = dispatch

    # container.pack(side="top", fill="both", expand=True, bg="#efe")
    # _endAction = { "type": "END_APP" }
    # uu = tk.Button(master, text="Done", command=lambda: dispatch(_endAction))
    # uu.pack(padx=10, pady=10)

    self.frames = {}
    pages = (ConfigPage, MainPage)
    for ff in pages:
      frame = ff(master, self)
      self.frames[ff] = frame
      frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

    self.show_frame(ConfigPage)

  def show_frame(self, cont):
    frame = self.frames[cont]
    frame.tkraise()

  def receive(self, msg):
    log.debug("get message from worker: {}".format(msg))


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
    self._confirm.grid_forget()

class MainPage(tk.Frame):
  def __init__(self, parent, controller):
    self.controller = controller
    tk.Frame.__init__(self, parent)

    label = tk.Label(self, text="Main page")
    label.pack(padx=5, pady=5)

    btn1 = tk.Button(self, text="start page",
      command=lambda: controller.show_frame(ConfigPage))
    btn1.pack()








