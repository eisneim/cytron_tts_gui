import tkinter as tk
from tkinter import messagebox
import logging

log = logging.getLogger("cytron")


def get_token(ctrl, payload, msg):
  log.info("get token success: {}".format(payload["access_token"]))
  # should save this token to config
  ctrl.show_frame("MainPage")


def get_token_err(ctrl, payload, msg):
  messagebox.showerror("error", payload)
  ctrl.frames["ConfigPage"]._confirm.grid()


def post_request_error(ctrl, payload, msg):
  log.info("post_request_error: {}".format(payload))
  messagebox.showerror("error", payload)


def post_request_done(ctrl, payload, msg):
  log.info("post_request_done")
  # should restore ui
  ctrl.frames["MainPage"].showRequesting(True)
  messagebox.showinfo("Done", "mp3 file saved in: {}".format(payload["filePath"]))

handlers = {
  "GET_TOKEN_ERROR": get_token_err,
  "GET_TOKEN": get_token,
  "POST_REQUEST_DONE": post_request_done,
  "POST_REQUEST_ERROR": post_request_error,
}