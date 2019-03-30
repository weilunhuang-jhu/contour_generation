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

tm = trimesh.load_mesh('./obj/monkey.obj');
mesh = pyrender.Mesh.from_trimesh(tm);

#m = pyrender.Mesh.from_points(pts, colors=colors)
sm = trimesh.creation.uv_sphere(radius=0.1)
sm.visual.vertex_colors = [1.0, 0.0, 0.0]

#mesh_pose=np.array([
#    [1, 0,   0,   0],
#    [0,  1, 0.0, 0.0],
#    [0.0,  0,   1.0,  0],
#    [0.0,  0.0, 0.0, 1.0] ])
scene = pyrender.Scene();
camera = pyrender.PerspectiveCamera(yfov=1.0);
camera_pose=np.array([
    [1, 0,   0,   0],
    [0,  1, 0.0, 0.0],
    [0.0,  0,   1.0,   5],
    [0.0,  0.0, 0.0, 1.0] ])
scene.add(mesh,name="mymesh");
scene.add(camera,pose=camera_pose);

default_mode="view";
        
class MyViewer(pyrender.Viewer):
    def __init__(self,scene, viewport_size=None, render_flags=None, viewer_flags=None,registered_keys=None, run_in_thread=False, **kwargs):
        self.mesh=tm;
        # mode: view mode and draw mode
        self.mode=default_mode;
        #ray_casting
        self.ray_casting=Ray_cast(self.mesh);
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
            print("==========find cutting vectors by mean vector==========")
        # press F4 to keep intersection info
        if symbol==pyglet.window.key.F4:
            self.keep=True;
            print("==========keep previous ray casting==========")
        # press F5 to find intersections on new model
        if symbol==pyglet.window.key.F5:
            self.ray_casting.intersect_on_new_model();
            print("==========find intersection on new model==========")

#            # press F6 to resume to initial view
#            if symbol==pyglet.window.key.F6:
#                # sets the projection
#                gl.glMatrixMode(gl.GL_PROJECTION)
#                gl.glLoadIdentity()
#                glu.gluPerspective(self.camera.init_camera_param.fov, width / float(height), 0.1, 10000)
#                # set the model view
#                self.camera.init_view();
#                print("==========initial view==========")
            
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
            if isIntersect:
                points=self.ray_casting.draw();
#                colors=np.random.uniform(size=points.shape);
#                temp=pyrender.Mesh.from_points(points,colors=colors);
                
                tfs = np.tile(np.eye(4), (len(points), 1, 1))
                tfs[:,:3,3] = points
                m = pyrender.Mesh.from_trimesh(sm, poses=tfs)

                
                self.render_lock.acquire();
                self.scene.add(m);
                self.render_lock.release();
                print(points)
                
                
#            print("location")
#            print(iInfo.icoordinate.shape)
#            print("triangleID")
#            print(iInfo.triangleID.shape)
            
        super().on_mouse_press(x, y, buttons, modifiers)
        
v = MyViewer(scene, use_raymond_lighting=True);   

  
#class Window(pyglet.window.Window):
#    def __init__(self, width, height, caption, resizable=False):
#        pyglet.window.Window.__init__(self, width=width, height=height, caption=caption, resizable=resizable)
#
#        # sets the background color
#        gl.glClearColor(*black)
#
#        # pre-loaded models
##        self.model_names = ['box.obj', 'uv_sphere.obj', 'monkey.obj']
##        self.model_names = ['box.obj', 'uv_sphere.obj', 'monkey.obj','Model.obj']
#        self.model_names = ['skull_defect.obj','implant.obj']
#
##        self.model_names = ['Model.obj']
#        
#        self.models = []
#        for name in self.model_names:
#            self.models.append(OBJModel(x=0.0,y=0.0,z=0.0,color=dark_gray, path=os.path.join('obj', name)))
#        # current model
#        self.model_index = 0
#        self.current_model = self.models[self.model_index]
#        # mode: view mode and draw mode
#        default_mode="view";
#        self.mode=default_mode;
#        #ray_casting
#        self.ray_casting=Ray_cast(self.current_model);
#        self.camera=Camera();
#        #keep ray_casting as previous one
#        self.keep=False;
#
#        @self.event
#        def on_resize(width, height):
#            # sets the viewport
#            gl.glViewport(0, 0, width, height)
#            # sets the projection
#            gl.glMatrixMode(gl.GL_PROJECTION)
#            gl.glLoadIdentity()
#            glu.gluPerspective(self.camera.init_camera_param.fov, width / float(height), 0.1, 10000)
#            print(self.camera.init_camera_param.fov)
#            # set the model view
#            self.camera.init_view();
#            return pyglet.event.EVENT_HANDLED
#
#        @self.event
#        def on_draw():
#            # clears the screen with the background color
#            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
#            #gl.glLoadIdentity()
#
#            # draws the current model
#            self.current_model.draw()
#            
#            #draws ray casting points
#            self.ray_casting.draw();
#
#        @self.event
#        def on_key_press(symbol, modifiers):
#            # press the LEFT or RIGHT key to change the current model
#            if symbol == pyglet.window.key.RIGHT:
#                # next model
#                self.model_index = (self.model_index + 1) % len(self.model_names)
#                # disable texture rendering for current model
#                if self.current_model.texture is not None:
#                    gl.glBindTexture(self.current_model.texture.target, 0);
#                    gl.glDisable(self.current_model.texture.target);
#                self.current_model = self.models[self.model_index];
##                # enable texture rendering for current model
#                if self.current_model.texture is not None:
#                    gl.glEnable(self.current_model.texture.target);
#                    gl.glBindTexture(self.current_model.texture.target, self.current_model.texture.id);
#                if self.keep==False:
#                    prev_iInfos=self.ray_casting.iInfos;
#                    self.ray_casting=Ray_cast(self.current_model);
#                    self.ray_casting.prev_iInfos=prev_iInfos;
#                    
#                    
#            elif symbol == pyglet.window.key.LEFT:
#                # previous model
#                self.model_index = (self.model_index - 1) % len(self.model_names)
#                self.current_model = self.models[self.model_index]
#                if self.keep==False:
#                    prev_iInfos=self.ray_casting.iInfos;
#                    self.ray_casting=Ray_cast(self.current_model);
#                    self.ray_casting.prev_iInfos=prev_iInfos;
#                    
#            # press F1 or F2 key to switch mode
#            if symbol ==pyglet.window.key.F1:
#                self.mode="view";
#                print("==========view mode==========")
#            if symbol==pyglet.window.key.F2:
#                self.mode="draw";
#                print("==========draw mode==========")
#            # press F3 key to find cutting vector by mean vector
#            if symbol==pyglet.window.key.F3:
#                self.ray_casting.end=True;
#                self.ray_casting.find_CuttingVectorByMean();
#                print("==========find cutting vectors by mean vector==========")
#            # press F4 to keep intersection info
#            if symbol==pyglet.window.key.F4:
#                self.keep=True;
#                print("==========keep previous ray casting==========")
#            # press F5 to find intersections on new model
#            if symbol==pyglet.window.key.F5:
#                self.ray_casting.intersect_on_new_model();
#                print("==========find intersection on new model==========")
#
#            # press F6 to resume to initial view
#            if symbol==pyglet.window.key.F6:
#                # sets the projection
#                gl.glMatrixMode(gl.GL_PROJECTION)
#                gl.glLoadIdentity()
#                glu.gluPerspective(self.camera.init_camera_param.fov, width / float(height), 0.1, 10000)
#                # set the model view
#                self.camera.init_view();
#                print("==========initial view==========")
#                
#            # press F10 to print info
#            if symbol==pyglet.window.key.F10:
#                print(self.ray_casting.prev_iInfos)
#                
#        
#        @self.event
#        def on_mouse_scroll(x, y, scroll_x, scroll_y):
#            self.camera.zoom(scroll_y);
#            # set the projection
#            gl.glMatrixMode(gl.GL_PROJECTION);
#            gl.glLoadIdentity();
#            glu.gluPerspective(self.camera.camera_param.fov, width / float(height), 0.1, 10000);
#            #set model view
#            self.camera.view();
#
#        @self.event
#        def on_mouse_drag(x, y, dx, dy, button, modifiers):
#            if self.mode=="view":
#                self.camera.translate(dx,dy,button);
#                self.camera.rotate(dx,dy,button);
#        
#        @self.event
#        def on_mouse_press(x, y, button, modifiers):
#            if self.mode=="draw":
#                w,h=self.get_size();
##                M_proj=(gl.GLfloat*16)();
##                M_modelview=(gl.GLfloat*16)();
##                gl.glGetFloatv(gl.GL_PROJECTION_MATRIX,M_proj);
##                gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
##                M_proj=euclid.Matrix4.new(*(list(M_proj)));
##                M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
##                print(M_proj);
##                print(M_modelview);
##                print(M_modelview.inverse());
##                for triangle in self.current_model.triangles: 
##                    print(triangle.vertices);
#                
##                print(w)
##                print(h)
##                print(x)
##                print(y)
#                
#                ray=self.ray_casting.build_ray(x,y,button,w,h);
#                print(ray)
#                iInfo=IntersectionInfo();
#                (isIntersect,iInfo)=self.ray_casting.intersect(ray);
#                if isIntersect:
#                    print("====================")
#                    print("iInfo in outest loop")
#                    print(iInfo.icoordinate);
#                    print("triangleID is")
#                    print(iInfo.triangleID)
#                    
## creates the window and sets its properties
#window = Window(width=400, height=400, caption='Viewer', resizable=True)
#
## starts the application
#pyglet.app.run()
