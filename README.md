# contour_generation
## Project Description

* A simple interactive application to allow user to choose arbitrary points on a mesh model with mouse
* Aims to generate contour of defected area of skull mesh

## Dependencies
* python3
* pyglet

  <https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/>
* pyeuclid

  <https://github.com/ezag/pyeuclid>

## Usage

* run
```python view.py```
with your **.obj** files in **/obj** folder and **/obj** should be at the same folder as all the **.py** files
* In the application window, use F1 (view) and F2 (draw) to switch **view** mode and **draw** mode

* In view mode:

  1. mouse scroll for zoom in and out
 
  2. mouse left for camera translation
 
  3. mouse right for camera rotation

* In draw mode:
 
  mouse press to choose arbitrary points on mesh model (if intersection exists between mesh model surface and ray emitted from your mouse position ), currently with functions to **find connecting points** and **find cutting vectors**


  

## File Description
* obj_model.py:
 
  load OBJ file and generate model object with vertices, normals, surfaces, texture coordinates information 

* camera.py:
 
  camera setting for application window

* triangle.py:

  triangle class, used for ray-plane intersection

* intersection_info.py

  IntersectionInfo class, used to store information of intersection
* ray.py: 
  
  do ray casting to find intersection bewteen mesh surface and ray emitted from mouse position

* viewer.py:
 
  application window
