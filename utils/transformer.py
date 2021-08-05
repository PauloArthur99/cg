import math
import numpy as np


class Transformer:
	# Identity
	@staticmethod
	def identity():
		return [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]]

	# returns a rotation matrix to the given angle an reference point
	@staticmethod
	def rotation(matrix, angle, ref_point):
		cos = math.cos(math.radians(angle))
		sin = math.sin(math.radians(angle))
		rotation_array = np.array([[cos, sin, 0], [-sin, cos, 0], [0, 0, 1]])
		if ref_point == (0, 0):
			result = np.dot(np.array(matrix), rotation_array)
			return result.tolist()
		else:
			neg_ref_point = (-ref_point[0], -ref_point[1])
			mat_after_trans = Transformer.translation(matrix, neg_ref_point)
			inter_result = np.dot(np.array(mat_after_trans), rotation_array)
			result = Transformer.translation(inter_result.tolist(), ref_point)
			return result
	
	# returns a rotation matrix to the given reference point
	@staticmethod
	def translation(matrix, ref_point):
		dx = ref_point[0]
		dy = ref_point[1]
		translation_array = np.array([[1.0, 0, 0], [0, 1.0, 0], [dx, dy, 1.0]])
		result = np.dot(np.array(matrix), translation_array)
		return result.tolist()

	# returns a scaling matrix to the given scale coefficient and center point
	@staticmethod
	def scale(matrix, scale_coef, center_point):
		sx = scale_coef[0]
		sy = scale_coef[1]
		scale_array = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
		neg_cent_point = (-center_point[0], -center_point[1])
		mat_after_trans = Transformer.translation(matrix, neg_cent_point)
		inter_result = np.dot(np.array(mat_after_trans), scale_array)
		result = Transformer.translation(inter_result.tolist(), center_point)
		return result
