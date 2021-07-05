# Instructions

## Interface manual

The main window interface is divided in two sections:
- the viewport, where the objects are displayed
- the commands frame, that is divided in:
  - The objects list box, in which are displayed all objects names in the scene
  - The "New Object" Button, where new objects can be added through the creation of the "New Object" window
  - The "Remove" button, that removes the selected object from the scene
  - The "Transform" button, that transforms the selected object through the creation of the "Transform Object" window 
  - The "in" and "out" buttons: responsable for zoom in and zoom out functionalities
  - The arrows: responsable for window navigation to right, left, up and down

The "New Object" window is responsable for the creation of a new object.
 - It must be specified a name and all the points coordinates that compose the object.
 - The coordinates must follow the **MCF
 - If the first coordinate is connected to the last coordinate, the "is a closed object" checkbox must be marked
 - "Ok" button confirms the object creation

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


**MCF = multiple coordinates format = (x1, y1), (x2, y2), ...
**SCF = single coordinate format = (x, y)
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
#### Install python modules
```
pip install -r requirements.txt
```
#### Run code
```
python main.py
```