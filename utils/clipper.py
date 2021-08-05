INSIDE = 0
BOTTOM = 1
LEFT = 2
TOP = 4
RIGHT = 8
class Clipper:
	@staticmethod
	def inside_clip_edge(region, edge):
		# is the region inside the current clipping edge?
		if region & edge:
			return False
		return True

	@staticmethod
	def intersection(x1, y1, x2, y2, edge, coef):
		x_min, x_max, y_min, y_max = -coef, coef, -coef, coef
		if edge & TOP:
			x = x1 + ((x2 - x1)/(y2 - y1))*(y_max - y1)
			y = y_max

		elif edge & BOTTOM:
			x = x1 + ((x2 - x1)/(y2 - y1))*(y_min - y1)
			y = y_min

		elif edge & RIGHT:
			y = y1 + ((y2 - y1)/(x2 - x1))*(x_max - x1)
			x = x_max

		elif edge & LEFT:
			y = y1 + ((y2 - y1)/(x2 - x1))*(x_min - x1)
			x = x_min
		return (x, y)

	@staticmethod
	def cohen_sutherland_polygon(coordinates, coef):
		output = coordinates.copy()
		edges = [BOTTOM, LEFT, TOP, RIGHT]
		for i in range(4):
			edge = edges[i]
			current = output.copy()
			l = len(current)
			output = []
			for j in range(l):
				x1, y1 = current[j%l]
				x2, y2 = current[(j + 1)%l]

				code1 = Clipper.region_code(x1, y1, coef)
				code2 = Clipper.region_code(x2, y2, coef)
				state1 = Clipper.inside_clip_edge(code1, edge)
				state2 = Clipper.inside_clip_edge(code2, edge)
	
				if state1 and state2:
					output.append((x2, y2))
				elif state1 and not state2:
					x, y = Clipper.intersection(x1, y1, x2, y2, edge, coef)
					output.append((x, y))
				elif not state1 and state2:
					x, y = Clipper.intersection(x1, y1, x2, y2, edge, coef)
					output.append((x, y))
					output.append((x2, y2))
		return output

	@staticmethod
	def region_code(x, y, coef):
		x_min, x_max, y_min, y_max = -coef, coef, -coef, coef
		code = INSIDE
		if x < x_min:
			code |= LEFT
		if x > x_max:
			code |= RIGHT
		if y < y_min:
			code |= BOTTOM
		if y > y_max:
			code |= TOP
	
		return code
	
	@staticmethod
	def cohen_sutherland(line, coef):
		# get line cooerdinates
		x1, y1 = line[0]
		x2, y2 = line[1]

		# get coordinates' region code
		code1 = Clipper.region_code(x1, y1, coef)
		code2 = Clipper.region_code(x2, y2, coef)
		valid = False
	
		# clip line coordinates to the window border until it gets accepted
		# (entire in window) or reject (entire outside window)
		while True:
			# entire line inside window
			if code1 == 0 and code2 == 0:
				valid = True
				break

			# entire line outside window
			elif (code1 & code2) != 0:
				break
	
			else:
				# which code is outside?
				code_out = code1 if code1 != INSIDE else code2

				# get intersection coordinates
				x, y = Clipper.intersection(x1, y1, x2, y2, code_out, coef)

				# overwrite point coordinates
				if code_out == code1:
					x1, y1 = x, y
					code1 = Clipper.region_code(x1, y1, coef)
	
				else:
					x2, y2 = x, y
					code2 = Clipper.region_code(x2, y2, coef)
	
		if valid:
			return [(x1, y1), (x2, y2)]
		return []

	@staticmethod
	def liang_barsky(line, coef):
		d1 = line[0]
		d2 = line[1]

		xmax, xmin, ymax, ymin = coef, -coef, coef, -coef

		dx = d2[0] - d1[0]
		dy = d2[1] - d1[1]
		p = [-dx, dx, -dy, dy]
		q = [d1[0] - xmin, xmax - d1[0], d1[1] - ymin, ymax - d1[1]]

		pos = [1]
		neg = [0]
		for i in range(4):
			if p[i] < 0:
				neg.append(q[i]/p[i])
			elif p[i] > 0:
				pos.append(q[i]/p[i])
			# line is parallel to window border and is entire outside window
			elif (q[i] < 0):
					return []
		
		u1 = max(neg)
		u2 = min(pos)

		# outside window
		if (u1 > u2):
			return []

		clipped = [
			(d1[0]+dx*u1, d1[1]+dy*u1),
			(d1[0]+dx*u2, d1[1]+dy*u2)
		]

		return clipped
