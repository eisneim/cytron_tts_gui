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


handlers = {
  "GET_TOKEN_ERROR": get_token_err,
  "GET_TOKEN": get_token,
}