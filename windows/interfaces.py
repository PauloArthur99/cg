import tkinter as tk
import windows.functions as wf
from tkinter import Entry, PhotoImage, ttk
from graphic_objects.shapes import *
from utils.tk_adaptations import *
from utils.helper import *
from utils.obj_helper import *


class SecondWindow(tk.Toplevel):
	def __init__(self, mainwindow, title_text):
		self.mainwindow = mainwindow # root
		self.title_text = title_text # window title
		self.is_opened = False       # is the window opened?
		self.initiated = False       # has the window already been built?
	
	def destroy(self):
		# destroy the window (forget structure)
		super().destroy()
		self.initiated = False

	@abstractclassmethod
	def _init_ui(self):
		pass

	def initiate(self):
		# create second window
		super().__init__()

		# set title
		self.title(self.title_text)
		
		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		self.mainframe.grid(row = 0, column = 0)

		# build user interface
		self._init_ui()

		# window is not resizable
		self.wm_resizable(False, False)

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

class ToolTip:
	def __init__(self, mainwindow, widget, text):
		self.mainwindow = mainwindow
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.close)
		self.initiated = False

	def enter(self, event=None):
		# hint mode is not enabled
		if (not self.mainwindow.hint_mode()):
			return
		if (self.initiated):
			# open tip with previous structure
			self.tw.deiconify()
			return

		# not created yet. Build structure
		x, y, cx, cy = self.widget.bbox("insert")
		x += self.widget.winfo_rootx() + 25
		y += self.widget.winfo_rooty() + 20
		# creates a toplevel window
		self.tw = tk.Toplevel(self.widget)
		self.tw["relief"] = "flat"
		# Leaves only the label and removes the app window
		self.tw.wm_overrideredirect(True)
		self.tw.wm_geometry("+%d+%d" % (x, y))
		label = tk.Label(
			self.tw,
			text=self.text,
		)
		label.pack(ipadx=1)
		self.initiated = True

	def close(self, event=None):
		# hint mode is not enabled
		if (not self.mainwindow.show_hints.get()):
			return
		if self.tw:
			# minimize window. Keep structure
			self.tw.withdraw()

class TransformWindowInterface(SecondWindow):
	def __init__(self, mainwindow, title_text = "Transform Object"):
		super().__init__(mainwindow, title_text)
		self.transformations = []

	def _init_ui(self):
		self.__build_fr_translation()
		self.__build_fr_scaling()
		self.__build_fr_rotation()
		self.__build_footer()

	def _update_transformation_label(self):
		self.lb_transformations["text"] = "%d transformations added" % \
			len(self.transformations)
	
	def _add_matrix(self, matrix):
		self.transformations.append(matrix)
		self._update_transformation_label()

	def _reset_transformations(self):
		self.transformations.clear()
		self.transformation_index = None
		self._update_transformation_label()

	def submit(self):
		pass

	def show(self):
		super().show()
		self._reset_transformations()
	
	def hide(self):
		super().hide()
		self._reset_transformations()
	
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
		self.fr_buttons = tk.Frame(self.fr_footer)

		self.lb_transformations = tk.Label(self.fr_footer)

		self.btn_ok = tk.Button(
			self.fr_buttons,
			text = "Ok",
			command = self.submit
		)

		self.btn_add = tk.Button(
			self.fr_buttons,
			text="Add",
			command = self.add
		)

		self.btn_cancel = tk.Button(
			self.fr_buttons,
			text = "Cancel",
			command = self.hide
		)

		self.fr_footer.grid( row = 3, column = 0)
		self.lb_transformations.grid(row = 0, column = 0)
		self.fr_buttons.grid(row = 1, column = 0)
		self.btn_ok.grid(    row = 0, column = 0)
		self.btn_add.grid(   row = 0, column = 1)
		self.btn_cancel.grid(row = 0, column = 2)
	
		self._update_transformation_label()

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
		self.lb_isFilled = Label(self.fr_top, text = "Is a filled object")
		self.ent_name  = tk.Entry(self.fr_top)
		self.ent_coord = tk.Entry(self.fr_top)
		self.ent_color = tk.Entry(self.fr_top)
		self.chkclosed = tk.BooleanVar()
		self.chkfilled = tk.BooleanVar()
		self.checkB_isClosed=tk.Checkbutton(self.fr_top,variable=self.chkclosed)
		self.checkB_isFilled=tk.Checkbutton(self.fr_top,variable=self.chkfilled)

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
		self.lb_isFilled.grid(    row = 8, column = 0)
		self.checkB_isFilled.grid(row = 9, column = 0)

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

class NewCurveWindowInterface(SecondWindow):
	def __init__(self, mainwindow, title_text = "New Curve"):
		super().__init__(mainwindow, title_text)
	
	def _init_ui(self):
		self.__build_body()
		self.__build_footer()
	
	def __build_body(self):
		self.fr_body = tk.Frame(self.mainframe)

		self.lb_name  = Label(self.fr_body, text = "Name")
		self.lb_coord = Label(self.fr_body, text = "Coordinates")
		self.lb_color = Label(self.fr_body, text = "Color")

		self.ent_name  = tk.Entry(self.fr_body)
		self.ent_coord = tk.Entry(self.fr_body)
		self.ent_color = tk.Entry(self.fr_body)
		
		self.fr_body.grid(  row = 0, column = 0)
		self.lb_name.grid(  row = 0, column = 0)
		self.ent_name.grid( row = 1, column = 0)
		self.lb_coord.grid( row = 2, column = 0)
		self.ent_coord.grid(row = 3, column = 0)
		self.lb_color.grid( row = 4, column = 0)
		self.ent_color.grid(row = 5, column = 0)
	
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

		self.fr_footer.grid( row = 1, column = 0)
		self.btn_ok.grid(    row = 0, column = 0)
		self.btn_cancel.grid(row = 0, column = 1)

class MainWindowInterface(tk.Tk):
	def __init__(self):
		# create window
		super().__init__()

		# we shouldn't place elements directly in root
		self.mainframe = Frame(self)
		
		# create second windows
		self.new_object_window = wf.NewObjectWindow(mainwindow = self)
		self.new_curve_window = wf.NewCurveWindow(mainwindow = self)
		self.transform_window = wf.TransformWindow(mainwindow = self)

		# create canvas
		self.canvas = wf.Viewport(self.mainframe, mainwindow = self)

		self.obj_helper = Obj_helper(self.canvas)

		# build user interface
		self.__init_ui()
		
		self.mainframe.grid(row = 0, column = 0)
		self.canvas.grid(row = 1, column = 1)
		# window is not resizable
		self.wm_resizable(False, False)
		self.title("SGI")

	def __init_ui(self):
		self.frame_left = Frame(self.mainframe)
		self.frame_commands = Frame(self.frame_left)
		self.frame_zoom = Frame(self.frame_commands)
		self.frame_arrows = Frame(self.frame_commands)
		self.frame_hints = Frame(self.frame_commands)
		self.frame_clipping = Frame(self.frame_commands)
		self.fr_list_box = Frame(self.frame_left)
		self.fr_list_box_commands = Frame(self.fr_list_box)
		
		self.lb_objNames = Label(self.fr_list_box, text = "Object List")
		self.lst_objNames = tk.Listbox(self.fr_list_box, width = 35)

		self.images = {
			1  : PhotoImage(file=Helper.get_image_file("arrow_left.png")),
			2  : PhotoImage(file=Helper.get_image_file("arrow_right.png")),
			3  : PhotoImage(file=Helper.get_image_file("arrow_up.png")),
			4  : PhotoImage(file=Helper.get_image_file("arrow_down.png")),
			5  : PhotoImage(file=Helper.get_image_file("zoom_in.png")),
			6  : PhotoImage(file=Helper.get_image_file("zoom_out.png")),
			7  : PhotoImage(file=Helper.get_image_file("rotate_left.png")),
			8  : PhotoImage(file=Helper.get_image_file("rotate_right.png")),
			9  : PhotoImage(file=Helper.get_image_file("import.png")),
			10 : PhotoImage(file=Helper.get_image_file("export.png")),
		}

		self.lb_hints = Label(self.frame_hints, text = "Show hints")
		self.show_hints = tk.BooleanVar()
		self.chk_hints=tk.Checkbutton(self.frame_hints,variable=self.show_hints)

		self.lb_clipping = Label(self.frame_clipping, text="clipping algorithm")
		self.clipping_type = tk.StringVar()
		self.clipping_combbx = ttk.Combobox(
			self.frame_clipping,
			textvariable= self.clipping_type
		)
		self.clipping_combbx_options = (
			"Cohen Sutherland",
			"Liang-Barsky"
		)
		self.clipping_combbx['values'] = self.clipping_combbx_options
		self.clipping_combbx["state"] = "readonly"
		self.clipping_combbx.bind(
			"<<ComboboxSelected>>", 
			self.__change_clipping_type
		)
		self.clipping_combbx.set(self.clipping_combbx_options[0])

		self.menubar = tk.Menu(self)
		self.file_menu = tk.Menu(self.menubar, tearoff=0)
		self.file_menu.add_command(
			label="Import .obj file",
			command=self._import_objfile
		)
		self.file_menu.add_command(
			label="Export as .obj file",
			command=self._export_objfile
		)
		self.menubar.add_cascade(label="File", menu=self.file_menu)
		self.config(menu=self.menubar)

		self.button_transform = tk.Button(
			self.fr_list_box_commands,
			text = "Transform",
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

		self.button_newcurve = tk.Button(
			self.frame_commands,
			text = "New Curve",
			command = self._new_curve
		)

		self.button_in = tk.Button(
			self.frame_zoom,
			image=self.images[5],
			command = self._zoom_in
		)

		self.button_out = tk.Button(
			self.frame_zoom,
			image=self.images[6],
			command = self._zoom_out
		)

		self.button_up = tk.Button(
			self.frame_arrows,
			image=self.images[3],
			command = self._move_up
		)

		self.button_down = tk.Button(
			self.frame_arrows,
			image=self.images[4],
			command = self._move_down
		)
		self.button_left = tk.Button(
			self.frame_arrows,
			image = self.images[1],
			command = self._move_left
		)
		self.button_right = tk.Button(
			self.frame_arrows,
			image=self.images[2],
			command = self._move_right
		)
		self.button_rot_left = tk.Button(
			self.frame_arrows,
			image=self.images[7],
			command=self._rotate_left
		)
		self.button_rot_right = tk.Button(
			self.frame_arrows,
			image=self.images[8],
			command=self._rotate_right
		)

		ToolTip(self, self.button_up,"moves the window up")
		ToolTip(self, self.button_down, "moves the window down")
		ToolTip(self, self.button_left, "moves the window to the left")
		ToolTip(self, self.button_right, "moves the window to the right")
		ToolTip(self, self.button_in, "zoom in")
		ToolTip(self, self.button_out, "zoom out")
		ToolTip(self, self.button_transform,
			"translate, rotate or scale the selected object"
		)
		ToolTip(self, self.button_newobject, "creates a new object")
		ToolTip(self, self.button_newcurve, "creates a new curve")
		ToolTip(self, self.button_remove, "removes the selected object")
		ToolTip(self, self.button_rot_left, "rotates the window to the left")
		ToolTip(self, self.button_rot_right, "rotates the window to the right")

		self.frame_left.grid(          row = 1, column = 0)
		self.frame_commands.grid(      row = 1, column = 0)
		self.button_newobject.grid(    row = 0, column = 0)
		self.button_newcurve.grid(     row = 1, column = 0)
		self.frame_zoom.grid(          row = 2, column = 0)
		self.button_in.grid(           row = 0, column = 0)
		self.button_out.grid(          row = 0, column = 1)
		self.frame_arrows.grid(        row = 3, column = 0)
		self.fr_list_box.grid(         row = 0, column = 0)
		self.lb_objNames.grid(         row = 0, column = 0)
		self.lst_objNames.grid(        row = 1, column = 0)
		self.fr_list_box_commands.grid(row = 2, column = 0)
		self.button_transform.grid(    row = 0, column = 0)
		self.button_remove.grid(       row = 0, column = 1)
		self.button_up.grid(           row = 0, column = 1)
		self.button_rot_left.grid(     row = 0, column = 0)
		self.button_rot_right.grid(    row = 0, column = 2)
		self.button_left.grid(         row = 1, column = 0, columnspan=2)
		self.button_right.grid(        row = 1, column = 1, columnspan=2)
		self.button_down.grid(         row = 2, column = 1)
		self.frame_hints.grid(         row = 5, column = 0)
		self.lb_hints.grid(            row = 0, column = 0)
		self.chk_hints.grid(           row = 0, column = 1)
		self.frame_clipping.grid(      row = 4, column = 0)
		self.lb_clipping.grid(         row = 0, column = 0)
		self.clipping_combbx.grid(     row = 0, column = 1)

	def hint_mode(self):
		# is hint mode enabled?
		return self.show_hints.get()

	def __change_clipping_type(self, arg=None):
		if (self.clipping_combbx.get() == self.clipping_combbx_options[0]):
			self.canvas.clipping_function = Clipper.cohen_sutherland
		elif (self.clipping_combbx.get() == self.clipping_combbx_options[1]):
			self.canvas.clipping_function = Clipper.liang_barsky

	def _new_object(self):
		pass
	
	def _transform_object(self):
		pass
	
	def _remove_object(self):
		pass
	
	def _import_objfile(self):
		pass

	def _export_objfile(self):
		pass
