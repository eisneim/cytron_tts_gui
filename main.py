import tkinter as tk
import threading
import queue
import sys
import os
import logging

import random
import time

from config import CytronConfig
import cytronui as cui
# from baidutts import Baidutts
from actionHandlers import handlers

# ----------- configure logging ---------
log = logging.getLogger("cytron")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# %(name)s -
formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
ch.setFormatter(formatter)

log.addHandler(ch)
# ------  end of configure logging ---------

class GuiPart:
  def __init__(self, master, ctx, dispatch):
    self.queue = ctx.queue
    self.master = master

    master.title("Simple TTS")
    master.configure(bg="red")

    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)


    # container = tk.Frame(master)
    # container.pack(side="top", fill="both", expand=True)
    # container.grid_rowconfigure(0, weight=1)
    # container.grid_columnconfigure(0, weight=1)

    # set up ui
    self.cytronUI = cui.CytronTTS(master, ctx)

  def processIncoming(self):
    """Handle all messages currently in the queue, if any."""
    while self.queue.qsize():
      try:
        msg = self.queue.get(0)
        # Check contents of message and do whatever is needed. As a
        # simple test, print it (in real life, you would
        # suitably update the GUI's display in a richer fashion).
        # print(msg)
        self.cytronUI.receive(msg)

      except queue.Empty:
        # just on general principles, although we don't
        # expect this branch to be taken in this case
        pass


class ThreadedClient:
  """
  Launch the main part of the GUI and the worker thread. periodicCall and
  endApplication could reside in the GUI part, but putting them here
  means that you have all the thread controls in a single place.
  """
  def __init__(self, root):
    """
    Start the GUI and the asynchronous threads. We are in the main
    (original) thread of the application, which will later be used by
    the GUI as well. We spawn a new thread for the worker (I/O).
    """
    self.root = root
    self.queue = queue.Queue()

    self.config = CytronConfig()

    # setup the GUI part
    self.gui = GuiPart(root, self, self.dispatch)

    # Set up the thread to do asynchronous I/O
    # More threads can also be created and used, if necessary
    self.running = True

    # self.thread1 = threading.Thread(target=self.workerThread1)
    # self.thread1.start()

    # Start the periodic call in the GUI to check if the queue contains
    # anything
    self.periodicCall()

  def dispatch(self, action):
    atype = action["type"]
    print("action type: {}".format(atype))
    if atype in handlers:
      fn = handlers[atype]
      # create a new thread for this handler
      tt = threading.Thread(target=fn, args=(self, action["payload"], action))
      tt.start()
    else:
      log.info("unhandled Action type: {}".format(action))


  def periodicCall(self):
    """
    Check every 200 ms if there is something new in the queue.
    """
    self.gui.processIncoming()
    if not self.running:
      # This is the brutal stop of the system. You may want to do
      # some cleanup before actually shutting it down.
      sys.exit(1)

    self.root.after(200, self.periodicCall)

  def workerThread1(self):
    """
    This is where we handle the asynchronous I/O. For example, it may be
    a 'select(  )'. One important thing to remember is that the thread has
    to yield control pretty regularly, by select or otherwise.
    """
    while self.running:
      # To simulate asynchronous I/O, we create a random number at
      # random intervals. Replace the following two lines with the real
      # thing.
      time.sleep(random.random() * 1.5)
      msg = {
        "type": "RAND_NUM",
        "payload": random.random(),
      }
      self.queue.put(msg)

  def endApplication(self):
    self.running = 0




root = tk.Tk()
client = ThreadedClient(root)

root.mainloop()




