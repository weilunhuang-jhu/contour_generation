#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 23:02:04 2019

@author: weilunhuang
"""
import euclid
import pyglet
from ray import Triangle
from pyglet.gl import gl

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
                    self.vertices.extend((float(x)*10, float(y)*10, float(z)*10));
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
        for i in range(len(self.quad_indices)//4):
            #put all indices for a quad into points-indices, and then separate it into 2 triangles
            points_indices.extend((self.quad_indices[4*i],self.quad_indices[4*i+1],self.quad_indices[4*i+2],self.quad_indices[4*i+3]));
            p1=euclid.Point3(self.vertices[3*points_indices[0]],self.vertices[3*points_indices[0]+1],self.vertices[3*points_indices[0]+2]);
            p2=euclid.Point3(self.vertices[3*points_indices[1]],self.vertices[3*points_indices[1]+1],self.vertices[3*points_indices[1]+2]);
            p3=euclid.Point3(self.vertices[3*points_indices[2]],self.vertices[3*points_indices[2]+1],self.vertices[3*points_indices[2]+2]);
            p4=euclid.Point3(self.vertices[3*points_indices[3]],self.vertices[3*points_indices[3]+1],self.vertices[3*points_indices[3]+2]);
            self.triangles.append(Triangle(points_indices[0],points_indices[1],points_indices[2],\
                                           p1,p2,p3));
            self.triangles.append(Triangle(points_indices[2],points_indices[3],points_indices[0],\
                                           p3,p4,p1));
            points_indices.clear();
        points_indices.clear();
        for i in range(len(self.triangle_indices)//3):
            #put all indices for a triangle into points_indices
            points_indices.extend((self.triangle_indices[3*i],self.triangle_indices[3*i+1],self.triangle_indices[3*i+2]));
            p1=euclid.Point3(self.vertices[3*points_indices[0]],self.vertices[3*points_indices[0]+1],self.vertices[3*points_indices[0]+2]);
            p2=euclid.Point3(self.vertices[3*points_indices[1]],self.vertices[3*points_indices[1]+1],self.vertices[3*points_indices[1]+2]);
            p3=euclid.Point3(self.vertices[3*points_indices[2]],self.vertices[3*points_indices[2]+1],self.vertices[3*points_indices[2]+2]);
            self.triangles.append(Triangle(points_indices[0],points_indices[1],points_indices[2],\
                                           p1,p2,p3));
            points_indices.clear();
    def subdivision(self):
        pass;
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
