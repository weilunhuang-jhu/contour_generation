#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:50:35 2019

@author: weilunhuang
"""
import euclid
import pyglet
from pyglet.gl import gl

point_color=(1,1,0,1)

class IntersectionInfo(object):
    
    def __init__(self):
        self.icoordinate=None;
        self.normal=None;
        self.texct_coordinate=None;
        self.triangleID=None;

class Triangle(object):
    
    def __init__(self,p1,p2,p3):
        self.vertices=[p1,p2,p3]; #list of vertices
        self.plane=euclid.Plane(self.vertices[0],self.vertices[1],self.vertices[2]);
        self.plane.n.normalize();
        self.v1=self.vertices[1]-self.vertices[0];
        self.v2=self.vertices[2]-self.vertices[0];
    def intersect(self,ray):
        iInfo=IntersectionInfo();
        ray.v.normalize();
        try:
            t=-(self.plane.n.dot(ray.p)-self.plane.k)/ray.v.dot(self.plane.n)
        except ZeroDivisionError:
            return (False,iInfo);
        #print("t is:")
        #print(t);
        if t>0:
            intersection=ray.p+ray.v*t;
            v=intersection-self.vertices[0];
            n_beta=self.plane.n.cross(self.v2);
            n_gamma=self.plane.n.cross(self.v1);
            v_beta=n_beta/self.v1.dot(n_beta);
            v_gamma=n_gamma/self.v2.dot(n_gamma);
            beta=v.dot(v_beta);
            gamma=v.dot(v_gamma);
            alpha=1-beta-gamma;
            if alpha>=0 and beta>=0 and gamma>=0:
                iInfo.icoordinate=intersection;
                iInfo.normal=self.plane.n;
                #print("intersection in triangle:")
                #print(intersection)
                #print(self.vertices)
                return (True,iInfo);
            else:
                return (False,iInfo)
        else:
            return (False,iInfo);
        
class Ray_cast(object):
    def __init__(self,model):
        self.model=model;
        self.points=[];
    def build_ray(self,mouse_x,mouse_y,button,w,h):
        #viewport coordinates to normalized device coordinates
        x=2*mouse_x/w-1;
        y=2*mouse_y/h-1;
        #call projection matrix and model view matrix
        M_proj=(gl.GLfloat*16)();
        M_modelview=(gl.GLfloat*16)();
        gl.glGetFloatv(gl.GL_PROJECTION_MATRIX,M_proj);
        gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX,M_modelview);
        M_proj=euclid.Matrix4.new(*(list(M_proj)));
        M_modelview=euclid.Matrix4.new(*(list(M_modelview)));
        M_proj_inversed=M_proj.inverse();
        M_modelview_inversed=M_modelview.inverse();
        #homogeneous clip coordinates
        vector_clip=euclid.Vector3(x,y,-1);
        #eye coordinates
        vector_eye=M_proj_inversed*vector_clip;
        vector_eye=euclid.Vector3(vector_eye[0],vector_eye[1],-1);
        #world coordinates
        vector_world=M_modelview_inversed*vector_eye;
        vector_world.normalize();
        print(vector_world);
        print(M_modelview_inversed);
        #build ray, starting point is camera eye position
        ray=euclid.Ray3(euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]),vector_world);
        return ray;
    def intersect(self,ray):
        iInfo=IntersectionInfo();
        mx=-1;
        iInfo_temp=IntersectionInfo();
        for i,triangle in enumerate(self.model.triangles):
            (isIntersect,iInfo_temp)=triangle.intersect(ray);
            if isIntersect:    
                #print("intersection_temp in outer loop")
                #print(iInfo_temp)
                d=(iInfo_temp.icoordinate-ray.p).magnitude_squared();
                if mx==-1 or d<mx:
                    iInfo=iInfo_temp;
                    iInfo.triangleID=i;
                    mx=d;
        if mx>-1:
            self.points.extend((iInfo.icoordinate[0],iInfo.icoordinate[1],iInfo.icoordinate[2]));
        return (mx>-1,iInfo);
    def line_intersect(self,ray1,ray2):
        """
            find intersection point between two lines
        """
        iInfo=IntersectionInfo();
        small_num=0.000001;
        den=ray2.v.cross(ray1.v);
        d=den.magnitude();
        t=-1;
        #if not paralleled
        if den>small_num:
            g=ray2.p-ray1.p;
            num=ray2.v.cross(g);
            n=num.magnitude();
            t=n/d;
            if(num.dot(den)>0):
                iInfo.icoordinate=ray1.p+t*ray1.v;
            else:
                iInfo.icoordinate=ray1.p-t*ray1.v;
        return(t,iInfo);
        
        
    def connect(self,iInfo1,iInfo2):
        """
            find connecting points along surface
        """
        v12=iInfo2.icoordinate-iInfo1.icoordinate;
        #get projected vector of v12 on plane1
        v_plane1=v12-v12.dot(iInfo1.normal)/iInfo1.normal.magnitude_squared()*iInfo1.normal;
        v_plane1.normalize();
        #build ray with projected vector
        ray1=euclid.Ray3(iInfo1.icoordinate,v_plane1);
        
        iInfo=IntersectionInfo();
        while(iInfo1.triangleID!=iInfo2.triangleID):
            t=-1;
            triangle=self.model.triangles[iInfo1.triangleID];
            rays=[euclid.Ray3(triangle.vertices[1],triangle.vertices[0]),\
                  euclid.Ray3(triangle.vertices[2],triangle.vertices[1]),\
                  euclid.Ray3(triangle.vertices[0],triangle.vertices[2])]
            for r in rays:
                t_temp,iInfo_temp=self.line_intersect(ray1,r);
                if t_temp>t:
                    iInfo=iInfo_temp;
                    t=t_temp;
            
    def spline(self):
        pass;    
    def draw(self):
        #pass
        gl.glColor4f(*point_color);
        pyglet.graphics.draw(len(self.points)//3,gl.GL_POINTS,('v3f',self.points));
        if len(self.points)//3>1:
            pyglet.graphics.draw(len(self.points)//3,gl.GL_LINE_STRIP,('v3f',self.points));
            
