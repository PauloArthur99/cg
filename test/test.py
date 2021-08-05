import sys
import os

# THIS MUST COME FIRST! Python does not recognize parent folder automatically
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.transformer import Transformer
from windows.functions import MainWindow


def heart(root):
	obj = root.canvas.create_curve(
		"heart",
		[
			(0, -100), (-300, 100), (-50, 200), (0, 100), 
			(50, 200), (300, 100), (0, -100),
			(-150, 50), (-25, 100), (0, 50),
			(25, 100), (150, 50), (0, -50),
		]
	)
	return obj

def square(root):
	obj = root.canvas.create_object(
		"square",
		[
			(50, 50), (50, 150), (150, 150), (150, 50)
		],
		is_closed=True
	)
	return obj

def batman(root):
	obj = root.canvas.create_object(
		"batman",
		[
			(5,3),(5,-1),(6,-2),(8, 0),(10,4),(12,8),(15,12),(13,16),
			(15,15),(19,15),(22,15),(24,15),(26,16),(25,14),(23,10),
			(22,6),(19,5),(17,3),(16,1),(15,-3),(15,-7),(13,-8), 
			(11,-10),(9,-12),(8,-14),(7,-18),(5,-16),(1,-14),(0,-14), 
			(-4,-15),(-6,-17),(-8,-15),(-10,-13),(-11,-12),(-12,-12), 
			(-13,-12),(-14,-13),(-17,-15),(-18,-15),(-22,-13),(-24,-12),
			(-25,-12),(-27,-13),(-25,-11),(-23,-8),(-21,-5),(-19,0), 
			(-15,-2),(-12,-4),(-10,-5),(-7,-6),(-4,-6),(-1,-6),(-1,-3),(-2,1), 
			(0,-1),(1,0),(2,0),(3, 1),(3, 3)
		],
		is_closed=True,
		is_filled=True
	)
	obj.transform(
		Transformer.scale(Transformer.identity(),
		(7, 7),
		obj.get_center())
	)
	root.canvas.draw()
	return obj

def test():
	tests = {
		1 : batman,
		2 : square,
		3 : heart,
	}

	if (len(sys.argv) < 2):
		print("incorrect use. Usage: test.py <number>\n")
		print("<number>:")
		for key, value in tests.items():
			print("%d-%s" % (key, value.__name__))
		exit()
	try:
		a = int(sys.argv[1])
	except ValueError:
		print("argument must be an integer")
		exit()

	root = MainWindow()
	tests[a](root)
	root.mainloop()


if __name__ == "__main__":
	test()