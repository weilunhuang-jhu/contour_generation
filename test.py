#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 14:35:53 2019

@author: weilunhuang
"""
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

try:
    1/0;
except ZeroDivisionError:
    print("got it")