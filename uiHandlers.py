import tkinter as tk
from tkinter import messagebox
import logging

log = logging.getLogger("cytron")


def get_token(ctx, payload, msg):
  log.info("get token success: {}".format(payload["access_token"]))
  ctx.show_frame("MainPage")


def get_token_err(ctx, payload, msg):
  messagebox.showerror("error", payload)
  ctx.frames["ConfigPage"]._confirm.grid()


handlers = {
  "GET_TOKEN_ERROR": get_token_err,
  "GET_TOKEN": get_token,
}