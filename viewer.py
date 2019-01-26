"""
Created on Tue Jan 08 2019

@author: weilunhuang
"""
import os
import pyglet

from obj_model import OBJModel
from camera import Camera
from ray import IntersectionInfo
from ray import Ray_cast
from pyglet.gl import gl
from pyglet.gl import glu

# colors
black = (0, 0, 0, 1)
dark_gray = (0.75, 0.75, 0.75, 1)
    
            
class Window(pyglet.window.Window):
    def __init__(self, width, height, caption, resizable=False):
        pyglet.window.Window.__init__(self, width=width, height=height, caption=caption, resizable=resizable)

        # sets the background color
        gl.glClearColor(*black)

        # pre-loaded models
        self.model_names = ['box.obj', 'uv_sphere.obj', 'monkey.obj','part.obj']
        self.models = []
        for name in self.model_names:
            self.models.append(OBJModel(x=0.0,y=0.0,z=0.0,color=dark_gray, path=os.path.join('obj', name)))
        # current model
        self.model_index = 0
        self.current_model = self.models[self.model_index]
        # mode: view mode and draw mode
        default_mode="view";
        self.mode=default_mode;
        #ray_casting
        self.ray_casting=Ray_cast(self.current_model);
        self.camera=Camera();
        

        @self.event
        def on_resize(width, height):
            # sets the viewport
            gl.glViewport(0, 0, width, height)
            # sets the projection
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            glu.gluPerspective(60, width / float(height), 0.1, 1000)
            self.camera.view();
            return pyglet.event.EVENT_HANDLED

        @self.event
        def on_draw():
            # clears the screen with the background color
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            #gl.glLoadIdentity()

            # sets wire-frame mode
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            # draws the current model
            self.current_model.draw()
            
            #draws ray casting points
            self.ray_casting.draw();

        @self.event
        def on_key_press(symbol, modifiers):
            # press the LEFT or RIGHT key to change the current model
            if symbol == pyglet.window.key.RIGHT:
                # next model
                self.model_index = (self.model_index + 1) % len(self.model_names)
                self.current_model = self.models[self.model_index]

            elif symbol == pyglet.window.key.LEFT:
                # previous model
                self.model_index = (self.model_index - 1) % len(self.model_names)
                self.current_model = self.models[self.model_index]
            # press F1 or F2 key to switch mode
            if symbol ==pyglet.window.key.F1:
                self.mode="view";
            if symbol==pyglet.window.key.F2:
                self.mode="draw";
            # press F5 to resume to initial view
            if symbol==pyglet.window.key.F5:
                self.camera.view();
                
        
        @self.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            self.camera.zoom(scroll_y);

        @self.event
        def on_mouse_drag(x, y, dx, dy, button, modifiers):
            if self.mode=="view":
                self.camera.translate(dx,dy,button);
                self.camera.rotate(dx,dy,button);
        
        @self.event
        def on_mouse_press(x, y, button, modifiers):
            if self.mode=="draw":
                w,h=self.get_size();
#                M_proj=(gl.GLfloat*16)();
#                M_modelview=(gl.GLfloat*16)();
#                gl.glGetFloatv(gl.GL_PROJECTION_MATRIX,M_proj);
#                gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
#                M_proj=euclid.Matrix4.new(*(list(M_proj)));
#                M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
#                print(M_proj);
#                print(M_modelview);
#                print(M_modelview.inverse());
#                for triangle in self.current_model.triangles: 
#                    print(triangle.vertices);
                
#                print(w)
#                print(h)
#                print(x)
#                print(y)
                
                ray=self.ray_casting.build_ray(x,y,button,w,h);
                print(ray)
                iInfo=IntersectionInfo();
                (isIntersect,iInfo)=self.ray_casting.intersect(ray);
                if isIntersect:
                    print("iInfo in outest loop")
                    print(iInfo.icoordinate);
                    
# creates the window and sets its properties
window = Window(width=400, height=400, caption='Viewer', resizable=True)

# starts the application
pyglet.app.run()
