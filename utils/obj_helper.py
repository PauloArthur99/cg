class Obj_helper:
	def __init__(self, canvas):
		self.canvas = canvas

	# exports scene as .obj file
	def export_obj(self, filename, graphicObjects):
		vertices = []
		for graph_obj in graphicObjects:
			for coord in graph_obj.coordinates:
				vertices.append(coord)
		vertices = list(set(vertices))
		# Writing to the corresponding file .obj.
		file = open(filename, 'w')
		for ver in vertices:
			file.write("v " + str(ver[0]) + " " + str(ver[1]) + " 0.0\n")

		# Writing the objects.
		for graph_obj in graphicObjects:
			vertices_index = []
			for coord in graph_obj.coordinates:
				idx = vertices.index(coord) + 1
				vertices_index.append(idx)

			file.write("o " + graph_obj.get_real_name() + "\n")
			if len(vertices_index) > 1:
				file.write("l ")
			else:
				file.write("p ")

			for elem in vertices_index:
				file.write(str(elem) + " ")
			if graph_obj.is_closed == True:
				file.write(str(vertices_index[0]))

			file.write("\n")
		file.close()
	
	# Load .obj file
	def import_obj(self, filename):
		with open(filename) as f:
			lines = f.readlines()

		object_name = None
		vertices = []
		for line in lines:
			line = line.split()
			if line[0] == 'v':
				x = float(line[1])
				y = float(line[2])
				vertices.append((x, y))
			if line[0] == 'o':
				object_name = line[1]
			if line[0] == 'l' or line[0] == 'p':
				object_coords = []
				is_closed = False
				for i in range(1, len(line)):
					index = int(line[i])
					if (index > 0):
						index -= 1
					aux = vertices[index]
					object_coords.append(aux)

				# Verifying whether the object is closed or not.
				if len(object_coords) > 1:
					if object_coords[0] == object_coords[-1]:
						object_coords.pop()
						is_closed = True
				self.canvas.create_object(object_name, object_coords, is_closed)
