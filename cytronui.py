import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as fdialog
import logging
import time
import os


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
    # self.configure(bg="#efe")
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

    self._text = tk.Text(self, highlightthickness=1, bd=1, bg="#efefef")
    self._text.grid(row=0,
      column=0,
      sticky=tk.N+tk.E+tk.S+tk.W,
      padx=5, pady=5)

    self._text.insert("end", "欲穷千里目，更上一层楼")

    # --------------- second column -----
    _rightSection = tk.Frame(self)
    _rightSection.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S)

    self._file = tk.Button(_rightSection,
      text="select text file",
      command=self.addTextFromFile)
    self._file.grid(row=0)

    self._destFolder = tk.Button(_rightSection,
      text="dest folder",
      command=self.setDestFolder)
    self._destFolder.grid(row=1)

    self._destFolderEntry = tk.Entry(_rightSection, width=15)
    self._destFolderEntry.grid(row=2)
    # set default dest folder to downloads if not on windows
    if os.name != "nt":
      home = os.path.expanduser("~")
      self.dirPath = os.path.join(home, "Downloads")
      self._destFolderEntry.insert(0, self.dirPath)

    _lframe = tk.LabelFrame(_rightSection, text="Audio Setting")
    _lframe.grid(row=3)

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
    self._per.set(1)
    tk.Radiobutton(_lframe, text="Female",
      value=0,
      variable=self._per).grid(row=6)
    tk.Radiobutton(_lframe, text="Male",
      value=1,
      variable=self._per).grid(row=6, column=1)

    # -=----------

    self._confirm = tk.Button(_rightSection,
      text="Generate Mp3", command=self.sendReuqest)
    self._confirm.grid(row=4, sticky="s", pady=5)
    # notify text
    self._sendingLabel = tk.Label(_rightSection, text="Requesting...")
    self._sendingLabel.grid(row=5)
    self._sendingLabel.grid_remove()

  def showRequesting(self, isDone=False):
    if not isDone:
      self._sendingLabel.grid()
      self._confirm.grid_remove()
    else:
      self._sendingLabel.grid_remove()
      self._confirm.grid()

  def setDestFolder(self):
    dirPath = fdialog.askdirectory()
    if not dirPath:
      return
    log.debug("set destDir: {}".format(dirPath))
    self._destFolderEntry.delete(0, "end")
    self._destFolderEntry.insert(0, dirPath)
    self.dirPath = dirPath

  def addTextFromFile(self):
    filePath = fdialog.askopenfilename()
    if not filePath:
      return
    log.debug("input text file: {}".format(filePath))
    with open(filePath, "r") as fin:
      text = fin.read()
    self._text.insert("end", text)

  def sendReuqest(self):
    # http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
    # line 1, 0 char; The -1c deletes 1 character; end contains a new line char
    text = self._text.get("1.0", 'end-1c')
    if not text or len(text) < 1:
      messagebox.showerror("error", "text input is required")
      return
    # make sure dest folder is set
    if not hasattr(self, "dirPath"):
      messagebox.showerror("error", "please set destination folder first")
      return

    # read all settings
    spd = self._spd.get()
    pit = self._pit.get()
    vol = self._vol.get()
    per = self._per.get()
    log.debug("text len: {} spd:{} pid:{} vol:{} per:{}".format(
      len(text), spd, pit, vol, per))

    action = {
      "type": "POST_REQUEST",
      "payload": {
        "text": text,
        "spd": spd,
        "pit": pit,
        "vol": vol,
        "per": per,
        "dest": self.dirPath,
      }
    }
    self.controller.dispatch(action)
    self.showRequesting()
