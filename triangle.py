#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:33:12 2019

@author: weilunhuang
"""
import euclid
from intersection_info import IntersectionInfo
# =============================================================================
# Triangle Class, to test intersection with a triangle
# =============================================================================
class Triangle(object):
    
    def __init__(self,i1,i2,i3,p1,p2,p3):
        self.vertex_indices=[i1,i2,i3];
        self.vertices=[p1,p2,p3]; #list of vertices
        self.plane=euclid.Plane(self.vertices[0],self.vertices[1],self.vertices[2]);
        self.plane.n.normalize();
        self.v1=self.vertices[1]-self.vertices[0];
        self.v2=self.vertices[2]-self.vertices[0];
    def intersect(self,ray):
        """
            find intersection between ray and triangle
        """
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
            if self.inside_check(intersection):
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
    def inside_check(self,intersection):
        """
            check if intersection is inside triangle, by Barycentric coordinate
        """
        v=intersection-self.vertices[0];
        n_beta=self.plane.n.cross(self.v2);
        n_gamma=self.plane.n.cross(self.v1);
        v_beta=n_beta/self.v1.dot(n_beta);
        v_gamma=n_gamma/self.v2.dot(n_gamma);
        beta=v.dot(v_beta);
        gamma=v.dot(v_gamma);
        alpha=1-beta-gamma;
        return (alpha>=0 and beta>=0 and gamma>=0)
