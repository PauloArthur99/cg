import tkinter as tk

class Frame(tk.Frame):
	def __init__(self, master, padx = 10, pady = 10, *args, **kwargs):
		super().__init__(master = master, padx = padx, pady = pady, *args, **kwargs)

class Label(tk.Label):
	def __init__(self, master, padx = 10, pady = 10, *args, **kwargs):
		super().__init__(master = master, padx = padx, pady = pady, *args, **kwargs)

class Button(tk.Button):
	def __init__(self, master, padx = 10, pady = 10, *args, **kwargs):
		super().__init__(master = master, padx = padx, pady = pady, *args, **kwargs)