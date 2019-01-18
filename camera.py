#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:44:54 2019

@author: weilunhuang
"""
import euclid
import pyglet
from pyglet.gl import gl
from pyglet.gl import glu

###fix camera eye, direction, up and use matrix multiplication to change camera view
class Camera(object):
    """ A camera.
    """
    def __init__(self,eye=euclid.Vector3(0,0,5),\
                 direction=euclid.Vector3(0,0,-1),\
                 up=euclid.Vector3(0,1,0)):
        self.eye=eye;
        self.direction=direction.normalized();
        self.up=up.normalized();
        self.right=self.direction.cross(self.up).normalized();
        self.tx,self.ty,self.tz,self.rx,self.ry,self.rz=0,0,0,0,0,0;
        
    def view(self):
        """ Adjust window size.
        """
        # sets the model view
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity();
        glu.gluLookAt(self.eye[0],self.eye[1],self.eye[2],\
                      self.eye[0]+self.direction[0],self.eye[1]+self.direction[1],self.eye[2]+self.direction[2],\
                      self.up[0],self.up[1],self.up[2])
        
    def translate(self,dx, dy, button):
        #move right and up
        if button == pyglet.window.mouse.LEFT:
            delta_x=self.right[0]*dx/20+self.up[0]*dy/20;
            delta_y=self.right[1]*dx/20+self.up[1]*dy/20;
            delta_z=self.right[2]*dx/20+self.up[2]*dy/20;
            self.tx+=delta_x;
            self.ty+=delta_y;
            self.tz+=delta_z;
            gl.glTranslatef(-delta_x,-delta_y,-delta_z);

    def zoom(self,scroll_y):
        #zoom in and out
        delta_x=self.direction[0]* scroll_y / 10.0;
        delta_y=self.direction[1]* scroll_y / 10.0;
        delta_z=self.direction[2]* scroll_y / 10.0;
        self.tx += delta_x;
        self.ty += delta_y;
        self.tz += delta_z;
        gl.glTranslatef(delta_x,delta_y,delta_z);
        
    def rotate(self,dx, dy, button):
        if button == pyglet.window.mouse.RIGHT:
            delta_rx=-dy/10;
            delta_ry=dx/10;
            self.rx+=delta_rx;
            self.ry+=delta_ry;
            gl.glRotatef(-delta_rx,1,0,0);
            gl.glRotatef(-delta_ry,0,1,0);

###modify camera eye, direction, up to change camera view

#class Camera(object):
#    """ A camera.
#    """
#    def __init__(self,eye=euclid.Vector3(0,10,10),\
#                 direction=euclid.Vector3(0,-1,-1),\
#                 up=euclid.Vector3(0,-1,1)):
#        self.eye=eye;
#        self.direction=direction.normalized();
#        self.up=up.normalized();
#        self.right=self.direction.cross(self.up).normalized();
#        self.angle_up=0;
#        self.angle_right=0;
#        self.rotation_center=euclid.Vector3(0,0,0);
#        
#    def view(self):
#        """ Adjust window size.
#        """
#        # sets the model view
#        gl.glMatrixMode(gl.GL_MODELVIEW)
#        gl.glLoadIdentity();
#        glu.gluLookAt(self.eye[0],self.eye[1],self.eye[2],\
#                      self.eye[0]+self.direction[0],self.eye[1]+self.direction[1],self.eye[2]+self.direction[2],\
#                      self.up[0],self.up[1],self.up[2])
#        
#    def translate(self,dx, dy, button):
#        #move right and up
#        if button == pyglet.window.mouse.LEFT:
#            self.eye+=self.right*dx/20;
#            self.eye+=self.up*dy/20;
#        self.view();
#
#    def zoom(self,scroll_y):
#        #zoom in and out
#        self.eye += self.direction* scroll_y / 10.0;
#        self.view();
#    def rotate(self,dx, dy, button):
#        
#        if button == pyglet.window.mouse.LEFT:
#            self.angle_up+=dx/5;
#            self.angle_right-=dy/5;
#            ## rotate about up direction
#            #update self.direction and self.right
#            old_direction=self.direction.copy();
#            self.direction = (self.direction*math.cos(self.angle_up) - self.right*math.sin(self.angle_up)).normalized();
#            self.right = (self.right*math.cos(self.angle_up)+ old_direction*math.sin(self.angle_up)).normalized();
#            #update self.eye        	
#            r = self.eye-self.rotation_center;
#            radius=r.magnitude();
#            r=r.normalized();
#        	v = self.up.cross(r).normalized();
#        	r_updated = (r*math.cos(self.angle_up) + v*math.sin(self.angle_right)).unit();
#        	this->position = center+ r_updated*radius;
#        self.view();
#        
#        
##    def apply(self):
##        """ Apply camera transformation.
##        """
##        gl.glLoadIdentity()
##        gl.glRotatef(self.rx, 1, 0, 0)
##        gl.glRotatef(self.ry, 0, 1, 0)
##        gl.glRotatef(self.rz, 0, 0, 1)

