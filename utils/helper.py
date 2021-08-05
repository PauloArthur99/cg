import re, os


class Helper:
	# transforms user input into a list os tuples (coordinates)
	@staticmethod
	def get_coords_from_entry(string):
		return (
			list(
				map(
					lambda x: tuple(map(float, x.split(","))), 
					re.findall(
						r'\(([ ]*-?\d+\.?\d*[ ]*[,][ ]*-?\d+\.?\d*[ ]*)\)',
						string
					)
				)
			)
		)

	# Is user color code valid? If so, return the code
	@staticmethod
	def validate_hex_color_entry(hex):
		r = re.search("^#([A-Fa-f0-9]{9}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", hex)
		if (r):
			return r.group()
		else:
			return None

	# returns an image file path
	@staticmethod
	def get_image_file(file):
		return os.path.abspath(os.path.join("windows/images", file))

	# returns the distance between two points
	@staticmethod
	def distance_between_points(p1, p2):
		return (((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)**0.5)

	# Are the polygon coordinates specified in clockwise orientation?
	@staticmethod
	def polygon_is_in_clockwise(points):
		sum = 0
		la = len(points)
		for i in range(la):
			sum += (points[(i + 1)%la][0]-points[i%la][0])* \
				(points[(i + 1)%la][1]+points[i%la][1])
		return True if sum > 0 else False
