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

####modify camera eye, direction, up to change camera view
#
#class Camera(object):
#    """ A camera.
#    """
#    def __init__(self,eye=euclid.Vector3(0,0,5),\
#                 direction=euclid.Vector3(0,0,-1),\
#                 up=euclid.Vector3(0,1,0)):
#        self.eye=eye;
#        self.direction=direction.normalize();
#        self.up=up.normalized();
#        self.right=self.direction.cross(self.up).normalize();
#        self.pitch=0;
#        self.yaw=-90;
#        self.rotation_center=euclid.Point3(0,0,0);
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
#        if button == pyglet.window.mouse.RIGHT:
#            self.angle_up+=dx/5;
#            self.angle_right-=dy/5;
#            ## rotate about up direction
#            #update self.direction and self.right
#            old_direction=self.direction.copy();
#            self.direction = (self.direction*math.cos(self.angle_up) - self.right*math.sin(self.angle_up)).normalized();
#            self.right = (self.right*math.cos(self.angle_up)+ old_direction*math.sin(self.angle_up)).normalized();
#            #update self.eye        	
##            r = self.eye-self.rotation_center;
##            radius=r.magnitude();
##            r=r.normalized();
##            v = self.up.cross(r).normalize();
##            r_updated = (r*math.cos(self.angle_up) + v*math.sin(self.angle_right)).unit();
##        	this->position = center+ r_updated*radius;
#            self.view();

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
        self.sensitive_t=1.0;
        self.sensitive_z=5;
        self.sensitive_r=0.3;
        #self.tx,self.ty,self.tz,self.rx,self.ry,self.rz=0,0,0,0,0,0;
        
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
            delta_x=self.right[0]*dx*self.sensitive_t+self.up[0]*dy*self.sensitive_t;
            delta_y=self.right[1]*dx*self.sensitive_t+self.up[1]*dy*self.sensitive_t;
            delta_z=self.right[2]*dx*self.sensitive_t+self.up[2]*dy*self.sensitive_t;
            gl.glTranslatef(-delta_x,-delta_y,-delta_z);
#            M_modelview=(gl.GLfloat*16)();
#            gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
#            M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
#            M_modelview_inversed=M_modelview.inverse();
#            self.eye=euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]);
#            self.view();
    def zoom(self,scroll_y):
        #zoom in and out
        delta_x=self.direction[0]* scroll_y *self.sensitive_z;
        delta_y=self.direction[1]* scroll_y *self.sensitive_z;
        delta_z=self.direction[2]* scroll_y *self.sensitive_z;
        gl.glTranslatef(delta_x,delta_y,delta_z);
#        M_modelview=(gl.GLfloat*16)();
#        gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
#        M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
#        M_modelview_inversed=M_modelview.inverse();
#        self.eye=euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]);
#        self.view();
    def rotate(self,dx, dy, button):
        if button == pyglet.window.mouse.RIGHT:
            delta_rx=-dy*self.sensitive_r;
            delta_ry=dx*self.sensitive_r;
#            M_modelview=(gl.GLfloat*16)();
#            gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
#            M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
#            M_modelview_inversed=M_modelview.inverse();
#            print("origin:")
#            print(M_modelview_inversed)
            gl.glRotatef(-delta_rx,1,0,0);
            gl.glRotatef(-delta_ry,0,1,0);
#            M_modelview=(gl.GLfloat*16)();
#            gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
#            M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
#            M_modelview_inversed=M_modelview.inverse();
#            print("after:")
#            print(M_modelview_inversed)
#            self.direction=euclid.Vector3(M_modelview_inversed[0],M_modelview_inversed[1],M_modelview_inversed[2]).normalize();
#            self.up=euclid.Vector3()
#            self.view();

