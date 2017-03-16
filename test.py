from tkinter import *

class Application(Frame):
  def say_hi(self):
    print("hi there, everyone")

  def createWidgets(self):
    self.QUIT = Button(self)
    self.QUIT["text"] = "QUIT"
    self.QUIT["fg"] = "green"
    self.QUIT["command"] = self.quit

    self.QUIT.pack({"side": "left"})

    self.hithere_ = Button(self)
    self.hithere_["text"] = "Hello"
    self.hithere_["command"] = self.say_hi
    self.hithere_.pack({"side": "left"})

  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.pack()
    self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
