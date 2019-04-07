"""
Created on Tue Jan 08 2019

reference:
    http://www.poketcode.com/en/pyglet_demos/index.html#obj_viewer

@author: weilunhuang
"""
import os
import pyglet
import trimesh
import pyrender
import numpy as np
from pyglet.gl import gl
from pyglet.gl import glu

from camera import Camera
from ray import IntersectionInfo
from ray import Ray_cast

skull_defect = trimesh.load_mesh('./obj/skull_defect_old.obj');
implant=trimesh.load_mesh('./obj/implant_old.obj');

mesh_skull_defect = pyrender.Mesh.from_trimesh(skull_defect);
mesh_implant=pyrender.Mesh.from_trimesh(skull_defect);

scene = pyrender.Scene();
camera = pyrender.PerspectiveCamera(yfov=1.0);
camera_pose=np.array([
    [1, 0,   0,   0],
    [0,  1, 0.0, 0.0],
    [0.0,  0,   1.0,   5],
    [0.0,  0.0, 0.0, 1.0] ])
scene.add(mesh_skull_defect, name="skull_defect_mesh");
#scene.add(mesh_implant, name="implant_mesh");
scene.add(camera,pose=camera_pose,name="mycamera");

default_mode="view";
        
class MyViewer(pyrender.Viewer):
    def __init__(self,scene, viewport_size=None, render_flags=None, viewer_flags=None,registered_keys=None, run_in_thread=False, **kwargs):
        self.mesh=skull_defect;
        # mode: view mode and draw mode
        self.mode=default_mode;
        #ray_casting
        self.ray_casting=Ray_cast(self.mesh);
        #my nodes for visualization
        self.nodes={"point_mesh_node":None,"cutting_vector_mesh_node":None};
#        self.point_mesh_node=None;
#        self.cutting_vector_mesh_node=None;
        #keep ray_casting as previous one
        self.keep=False;
        super().__init__(scene, viewport_size,render_flags, viewer_flags,registered_keys, run_in_thread, **kwargs);
        

    def on_key_press(self,symbol, modifiers):
        # press F1 or F2 key to switch mode
        if symbol ==pyglet.window.key.F1:
            self.mode="view";
            print("==========view mode==========")
        if symbol==pyglet.window.key.F2:
            self.mode="draw";
            print("==========draw mode==========")
        # press F3 key to find cutting vector by mean vector
        if symbol==pyglet.window.key.F3:
            self.ray_casting.end=True;
            self.ray_casting.find_CuttingVectorByMean();
            #get mesh from ray_casting
            meshes=self.ray_casting.draw();
            #update scene
            self.update_scene(meshes);
            #reassign self.pointmesh_node
            self.find_node();
            
            print("==========find cutting vectors by mean vector==========")
                
        # press F4 to keep intersection info
        if symbol==pyglet.window.key.F4:
            self.keep=True;
            print("==========keep previous ray casting==========")
        # press F5 to find intersections on new model
        if symbol==pyglet.window.key.F5:
            self.ray_casting.intersect_on_new_model();
            print("==========find intersection on new model==========")
        # press F6 to make mesh invisible
        if symbol==pyglet.window.key.F6:
            
            print("==========F6 pressed==========")
        
        # press F10 to print info
        if symbol==pyglet.window.key.F10:
            print(self.ray_casting.prev_iInfos)
        super().on_key_press(symbol, modifiers)
        
    def on_mouse_press(self, x, y, buttons, modifiers):
        
        if self.mode=="draw":
            w,h=self.get_size();

            #get projection matrix and inversed modelview matrix
            M_proj=self.scene.main_camera_node.camera.get_projection_matrix(w,h);
            M_modelview_inversed=self.scene.get_pose(self.scene.main_camera_node);
            
#            print("M_proj")
#            print(M_proj)
#            print("M_modelview_inversed")
#            print(M_modelview_inversed)
            
            #reshape and pass two matrices to ray_casting
            M_proj=M_proj.T.reshape(16);
            M_modelview_inversed =M_modelview_inversed.T.reshape(16);
            ray=self.ray_casting.build_ray(x,y,buttons,w,h,M_proj, M_modelview_inversed);
            
            
            isIntersect=self.ray_casting.intersect(ray);
            print(isIntersect)
            #update if isIntersect
            if isIntersect:
                #get mesh from ray_casting
                meshes=self.ray_casting.draw();
                #update scene
                self.update_scene(meshes);
            #reassign self.pointmesh_node
            self.find_node();
            
        super().on_mouse_press(x, y, buttons, modifiers)
    def find_node(self):
        """
            find and assign node given list of node_names
        """
        node_names=list(self.nodes.keys());
        nodes_list=list(self.scene.nodes);
        for i in range(len(nodes_list)):
            for j in range(len(node_names)):
                if nodes_list[i].name==node_names[j]:
                    self.nodes[node_names[j]]=nodes_list[i];
                    
    def update_scene(self,meshes):
        """
            update scene by removing/adding mesh
        """
        #lock render first
        self.render_lock.acquire();
        #iterate and add meshes to scene
        for i in range(len(meshes)):
            temp_mesh=meshes[i];
            if self.nodes[temp_mesh.name+'_node'] is not None:
                self.scene.remove_node(self.nodes[temp_mesh.name+'_node']);
            self.scene.add(temp_mesh,name=temp_mesh.name);
        #release lock
        self.render_lock.release();
    
v = MyViewer(scene, use_raymond_lighting=True);   
