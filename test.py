#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 14:35:53 2019

@author: weilunhuang
"""
import euclid
#from scipy import interpolate
#import numpy as np
#import matplotlib.pyplot as plt
#vertices = [];
#vertex_nomals=[];
#text_coord=[];
#faces=[];
#
#path='./obj/box.obj';
#with open(path) as obj_file:
#    for line in obj_file.readlines():
#        # reads the file line by line
#        data = line.split();
#        print(data);
#        if len(data)==0 or data[0] not in ['v','vn','vt','f']:
#            continue;
#        if data[0] == 'v':
#            x, y, z = data[1:4];
#            vertices.extend((float(x), float(y), float(z)));
#        # every line that begins with a 'vn' is a vertex normal
#        if data[0] == 'vn':
#            x_n, y_n, z_n = data[1:4];
#            vertex_nomals.extend((float(x_n), float(y_n), float(z_n)));
#        # every line that begins with a 'vt' is a text coordinate
#        if data[0] == 'vt':
#            t_u, t_v= data[1:3];
#            text_coord.extend((float(t_u), float(t_v)));
#        # every line that begins with an 'f' is a face
#        # loads the faces
#        elif data[0] == 'f':
#            vi_1, vi_2, vi_3 = data[1:4]
#            faces.extend((vi_1,vi_2,vi_3))
#point1=[0,0];
#point2=[0,1];
#point3=[1,1];
#point4=[1,0];
#
#x=np.arange(4);
#y=np.array([point1,point2,point3,point4]);
#cs=interpolate.CubicSpline(x,y);
#plt.plot(y[:,0],y[:,1]);
#plt.plot(cs(xs)[:,0],cs(xs)[:,1])
#plt.show()

ray1=euclid.Ray3(euclid.Point3(0,0,0),euclid.Point3(1,1,1));
ray2=euclid.Ray3(euclid.Point3(1,1,0),euclid.Point3(1,1,-0.5));
def line_intersect(ray1,ray2):
    """
        find intersection point between two lines
    """
    small_num=0.000001;
    den=ray2.v.cross(ray1.v);
    d=den.magnitude();
    t=-1;
    #if not paralleled
    if d>small_num:
        g=ray2.p-ray1.p;
        num=ray2.v.cross(g);
        n=num.magnitude();
        t=n/d;
        if(num.dot(den)<0):
            t=-t
        print(t)
        print(ray1.p+t*ray1.v);
        
line_intersect(ray1,ray2)