import tkinter as tk
import logging

log = logging.getLogger("cytron")

class CytronTTS:
  def __init__(self, master, dispatch):
    # reference to the dispatch function
    self.dispatch = dispatch

    # container.pack(side="top", fill="both", expand=True, bg="#efe")
    _endAction = { "type": "END_APP" }
    uu = tk.Button(master, text="Done", command=lambda: dispatch(_endAction))
    uu.pack(padx=10, pady=10)
    tk.Entry(master).pack()

    # some test
    _hello = { "type": "HELLO" }
    btn = tk.Button(master, text="hello", command=lambda: dispatch(_hello))
    btn.pack()


  def receive(self, msg):
    log.debug("get message from worker: {}".format(msg))










