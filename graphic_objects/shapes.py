from abc import abstractclassmethod
from utils.clipper import Clipper
from utils.transformer import Transformer
from utils.helper_curves import Helper_curves
import numpy as np

class GraphicObjectCreator:
	def __init__(self, canvas):
		self.canvas = canvas

	# create a graphic object based on the coordinates amount
	def create(self, name, coords, is_closed = False, fill = "#000000", is_filled=False):
		l = len(coords)
		if l == 1:
			return Dot(self.canvas, "[Dot]%s" % name, coords, fill = fill)
		elif l == 2:
			return Line(self.canvas, "[Line]%s" % name, coords, fill = fill)
		else:
			return Wireframe(
				self.canvas,
				"[Wireframe]%s" % name,
				coords,
				is_closed,
				fill = fill,
				is_filled = is_filled
			)

class GraphicObject:
	def __init__(
		self, 
		canvas, 
		name, 
		coords, 
		is_closed = False, 
		fill = "#000000", 
		is_filled=False
	):
		self.canvas = canvas
		self.name = name
		self.is_closed = is_closed
		self.coordinates = coords
		self.scn = []
		self.fill = fill
		self.is_filled = is_filled
	
	@abstractclassmethod
	def draw(self, matrix):
		pass

	@abstractclassmethod
	def get_center(self):
		pass
	
	# take real name of the object (what was specified in creation)
	def get_real_name(self):
		return self.name[self.name.index("]") + 1:]

	# transform object coordinates
	def transform(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.coordinates = new_coords
	
	# calculates object coordinates in normalized coordinate system
	def update_scn(self, matrix):
		new_coords = []
		for coord in self.coordinates:
			coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
			new_coords.append((coord_multi[0], coord_multi[1]))
		self.scn = new_coords

class Dot(GraphicObject):
	def draw(self, matrix):
		# normalize coordinates
		self.update_scn(matrix)

		# dot is not inside window. We don't need to draw
		if (max(map(abs, self.scn[0])) > 1):
			return 

		# get viewport coordinates
		c = self.canvas.transform_viewport(self.scn)
		x, y = c[0]

		# draw a line
		self.canvas.create_line(x, y, x + 1, y, fill = self.fill)
	
	def get_center(self):
		center = self.coordinates[0]
		return (center[0], center[1])

class Line(GraphicObject):
	def draw(self, matrix):
		# normalize coordinates
		self.update_scn(matrix)

		# gets clipped line
		clipped = self.canvas.clipping_function(self.scn, 1)

		# line is not inside window. Ignore it
		if (not clipped):
			return

		# get viewport coordinates
		c = self.canvas.transform_viewport(clipped)

		x1, y1 = c[0]
		x2, y2 = c[1]

		# draw a line
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
	def draw(self, matrix):
		# normalize coordinates
		self.update_scn(matrix)

		# is a filled object?
		if (self.is_filled):
			self.__draw_filled()
		else:
			self.__draw_wire()
		
	def __draw_wire(self):
		for i in range(len(self.scn) - 1):
			# get clipped line
			clipped = self.canvas.clipping_function(self.scn[i:i+2], 1)

			# line is not inside window. Ignore it
			if (not clipped):
				continue

			# get viewport coordinates
			transformed = self.canvas.transform_viewport(clipped)
			x1, y1 = transformed[0]
			x2, y2 = transformed[1]

			# draw a line
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
		
		# is a closed shape? If so, connect first and last points
		if self.is_closed:
			clipped = self.canvas.clipping_function(
				[self.scn[0], self.scn[-1]],
				1
			)
			if (not clipped):
				return
			transformed = self.canvas.transform_viewport(clipped)
			x1, y1 = transformed[0]
			x2, y2 = transformed[1]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

	def __draw_filled(self):
		# get clipped polygon
		polygon = Clipper.cohen_sutherland_polygon(self.scn, 1)

		# polygon is not inside window
		if (not polygon):
			return

		# get viewport coordinates
		transformed = self.canvas.transform_viewport(polygon)
		temp = []

		# turns [(x1, y1), (x2, y2)...] into [x1, y1, x2, y2, ...]
		for p in transformed:
			temp.extend(p)

		# draw a filled polygon
		self.canvas.create_polygon(temp, fill = self.fill)

	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

# note that this object is static, it's not part of the world. So we don't need
# to make any kind of transformation in it
class Subcanvas(GraphicObject):
	def draw(self):
		c = self.coordinates
		for i in range(len(c) - 1):
			x1, y1 = c[i]
			x2, y2 = c[i + 1]
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
		
		x1, y1 = c[-1]
		x2, y2 = c[0]
		self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)

class Axis(Line):
	# make axis bigger or smaller to support window zoom in and zoom out
	def update_scale(self, coef):
		scale = Transformer.scale(
				Transformer.identity(),
				(coef, coef),
				self.get_center()
		)
		self.transform(scale)
	
	# move axis to support window movement
	def update_range(self, vector):
		translation = Transformer.translation(
			Transformer.identity(),
			vector
		)
		self.transform(translation)

# class used for objects that are not drawn. For example, the window
class LazyGraphicObject(GraphicObject):
	def __init__(self, coords):
		super().__init__(
			canvas = None,
			name = "lazy-object",
			coords = coords
		)

class LazyWireframe(LazyGraphicObject, Wireframe):
	# we only need parent functions
	def __dummy(self):
		pass

class LazyLine(LazyGraphicObject, Line):
	# we only need parent functions
	def __dummy(self):
		pass

class LazyDot(LazyGraphicObject, Dot):
	# we only need parent functions
	def __dummy(self):
		pass

class Curve2d(GraphicObject):
	def __init__(self, name, canvas, coords, fill = "#000000"):
		super().__init__(canvas, name, coords, fill = fill)

		# bezier method matrix
		self.method_matrix = [
			[-1,  3, -3, 1],
			[ 3, -6,  3, 0],
			[-3,  3,  0, 0],
			[ 1,  0,  0, 0]
		]
		curve_points = [self.coordinates[0]]
		
		# iterate throught curves
		for i in range(0, len(self.coordinates) - 1, 3):
			p1 = self.coordinates[i]     # initial point
			p2 = self.coordinates[i + 1] # first control point
			p3 = self.coordinates[i + 2] # second control point
			p4 = self.coordinates[i + 3] # final point

			points_matrix = [
				[p1[0], p1[1], 1],
				[p2[0], p2[1], 1],
				[p3[0], p3[1], 1],
				[p4[0], p4[1], 1],
			]
			matrix = np.dot(self.method_matrix, points_matrix)
			step = 0.02
			t = step
			x1,x2,x3,x4 = matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0]
			y1,y2,y3,y4 = matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1]
			while (t < 1):
				t2, t3 = t**2, t**3
				curve_points.append(
					(
						(x1*t3)	+ (x2*t2) + (x3*t) + (x4),
						(y1*t3)	+ (y2*t2) + (y3*t) + (y4),
					)
				)
				t += step				
			curve_points.append(p4)
		# overwrite coordinates (now it's a set of ponints)
		self.coordinates = curve_points

class Curve_bSpline(GraphicObject):
	def __init__(self, name, canvas, coords, fill = "#000000"):
		super().__init__(canvas, name, coords, fill = fill)

		# bezier method matrix
		self.method_matrix = [
			[-1/6,  3/6, -3/6, 1/6],
			[ 3/6, -6/6,  3/6, 0],
			[-3/6,  0,  3/6, 0],
			[ 1/6,  4/6,  1/6, 0]
		]
		step = 0.02
		step2, step3 = step**2, step**3 
		#curve_points = [self.coordinates[0]]

		init_matrix = [
			[0, 0, 0, 1],
			[step3, step2, step, 0],
			[6*step3, 2*step2, 0, 0],
			[6*step3, 0, 0, 0]
		]
		curve_points = []

		# iterate throught curves
		for i in range(3, len(self.coordinates)):
			p1 = self.coordinates[i - 3]     # first control point
			p2 = self.coordinates[i - 2] # second control point
			p3 = self.coordinates[i - 1] # third control point
			p4 = self.coordinates[i] # final control point

			points_matrix = [
				[p1[0], p1[1], 1],
				[p2[0], p2[1], 1],
				[p3[0], p3[1], 1],
				[p4[0], p4[1], 1],
			]
			matrix_coef = np.dot(self.method_matrix, points_matrix)
			
			matrixD = np.dot(init_matrix, matrix_coef)
			x, delta_x1, delta_x2, delta_x3 = matrixD[0][0], matrixD[1][0], matrixD[2][0], matrixD[3][0]
			y, delta_y1, delta_y2, delta_y3 = matrixD[0][1], matrixD[1][1], matrixD[2][1], matrixD[3][1]
			curve_points.append((x, y))

			curve_points = Helper_curves.fwd_diff(curve_points, step, x, delta_x1, delta_x2, delta_x3,
									y, delta_y1, delta_y2, delta_y3)

		# overwrite coordinates (now it's a set of ponints)
		self.coordinates = curve_points	

	def draw(self, matrix):
		self.update_scn(matrix)
		for i in range(len(self.scn) - 1):
			# get clipped line
			clipped = self.canvas.clipping_function(self.scn[i:i+2], 1)

			# line is not inside window. Ignore it
			if (not clipped):
				continue

			# get viewport coordinates
			transformed = self.canvas.transform_viewport(clipped)
			x1, y1 = transformed[0]
			x2, y2 = transformed[1]

			# draw a line
			self.canvas.create_line(x1, y1, x2, y2, fill = self.fill)
	
	def get_center(self):
		orderedx = self.coordinates.copy()
		orderedy = self.coordinates.copy()
		orderedx.sort(key=lambda x: x[0])
		orderedy.sort(key=lambda x: x[1])
		x = (orderedx[0][0] + orderedx[-1][0])/2
		y = (orderedy[0][1] + orderedy[-1][1])/2
		return (x, y)

