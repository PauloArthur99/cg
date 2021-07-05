from abc import abstractclassmethod
import numpy as np

class GraphicObjectCreator:
	def __init__(self, canvas):
		self.canvas = canvas

	def create(self, name, coords, is_closed = False, fill = "#ff0"):
		l = len(coords)
		if l == 1:
			return Dot(self.canvas, "[Dot]%s" % name, coords)
		elif l == 2:
			return Line(self.canvas, "[Line]%s" % name, coords, fill = fill)
		else:
			return Wireframe(self.canvas, "[Wireframe]%s" % name, coords, is_closed)

class GraphicObject:
	def __init__(self, canvas, name, coords, is_closed = False, fill = "#ff0"):
		self.canvas = canvas
		self.name = name
		self.is_closed = is_closed
		self.coordinates = coords
		self.fill = fill
	
	@abstractclassmethod
	def draw(self):
		pass

	@abstractclassmethod
	def get_center(self):
		pass

	def transform(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.coordinates = new_coords


class Dot(GraphicObject):
	def draw(self):
		c = self.canvas.transform_viewport(self.coordinates)
		x, y = c[0]

		self.canvas.create_line(x, y, x + 1, y, fill = self.fill)
	
	def get_center(self):
		center = self.coordinates[0]
		return (center[0], center[1])

class Line(GraphicObject):
	def draw(self):
		c = self.canvas.transform_viewport(self.coordinates)

		x1, y1 = c[0]
		x2, y2 = c[1]

		self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
	
	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

	

class Wireframe(GraphicObject):
	def draw(self):
		c = self.canvas.transform_viewport(self.coordinates)
		for i in range(len(c) - 1):
			x1, y1 = c[i]
			x2, y2 = c[i + 1]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
		
		# is a closed shape?
		if self.is_closed:
			x1, y1 = c[-1]
			x2, y2 = c[0]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

class AxisX(GraphicObject):
	def draw(self):
		x1 = self.canvas.minx
		x2 = self.canvas.maxx
		y1 = self.coordinates[0][1]
		y2 = self.coordinates[1][1]

		c = self.canvas.transform_viewport([(x1, y1), (x2, y2)])
		
		x1, y1 = c[0]
		x2, y2 = c[1]

		self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

class AxisY(GraphicObject):
	def draw(self):
		x1 = self.coordinates[0][0]
		x2 = self.coordinates[1][0]
		y1 = self.canvas.miny
		y2 = self.canvas.maxy

		c = self.canvas.transform_viewport([(x1, y1), (x2, y2)])
		
		x1, y1 = c[0]
		x2, y2 = c[1]		

		self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)