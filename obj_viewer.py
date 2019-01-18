"""
Created on Tue Jan 08 2019

@author: weilunhuang
"""
import os
import pyglet
import euclid
from camera import Camera
from ray import IntersectionInfo
from ray import Triangle
from ray import Ray_cast
from pyglet.gl import gl
from pyglet.gl import glu

# colors
black = (0, 0, 0, 1)
dark_gray = (0.75, 0.75, 0.75, 1)

class OBJModel:
    """
    Represents an OBJ model.
    """
    def __init__(self, x=0.0,y=0.0,z=0.0, color=dark_gray, path=None):
        self.vertices = [];
        self.vertex_nomals=[];
        self.text_coord=[];
        self.quad_indices = [];
        self.triangle_indices = [];
        self.normal_indices=[];
        self.text_indices=[];
        self.triangles=[];

        # translation and rotation values
        self.x, self.y, self.z = x, y, z;
        self.rx = self.ry = self.rz = 0;

        # color of the model
        self.color = color;

        # if path is provided
        if path:
            self.load(path);

    def clear(self):
        self.vertices = self.vertices[:];
        self.vertex_nomals=self.vertex_nomals[:];
        self.text_coord=self.text_coord[:];
        self.quad_indices = self.quad_indices[:];
        self.triangle_indices = self.triangle_indices[:];
        self.normal_indices=self.normal_indices[:];
        self.text_indices=self.text_indices[:];
        self.triangles=self.triangles[:];
    def load(self, path):
        self.clear();

        with open(path) as obj_file:
            for line in obj_file.readlines():
                # reads the file line by line
                data = line.split();
                #print(data);
                if len(data)==0 or data[0] not in ['v','vn','vt','f']:
                    continue;
                # every line that begins with a 'v' is a vertex
                if data[0] == 'v':
                    x, y, z = data[1:4];
                    self.vertices.extend((float(x), float(y), float(z)));
                # every line that begins with a 'vn' is a vertex normal
                if data[0] == 'vn':
                    x_n, y_n, z_n = data[1:4];
                    self.vertex_nomals.extend((float(x_n), float(y_n), float(z_n)));
                # every line that begins with a 'vt' is a text coordinate
                if data[0] == 'vt':
                    t_u, t_v= data[1:3];
                    self.text_coord.extend((float(t_u), float(t_v)));
                # every line that begins with an 'f' is a face
                # loads the faces
                elif data[0] == 'f':
                    # quads
                    # Note: in obj files the first index is 1, so we must subtract one for each
                    # retrieved value
                    if len(data) == 5:
                        vi_1, vi_2, vi_3, vi_4 = data[1:5]
                        self.quad_indices.extend((int(vi_1) - 1, int(vi_2) - 1, int(vi_3) - 1, int(vi_4) - 1))
                    # triangles
                    # Note: in obj files the first index is 1, so we must subtract one for each
                    # retrieved value                    
                    elif len(data) == 4:
                        #triangles with complete info
                        vi_1, vi_2, vi_3 = data[1:4]
                        if '/' in data[1]:
                            vi_1=vi_1.split('/')
                            vi_2=vi_2.split('/')
                            vi_3=vi_3.split('/')
                            self.triangle_indices.extend((int(vi_1[0]) - 1, int(vi_2[0]) - 1, int(vi_3[0]) - 1))
                            self.text_indices.extend((int(vi_1[1]) - 1, int(vi_2[1]) - 1, int(vi_3[1]) - 1))
                            self.normal_indices.extend((int(vi_1[2]) - 1, int(vi_2[2]) - 1, int(vi_3[2]) - 1))
                            
                        else:
                            self.triangle_indices.extend((int(vi_1) - 1, int(vi_2) - 1, int(vi_3) - 1))
        points_indices=[];
        for i in range(len(self.quad_indices)):
            points_indices.append(self.quad_indices[i]);
            if i%4==3:
                p1=euclid.Point3(self.vertices[points_indices[0]],self.vertices[points_indices[0]+1],self.vertices[points_indices[0]+2]);
                p2=euclid.Point3(self.vertices[points_indices[1]],self.vertices[points_indices[1]+1],self.vertices[points_indices[1]+2]);
                p3=euclid.Point3(self.vertices[points_indices[2]],self.vertices[points_indices[2]+1],self.vertices[points_indices[2]+2]);
                p4=euclid.Point3(self.vertices[points_indices[3]],self.vertices[points_indices[3]+1],self.vertices[points_indices[3]+2]);
                self.triangles.append(Triangle(p1,p2,p3));
                self.triangles.append(Triangle(p3,p4,p1));
                points_indices.clear();
        points_indices.clear();
        for i in range(len(self.triangle_indices)):
            points_indices.append(self.triangle_indices[i]);
            if i%4==2:
                p1=euclid.Point3(self.vertices[points_indices[0]],self.vertices[points_indices[0]+1],self.vertices[points_indices[0]+2]);
                p2=euclid.Point3(self.vertices[points_indices[1]],self.vertices[points_indices[1]+1],self.vertices[points_indices[1]+2]);
                p3=euclid.Point3(self.vertices[points_indices[2]],self.vertices[points_indices[2]+1],self.vertices[points_indices[2]+2]);
                self.triangles.append(Triangle(p1,p2,p3));
                points_indices.clear();
            
    def draw(self):
        
        gl.glPushMatrix();
        # sets the position
        gl.glTranslatef(self.x, self.y, self.z);

        # sets the rotation
        gl.glRotatef(self.rx, 1, 0, 0);
        gl.glRotatef(self.ry, 0, 1, 0);
        gl.glRotatef(self.rz, 0, 0, 1);

        # sets the color
        gl.glColor4f(*self.color);
        
        # draw primitives with batch or vertex_list 
#        batch=pyglet.graphics.Batch();
#        vertex_list=batch.add(len(self.vertices) // 3,gl.GL_QUADS,None,('v3f', self.vertices));
#        batch.draw();
#        vertex_list = pyglet.graphics.vertex_list(len(self.vertices) / 3,('v3f', self.vertices));
#        vertex_list.draw(gl.GL_QUADS)

        # draws the quads
        pyglet.graphics.draw_indexed(len(self.vertices) // 3, gl.GL_QUADS, self.quad_indices, ('v3f', self.vertices))
        # draws the triangles
        pyglet.graphics.draw_indexed(len(self.vertices) // 3, gl.GL_TRIANGLES, self.triangle_indices,('v3f', self.vertices))
        gl.glPopMatrix();        
    
            
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
            # press the F1 or F2 key to switch mode
            if symbol ==pyglet.window.key.F1:
                self.mode="view";
            if symbol==pyglet.window.key.F2:
                self.mode="draw";
        
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
                
                #print(self.current_model.triangles);
                
#                print(w)
#                print(h)
#                print(x)
#                print(y)
                ray_casting=Ray_cast(self.current_model);
                ray=ray_casting.build_ray(x,y,button,w,h);
                iInfo=IntersectionInfo();
                if ray_casting.intersect(ray,iInfo):
                    print(iInfo.icoordinate);

# creates the window and sets its properties
window = Window(width=400, height=400, caption='OBJ Viewer', resizable=True)

# starts the application
pyglet.app.run()
