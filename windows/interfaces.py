import tkinter as tk
import windows.functions as wf
from tkinter import ttk
from graphic_objects.shapes import *
from utils.tk_adaptations import *


class SecondWindow(tk.Toplevel):
	def __init__(self, mainwindow, title_text):
		self.mainwindow = mainwindow
		self.title_text = title_text
		self.is_opened = False
		self.initiated = False
	
	def destroy(self):
		super().destroy()
		self.initiated = False

	@abstractclassmethod
	def _init_ui(self):
		pass

	def initiate(self):
		# create second window
		super().__init__()
		self.title(self.title_text)
		
		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		self.mainframe.grid(row = 0, column = 0)

		# build user interface
		self._init_ui()

		# set window as initiated
		self.initiated = True

	def show(self):
		# not created yet
		if (not self.initiated):
			self.initiate()
		# window is opened. Close and open again (to take focus).
		elif (self.is_opened):
			self.hide()
			super().deiconify()
		else:
			# open window with previous structure
			super().deiconify()

		self.is_opened = True

	def hide(self):
		# minimize window. Keeps structure
		super().withdraw()
		self.is_opened = False

class TransformWindowInterface(SecondWindow):
	def __init__(self, mainwindow, title_text = "Transform Object"):
		super().__init__(mainwindow, title_text)

	def _init_ui(self):
		self.__build_fr_translation()
		self.__build_fr_scaling()
		self.__build_fr_rotation()
		self.__build_footer()

	def submit(self):
		pass

	def __change_fr_translation(self):
		if (self.translate.get()):
			self.trans_ent.config(state = "normal")
		else:
			self.trans_ent.config(state = "disable")
	
	def __change_fr_scaling(self):
		if (self.scale.get()):
			self.scal_ent.config(state = "normal")
		else:
			self.scal_ent.config(state = "disable")
		
	def __change_fr_rotation(self):
		self.rot_combbx.set(self.rot_combbx_options[0])
		if (self.rotate.get()):
			self.rot_ent_angle["state"] = "normal"
			self.rot_combbx["state"] = "readonly"
		else:
			self.rot_ent_angle["state"] = "disable"
			self.rot_combbx["state"] = "disabled"
			self.__change_rot_type()
	
	def __change_rot_type(self, arg = None):
		if (self.rot_combbx.get() == self.rot_combbx_options[2]):
			self.rot_ent_point["state"] = "normal"
		else:
			self.rot_ent_point["state"] = "disable"

	def __build_fr_translation(self):
		self.fr_trans = tk.Frame(self.mainframe)

		self.fr_trans_header = tk.Frame(self.fr_trans)
		self.fr_trans_body = tk.Frame(self.fr_trans)

		self.trans_lb = Label(self.fr_trans_header, text = "Translate")
		self.trans_lb_body = Label(self.fr_trans_body, text = "Vector:")

		self.translate = tk.BooleanVar()
		self.chk_btn_translate = tk.Checkbutton(
			self.fr_trans_header,
			variable=self.translate,
			command = self.__change_fr_translation
		)

		self.trans_ent = tk.Entry(self.fr_trans_body, state = "disable")

		self.fr_trans.grid(       row = 0, column = 0)
		self.fr_trans_header.grid(row = 0, column = 0)
		self.fr_trans_body.grid(  row = 1, column = 0)

		self.trans_lb.grid(         row = 0, column = 0)
		self.chk_btn_translate.grid(row = 0, column = 1)
		self.trans_lb_body.grid(    row = 1, column = 0)
		self.trans_ent.grid(        row = 1, column = 1)

	def __build_fr_scaling(self):
		self.fr_scal = tk.Frame(self.mainframe)

		self.fr_scal_header = tk.Frame(self.fr_scal)
		self.fr_scal_body = tk.Frame(self.fr_scal)

		self.scal_lb = Label(self.fr_scal_header, text = "Scale")
		self.scal_lb_body = Label(self.fr_scal_body, text = "Factor:")

		self.scale = tk.BooleanVar()
		self.chk_btn_scale = tk.Checkbutton(
			self.fr_scal_header,
			variable=self.scale,
			command = self.__change_fr_scaling
		)

		self.scal_ent = tk.Entry(self.fr_scal_body, state="disabled")

		self.fr_scal.grid(       row = 1, column = 0)
		self.fr_scal_header.grid(row = 0, column = 0)
		self.fr_scal_body.grid(  row = 1, column = 0)

		self.scal_lb.grid(      row = 0, column = 0)
		self.chk_btn_scale.grid(row = 0, column = 1)
		self.scal_lb_body.grid( row = 1, column = 0)
		self.scal_ent.grid(     row = 1, column = 1)

	def __build_fr_rotation(self):
		self.fr_rot = tk.Frame(self.mainframe)

		self.fr_rot_header = tk.Frame(self.fr_rot)
		self.fr_rot_body = tk.Frame(self.fr_rot)

		self.rot_lb = Label(self.fr_rot_header, text = "Rotate")
		self.rot_lb_angle = Label(self.fr_rot_body, text = "Angle:")
		self.rot_lb_point = Label(self.fr_rot_body, text = "Point:")

		self.rotate = tk.BooleanVar()
		self.chk_btn_rotate = tk.Checkbutton(
			self.fr_rot_header,
			variable=self.rotate,
			command = self.__change_fr_rotation
		)

		self.rotation_type = tk.StringVar()
		self.rot_combbx = ttk.Combobox(
			self.fr_rot_body,
			textvariable= self.rotation_type
		)
		self.rot_combbx_options = (
			"Object Center",
			"World Center",
			"Arbitrary Point"
		)
		self.rot_combbx['values'] = self.rot_combbx_options
		self.rot_combbx["state"] = "disabled"
		self.rot_combbx.bind("<<ComboboxSelected>>", self.__change_rot_type)

		self.rot_ent_angle = tk.Entry(self.fr_rot_body, state="disabled")
		self.rot_ent_point = tk.Entry(self.fr_rot_body, state="disabled")

		self.fr_rot.grid(        row = 2, column = 0)
		self.fr_rot_header.grid( row = 0, column = 0)
		self.fr_rot_body.grid(   row = 1, column = 0)
		self.rot_lb.grid(        row = 0, column = 0)
		self.chk_btn_rotate.grid(row = 0, column = 1)
		self.rot_combbx.grid(    row = 1, column = 0, columnspan = 2)
		self.rot_lb_angle.grid(  row = 2, column = 0)
		self.rot_ent_angle.grid( row = 2, column = 1)
		self.rot_lb_point.grid(  row = 3, column = 0)
		self.rot_ent_point.grid( row = 3, column = 1)

	def __build_footer(self):
		self.fr_footer = tk.Frame(self.mainframe)

		self.btn_ok = tk.Button(
			self.fr_footer,
			text = "Ok",
			command = self.submit
		)

		self.btn_cancel = tk.Button(
			self.fr_footer,
			text = "Cancel",
			command = self.hide
		)

		self.fr_footer.grid( row = 3, column = 0)
		self.btn_ok.grid(    row = 0, column = 0)
		self.btn_cancel.grid(row = 0, column = 1)

class NewObjectWindowInterface(SecondWindow):
	def __init__(self, mainwindow, title_text = "New Object"):
		super().__init__(mainwindow, title_text)

	def submit(self):
		pass

	def _init_ui(self):
		# build top frame
		self.__build_fr_top()
		# build bottom frame
		self.__build_fr_bottom()

	def __build_fr_top(self):
		# create elements
		self.fr_top   = Frame(self.mainframe)
		self.lb_name  = Label(self.fr_top, text = "Name")
		self.lb_coord = Label(self.fr_top, text = "Coordinates")
		self.lb_color = Label(self.fr_top, text = "Color")
		self.lb_isClosed = Label(self.fr_top, text = "Is a closed object")
		self.ent_name  = tk.Entry(self.fr_top)
		self.ent_coord = tk.Entry(self.fr_top)
		self.ent_color = tk.Entry(self.fr_top)
		self.chkValue = tk.BooleanVar() 
		self.checkB_isClosed = tk.Checkbutton(self.fr_top, variable = self.chkValue)

		# positioning elements
		self.fr_top.grid(         row = 0, column = 0)
		self.lb_name.grid(        row = 0, column = 0)
		self.ent_name.grid(       row = 1, column = 0)
		self.lb_coord.grid(       row = 2, column = 0)
		self.ent_coord.grid(      row = 3, column = 0)
		self.lb_color.grid(       row = 4, column = 0)
		self.ent_color.grid(      row = 5, column = 0)
		self.lb_isClosed.grid(    row = 6, column = 0)
		self.checkB_isClosed.grid(row = 7, column = 0)

	def __build_fr_bottom(self):
		# create bottom frame
		self.fr_bottom = Frame(self.mainframe)

		# create buttons
		self.btn_ok = Button(
			self.fr_bottom,
			text = "Ok",
			command = self.submit
		)
		self.btn_cancel = Button(
			self.fr_bottom,
			text = "Cancel",
			command = self.hide
		)

		# positioning elements
		self.fr_bottom.grid( row = 2, column = 0)
		self.btn_ok.grid(    row = 0, column = 0)
		self.btn_cancel.grid(row = 0, column = 1)

class MainWindowInterface(tk.Tk):
	def __init__(self):
		# create window
		super().__init__()

		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		
		self.new_object_window = wf.NewObjectWindow(mainwindow = self)
		self.transform_window = wf.TransformWindow(mainwindow = self)

		self.canvas = wf.Viewport(self.mainframe, mainwindow = self)

		self.__init_ui()
		
		self.mainframe.grid(row = 0, column = 0)
		self.canvas.grid(row = 0, column = 1)

	def __init_ui(self):
		self.frame_left = Frame(self.mainframe)
		self.frame_commands = Frame(self.frame_left)
		self.frame_zoom = Frame(self.frame_commands)
		self.frame_arrows = Frame(self.frame_commands)
		self.fr_list_box = Frame(self.frame_left)
		self.fr_list_box_commands = Frame(self.fr_list_box)
		
		self.lb_objNames = Label(self.fr_list_box, text = "Object List")
		self.lst_objNames = tk.Listbox(self.fr_list_box, width = 35)

		self.button_transform = tk.Button(
			self.fr_list_box_commands,
			text = "Tansform",
			command	= self._transform_object
		)

		self.button_remove = tk.Button(
			self.fr_list_box_commands,
			text = "Remove",
			command = self._remove_object
		)

		self.button_newobject = tk.Button(
			self.frame_commands,
			text = "New Object",
			command = self._new_object
		)

		self.button_in = tk.Button(
			self.frame_zoom,
			text = "In",
			command = self._zoom_in
		)

		self.button_out = tk.Button(
			self.frame_zoom,
			text = "Out",
			command = self._zoom_out
		)

		self.button_up = tk.Button(
			self.frame_arrows,
			text = "^",
			command = self._move_up
		)

		self.button_down = tk.Button(
			self.frame_arrows,
			text = "v",
			command = self._move_down
		)
		self.button_left = tk.Button(
			self.frame_arrows,
			text = "<",
			command = self._move_left
		)
		self.button_right = tk.Button(
			self.frame_arrows,
			text = ">",
			command = self._move_right
		)

		# positioning elements
		self.frame_left.grid(          row = 0, column = 0)
		self.frame_commands.grid(      row = 1, column = 0)
		self.button_newobject.grid(    row = 0, column = 0)
		self.frame_zoom.grid(          row = 1, column = 0)
		self.button_in.grid(           row = 0, column = 0)
		self.button_out.grid(          row = 0, column = 1)
		self.frame_arrows.grid(        row = 2, column = 0)
		self.fr_list_box.grid(         row = 0, column = 0)
		self.lb_objNames.grid(         row = 0, column = 0)
		self.lst_objNames.grid(        row = 1, column = 0)
		self.fr_list_box_commands.grid(row = 2, column = 0)
		self.button_transform.grid(    row = 0, column = 0)
		self.button_remove.grid(       row = 0, column = 1)
		self.button_up.grid(           row = 0, column = 0, columnspan = 2)
		self.button_left.grid(         row = 1, column = 0)
		self.button_right.grid(        row = 1, column = 1)
		self.button_down.grid(         row = 2, column = 0, columnspan = 2)

	def _new_object(self):
		pass
	
	def _transform_object(self):
		pass
	
	def _remove_object(self):
		pass
