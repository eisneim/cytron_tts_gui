import tkinter as tk
import threading
import queue
import sys

import random
import time


class GuiPart:
  def __init__(self, master, appQueue, endCommand):
    self.queue = appQueue
    self.master = master
    # set up ui
    uu = tk.Button(master, text="Done", command=endCommand)
    uu.pack(padx=10, pady=10)
    tk.Entry(master).pack()

  def processIncoming(self):
    """Handle all messages currently in the queue, if any."""
    while self.queue.qsize():
      try:
        msg = self.queue.get(0)
        # Check contents of message and do whatever is needed. As a
        # simple test, print it (in real life, you would
        # suitably update the GUI's display in a richer fashion).
        print(msg)
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
  def __init__(self, master):
    """
    Start the GUI and the asynchronous threads. We are in the main
    (original) thread of the application, which will later be used by
    the GUI as well. We spawn a new thread for the worker (I/O).
    """
    self.master = master
    self.queue = queue.Queue()

    # setup the GUI part
    self.gui = GuiPart(master, self.queue, self.endApplication)

    # Set up the thread to do asynchronous I/O
    # More threads can also be created and used, if necessary
    self.running = True
    self.thread1 = threading.Thread(target=self.workerThread1)
    self.thread1.start()

    # Start the periodic call in the GUI to check if the queue contains
    # anything
    self.periodicCall()

  def periodicCall(self):
    """
    Check every 200 ms if there is something new in the queue.
    """
    self.gui.processIncoming()
    if not self.running:
      # This is the brutal stop of the system. You may want to do
      # some cleanup before actually shutting it down.
      sys.exit(1)

    self.master.after(200, self.periodicCall)

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




