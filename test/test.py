import sys
import os

# For some reason python does not recognize parent folder automatically
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from windows.functions import MainWindow

def test():
	root = MainWindow()
	obj = root.canvas.create_object(
		"Quadrado",
		[(100, 100), (-100, 100), (-100, -100), (100, -100)],
		is_closed=True
	)
	root.lst_objNames.insert("end", obj.name)
	root.mainloop()

if __name__ == "__main__":
	test()