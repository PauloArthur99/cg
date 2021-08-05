# Instructions

## Interface manual

The main window interface is divided in three sections:
- the file menu, where you can import .obj files to the scene and export the scene as .obj file
- the viewport, where the objects are displayed
- the commands frame, that is divided in:
  - The objects list box, in which are displayed all objects names in the scene
  - The "New Object" Button, where new objects can be added through the creation of the "New Object" window
  - The "New Curve" Button, where new bezier curves can be created though the creation of the "New Curve" window
  - The "Remove" button, that removes the selected object from the scene
  - The "Transform" button, that transforms the selected object through the creation of the "Transform Object" window 
  - The zoom buttons: responsable for zoom in and zoom out functionalities
  - The rotation buttons: responsable for window rotation to right and left
  - The arrows: responsable for window navigation to right, left, up and down

The "New Object" window is responsable for the creation of a new object.
 - It must be specified a name and all the points coordinates that compose the object.
 - The coordinates must follow the **MCF
 - If the first coordinate is connected to the last coordinate, the "is a closed object" checkbox must be marked
 - "Ok" button confirms the object creation
 - Optionally, a rgb color code can be specified to create the object. The default is black. The code must follow one of the **RGBF. Note that tkinter does not support all color codes

The "New Curve" window is responsable for the creation of a new bezier curve.
 - It must be specified a name for the curve
 - It must be specified 4 + 3x coordinates (x >= 0). The first 4 coordinates create the first curve, where the first point is where the curve begins, the second point is the first control point, the third point is the second control point and the fourth is where the curve ends. To connect another curve, 3 more points can be specified: first control point, second control point and final point. (note that the curve initiates where the last has stopped). Coordinates must follow **MCF
 - Optionally, a rgb color code can be specified. The code must follow the **RGBF

The "Transform Object" window is responsable for the object transformation functions (translation, rotation and scaling)
 - It must be checked which transformations are going to be aplied.
 - In translation:
    - The object position is changed based on a vector
    - Vector must follow the **SCF
 - In scaling:
    - Object height and width scale are changed based on the scale factor
    - Factor must follow the **SCF
 - In rotation:
    - The object is rotated arround a point, according to the selected rotation type. The point can be its center, the world center or any arbitrary point
    - An angle in degrees must be specified
    - If the rotation type is "arbitrary point", a point must be specified following **SCF
 - It is possible to add multiple transformations to be applied.
 - The Ok button applies all transformations added


**MCF = multiple coordinates format = (x1, y1), (x2, y2), ...  

**SCF = single coordinate format = (x, y)

**RGBF = #rgb OR #rrggbb OR #rrrgggbbb

## Development Environment
 - Operational System: Ubuntu 20.04
 - Python 3.8.5

# Running code
#### Create virtual environment
```
python -m virtualenv env
```
#### Activate environment
```
source env/bin/activate
```
#### Install dependencies
```
pip install -r requirements.txt
```
#### Run code
```
python main.py
```