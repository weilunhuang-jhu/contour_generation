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
import math

class Camera_param(object):
    """
        class to store camera eye, direction, up, right, yaw, pitch
    """
    def __init__(self,eye=euclid.Vector3(0,0,5),\
                 direction=euclid.Vector3(0,0,-1),\
                 up=euclid.Vector3(0,1,0), yaw=-90, pitch=0, fov=60):
        
        self.eye=eye;
        self.direction=direction.normalized();
        self.up=up.normalized();
        self.right=self.direction.cross(self.up).normalized();
        self.yaw=yaw;
        self.pitch=pitch;
        self.fov=fov;
        
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

####modify camera eye, direction, up to change camera view
class Camera(object):
    """ A camera.
    """
    def __init__(self,eye=euclid.Vector3(0,0,50),\
                 direction=euclid.Vector3(0,0,-1),\
                 up=euclid.Vector3(0,1,0),yaw=-90,pitch=0,fov=60):
        self.init_camera_param=Camera_param(eye,direction,up,yaw,pitch, fov);
        self.camera_param=Camera_param(eye,direction,up,yaw,pitch, fov);
        self.sensitive_t=1.0;
        self.sensitive_z=5;
        self.sensitive_r=0.3;
        self.updateCameraVectors();
        #self.tx,self.ty,self.tz,self.rx,self.ry,self.rz=0,0,0,0,0,0;
        
    def updateCameraVectors(self):
        #update self.direction
        direction=euclid.Vector3(0,0,0);
        direction[0]=math.cos(math.pi*self.camera_param.yaw/180)*math.cos(math.pi*self.camera_param.pitch/180);
        direction[1]=math.sin(math.pi*self.camera_param.pitch/180);
        direction[2]=math.sin(math.pi*self.camera_param.yaw/180)*math.cos(math.pi*self.camera_param.pitch/180);
        self.camera_param.direction=direction;
        #update self.up and self.right
        self.camera_param.right=self.camera_param.direction.cross(self.camera_param.up).normalized();
        self.camera_param.up =self.camera_param.right.cross(self.camera_param.direction).normalized();
        
    def init_view(self):
        # set the model view to initial setting
        gl.glMatrixMode(gl.GL_MODELVIEW);
        gl.glLoadIdentity();
        glu.gluLookAt(self.init_camera_param.eye[0],self.init_camera_param.eye[1],self.init_camera_param.eye[2],\
                      self.init_camera_param.eye[0]+self.init_camera_param.direction[0],self.init_camera_param.eye[1]+self.init_camera_param.direction[1],self.init_camera_param.eye[2]+self.init_camera_param.direction[2],\
                      self.init_camera_param.up[0],self.init_camera_param.up[1],self.init_camera_param.up[2])
        #print(self.init_camera_param.eye)
    def view(self):
        # update the model view
        gl.glMatrixMode(gl.GL_MODELVIEW);
        gl.glLoadIdentity();
        glu.gluLookAt(self.camera_param.eye[0],self.camera_param.eye[1],self.camera_param.eye[2],\
                      self.camera_param.eye[0]+self.camera_param.direction[0],self.camera_param.eye[1]+self.camera_param.direction[1],self.camera_param.eye[2]+self.camera_param.direction[2],\
                      self.camera_param.up[0],self.camera_param.up[1],self.camera_param.up[2])
        #print(self.camera_param.eye)
    def translate(self,dx, dy, button):
        #move left/right, forward/backward
        if button == pyglet.window.mouse.LEFT:
            self.camera_param.eye+=dy*self.camera_param.direction*self.sensitive_t;
            self.camera_param.eye+=dx*self.camera_param.right*self.sensitive_t;
            self.view();

    def zoom(self,scroll_y):
        if (self.camera_param.fov>1 and self.camera_param.fov<=75):
            self.camera_param.fov+=scroll_y;
        #check fov bound
        if self.camera_param.fov<=1:
            self.camera_param.fov=1;
        if self.camera_param.fov>=75:
            self.camera_param.fov=75;
    
        
    def rotate(self,dx, dy, button):
        if button == pyglet.window.mouse.RIGHT:
            self.camera_param.yaw+=dx*self.sensitive_r;
            self.camera_param.pitch+=dy*self.sensitive_r;
            #check pitch bound
            if self.camera_param.pitch>89:
                self.camera_param.pitch=89;
            if self.camera_param.pitch<-89:
                self.camera_param.pitch=-89;
            self.updateCameraVectors();
            self.view();



####fix camera eye, direction, up and use matrix multiplication to change camera view
#class Camera(object):
#    """ A camera.
#    """
#    def __init__(self,eye=euclid.Vector3(0,0,5),\
#                 direction=euclid.Vector3(0,0,-1),\
#                 up=euclid.Vector3(0,1,0)):
#        self.eye=eye;
#        self.direction=direction.normalized();
#        self.up=up.normalized();
#        self.right=self.direction.cross(self.up).normalized();
#        self.sensitive_t=1.0;
#        self.sensitive_z=5;
#        self.sensitive_r=0.3;
#        #self.tx,self.ty,self.tz,self.rx,self.ry,self.rz=0,0,0,0,0,0;
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
#            delta_x=self.right[0]*dx*self.sensitive_t+self.up[0]*dy*self.sensitive_t;
#            delta_y=self.right[1]*dx*self.sensitive_t+self.up[1]*dy*self.sensitive_t;
#            delta_z=self.right[2]*dx*self.sensitive_t+self.up[2]*dy*self.sensitive_t;
#            gl.glTranslatef(-delta_x,-delta_y,-delta_z);
##            M_modelview=(gl.GLfloat*16)();
##            gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
##            M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
##            M_modelview_inversed=M_modelview.inverse();
##            self.eye=euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]);
##            self.view();
#    def zoom(self,scroll_y):
#        #zoom in and out
#        delta_x=self.direction[0]* scroll_y *self.sensitive_z;
#        delta_y=self.direction[1]* scroll_y *self.sensitive_z;
#        delta_z=self.direction[2]* scroll_y *self.sensitive_z;
#        gl.glTranslatef(delta_x,delta_y,delta_z);
##        M_modelview=(gl.GLfloat*16)();
##        gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
##        M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
##        M_modelview_inversed=M_modelview.inverse();
##        self.eye=euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]);
##        self.view();
#    def rotate(self,dx, dy, button):
#        if button == pyglet.window.mouse.RIGHT:
#            delta_rx=-dy*self.sensitive_r;
#            delta_ry=dx*self.sensitive_r;
##            M_modelview=(gl.GLfloat*16)();
##            gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
##            M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
##            M_modelview_inversed=M_modelview.inverse();
##            print("origin:")
##            print(M_modelview_inversed)
#            gl.glRotatef(-delta_rx,1,0,0);
#            gl.glRotatef(-delta_ry,0,1,0);
##            M_modelview=(gl.GLfloat*16)();
##            gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
##            M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
##            M_modelview_inversed=M_modelview.inverse();
##            print("after:")
##            print(M_modelview_inversed)
##            self.direction=euclid.Vector3(M_modelview_inversed[0],M_modelview_inversed[1],M_modelview_inversed[2]).normalize();
##            self.up=euclid.Vector3()
##            self.view();
#
