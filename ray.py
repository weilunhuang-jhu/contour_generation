#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:50:35 2019

@author: weilunhuang
"""
import euclid

class IntersectionInfo(object):
    
    def __init__(self):
        self.icoordinate=None;
        self.normal=None;
        self.texct_coordinate=None;

class Triangle(object):
    
    def __init__(self,p1,p2,p3):
        self.vertices=[p1,p2,p3]; #list of vertices
        self.plane=euclid.Plane(self.vertices[0],self.vertices[1],self.vertices[2]);
        self.v1=self.vertices[1]-self.vertices[0];
        self.v2=self.vertices[2]-self.vertices[0];
    def intersect(self,ray,intersection_info):
        intersection=self.plane.intersect(ray);
        if intersection==None:
            return False;
        if (intersection-ray.p)[0]/ray.v[0]<0:
            return False;
        v=intersection-self.vertices[0];
        n_beta=self.plane.n.normalized().cross(self.v2);
        n_gamma=self.plane.n.normalized().cross(self.v1);
        v_beta=n_beta/self.v1.dot(n_beta);
        v_gamma=n_gamma/self.v2.dot(n_gamma);
        beta=v.dot(v_beta);
        gamma=v.dot(v_gamma);
        alpha=1-beta-gamma;
        if alpha>=0 and beta>=0 and gamma>=0:
            intersection_info.icoordinate=intersection;
            intersection_info.normal=self.plane.n.normalized();
            return True;
        else:
            return False;
        
class Ray_cast(object):
    def __init__(self,model):
        self.model=model;
    def build_ray(self,mouse_x,mouse_y,button,w,h):
        #pass
        x=2*mouse_x/w-1;
        y=2*mouse_y/h-1;
        #return ray;
    def intersect(self,ray,iInfo):
        #pass
        mx=-1;
        intersection_temp=IntersectionInfo();
        for triangle in self.model.triangles:
            if triangle.intersect(ray,intersection_temp):
                d=(intersection_temp.icoordinate-ray.p).magnitude();
                if mx==-1 or d<mx:
                    iInfo=intersection_temp;
                    mx=d;
        return mx==-1;
                
        
    def draw(self,point):
        pass
