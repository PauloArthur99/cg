import re
import math
import tkinter as tk
import windows.interfaces as wi
from utils.tk_adaptations import *
from graphic_objects.shapes import *
from utils.transformer import *
from utils.helper import *


class MainWindow(wi.MainWindowInterface):
	def __init__(self):
		super().__init__()

		self.canvas.draw()

	def _new_object(self):
		self.new_object_window.show()
	
	def _transform_object(self):
		self.transform_window.show()
	
	def get_selected_object(self):
		index = self.lst_objNames.curselection()
		# must be one and only one object
		if (len(index) != 1): return -1

		return index[0]

	def _remove_object(self):
		index = self.get_selected_object()

		if (index == -1):
			print("No selected object to remove")
			return

		# remove object from object list
		self.canvas.remove_object(index)
		
		# remove object name from list box
		assert(index < self.lst_objNames.size())
		self.lst_objNames.delete(index)

	def _zoom_in(self):
		self.canvas.zoom(self.canvas.delta_zoom)
		
	def _zoom_out(self):
		self.canvas.zoom(1 / self.canvas.delta_zoom)

	def _move_up(self):
		self.canvas.movewin(0, self.canvas.delta_move)
		
	def _move_down(self):
		self.canvas.movewin(0, -self.canvas.delta_move)

	def _move_left(self):
		self.canvas.movewin(-self.canvas.delta_move, 0)

	def _move_right(self):
		self.canvas.movewin(self.canvas.delta_move, 0)

class Viewport(tk.Canvas):
	def __init__(self, master, mainwindow):
		self.mainwindow = mainwindow

		# viewport size
		self.width = 500
		self.height = 500

		# navigation coefitients
		self.delta_move = 30
		self.delta_zoom = 1.4

		# scene scale
		self.imgscale = 1

		# window coordinates
		self.minx = -self.width/2
		self.miny = -self.height/2
		self.maxx = self.width/2
		self.maxy = self.height/2

		self.graphicObjects = []
		self.axis_list = []

		self.graphic_object_creator = GraphicObjectCreator(
			self
		)

		super().__init__(
			master = master,
			bg = "white",
			width = self.width,
			height = self.height,
		)

		self.__create_axis()

	def __create_axis(self):
		axisx = AxisX(
			canvas = self,
			name = "axis-x",
			coords = [
				(-math.inf, 0),
				(math.inf, 0)
			],
			fill = "red"
		)
		axisy = AxisY(
			canvas = self,
			name = "axis-y",
			coords = [
				(0, -math.inf),
				(0, math.inf)
			],
			fill = "green"
		)

		# add axis to the axis_list
		self.axis_list.append(axisx)
		self.axis_list.append(axisy)
		
		self.draw()

	def transform_viewport(self, coords):
		transformed = []
		kx = self.width
		ky = self.height
		tx = (self.maxx-self.minx)
		ty = (self.maxy-self.miny)
		for c in coords:
			x, y = c

			transformed.append(
				(
					(     (x - self.minx) / tx)  * kx,
					(1 - ((y - self.miny) / ty)) * ky
				)
			)

		return transformed
	
	def transform_object(self, index, matrix):
		obj = self.graphicObjects[index]
		obj.transform(matrix)
		self.draw()

	def create_object(self, name, coords, is_closed = False, fill = "black"):
		# create new graphic object
		newGraphicObject = self.graphic_object_creator.create(
			name,
			coords,
			is_closed,
			fill
		)

		# add new object to the list
		self.graphicObjects.append(newGraphicObject)

		# draw new object
		newGraphicObject.draw()

		return newGraphicObject

	def remove_object(self, index):
		assert(index < len(self.graphicObjects))

		self.graphicObjects.pop(index)

		self.draw()

	def draw(self):
		self.delete("all")
		for i in self.axis_list:
			i.draw()
		for i in self.graphicObjects:
			i.draw()
		
	
	def movewin(self, deltax, deltay):
		# update window edges coordinates
		self.maxx += deltax
		self.minx += deltax
		self.maxy += deltay
		self.miny += deltay

		# redraw scene
		self.draw()
	
	def zoom(self, delta):
		rangex = (self.maxx - self.minx) / 2
		rangey = (self.maxy - self.miny) / 2
	
		# get center coordinates
		midlex = (self.maxx + self.minx) / 2
		midley = (self.maxy + self.miny) / 2

		# rearange window position
		self.minx = midlex - (rangex * 1 / delta)
		self.miny = midley - (rangey * 1 / delta)
		self.maxx = midlex + (rangex * 1 / delta)
		self.maxy = midley + (rangey * 1 / delta)

		# update image scale
		self.imgscale *= delta
		# redraw scene
		self.draw()


class NewObjectWindow(wi.NewObjectWindowInterface):
	def submit(self):
		# get object name
		name = self.ent_name.get()

		# get object color
		fill = self.ent_color.get() 
		
		if (not name):
			print("No name specified")
			return
		
		# ger Check Button value
		is_closed = self.chkValue.get()
		
		# get coordinates list
		coord = Helper.get_coords_from_entry(self.ent_coord.get())

		if (not coord):
			print("No coordinates specified")
			return

		obj = self.mainwindow.canvas.create_object(
			name,
			coord,
			is_closed,
			fill
		)

		# update object names list box
		self.mainwindow.lst_objNames.insert("end", obj.name)

class TransformWindow(wi.TransformWindowInterface):
	def submit(self):
		index = self.mainwindow.get_selected_object()

		if (index == -1):
			print("No object selected to transform")
			return
		
		obj = self.mainwindow.canvas.graphicObjects[index]

		translate = self.translate.get()
		rotate = self.rotate.get()
		scale = self.scale.get()
	
		matrix = Transformer.identity()

		if scale:
			scale_factor = Helper.get_coords_from_entry(self.scal_ent.get())
			if (len(scale_factor) != 1):
				print("invalid scale factor specified")
				return
			scale_factor = scale_factor[0]
			center = obj.get_center()
			matrix = Transformer.scale(matrix, scale_factor, center)

		if rotate:
			try:
				angle = float(self.rot_ent_angle.get())
			except ValueError:
				print("invalid angle specified")
				return
			rtype = self.rotation_type.get()
			if (rtype == self.rot_combbx_options[0]):
				point = obj.get_center()
			elif (rtype == self.rot_combbx_options[1]):
				point = (0, 0) # world center
			else:
				point = Helper.get_coords_from_entry(self.rot_ent_point.get())
				if (len(point) != 1):
					print("invalid rotation point specified")
					return
				point = point[0]
			matrix = Transformer.rotation(matrix, angle, point)

		if translate:
			vector = Helper.get_coords_from_entry(self.trans_ent.get())
			if (len(vector) != 1):
				print("invalid translation vector specified")
				return
			vector = vector[0]
			matrix = Transformer.translation(matrix, vector)

		self.mainwindow.canvas.transform_object(index, matrix)
