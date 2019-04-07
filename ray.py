#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:50:35 2019

@author: weilunhuang
"""
import euclid
import pyglet
import numpy as np
import trimesh
import pyrender
#import networkx as nx
from intersection_info import IntersectionInfo
from pyglet.gl import gl

point_color=np.array([1,0,0,1]).reshape((1,4));
cutting_vector_color=np.array([0,0,1,1]).reshape((1,4));
cutting_vector_by_mean_color=(0,1,0,1)

#m = pyrender.Mesh.from_points(pts, colors=colors)

#create point as a sphere in trimesh
sm = trimesh.creation.uv_sphere(radius=0.0003)
sm.visual.vertex_colors = [1.0, 0.0, 0.0]


# =============================================================================
# Ray_cast Class, to do ray-castin, find connecting points along surface
# =============================================================================    
class Ray_cast(object):
    def __init__(self,model):
        self.model=model;# a trimesh object
        self.points=None;
        self.cutting_vector_points=None;#consists of pairs of point and cut_end point
        #self.cutting_vector_points_by_center=[];
        self.cutting_vector_points_by_mean=None;
        self.iInfos=[];
        self.prev_iInfos=[];
        self.cutting_vector_length=20;
        self.end=False;
    
    def build_ray(self,mouse_x,mouse_y,button,w,h,M_proj,M_modelview_inversed):
        """
            build ray: from mouse position to a 3D ray (in world coordinate) starting from camera eye position
        """
        #viewport coordinates to normalized device coordinates
        x=2*mouse_x/w-1;
        y=2*mouse_y/h-1;
        #use projection matrix and inversed model view matrix        
        M_proj=euclid.Matrix4.new(*(M_proj));
        M_proj_inversed=M_proj.inverse();
        M_modelview_inversed=euclid.Matrix4.new(*(M_modelview_inversed));
        
        #homogeneous clip coordinates
        vector_clip=euclid.Vector3(x,y,-1);
        
        #eye coordinates
        vector_eye=M_proj_inversed*vector_clip;
        vector_eye=euclid.Vector3(vector_eye[0],vector_eye[1],-1);
        
        #world coordinates
        vector_world=M_modelview_inversed*vector_eye;
        vector_world.normalize();
        
        #build ray, starting point is camera eye position
        ray=euclid.Ray3(euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]),vector_world);
        return ray;
        
    def intersect(self,ray):
        """
            find intersection between ray and mesh model
        """
        isIntersect=False;
        iInfo=IntersectionInfo();
        ray_origins=np.array([ray.p[0],ray.p[1],ray.p[2]]);
        ray_origins=ray_origins.reshape((1,3));
        ray_directions=np.array([ray.v[0],ray.v[1],ray.v[2]]);
        ray_directions=ray_directions.reshape((1,3));
        #use ray.intersects_location() in trimesh to find intersection
        locations, index_ray, index_tri = self.model.ray.intersects_location(ray_origins=ray_origins, ray_directions=ray_directions, multiple_hits=False)
        #record points and iInfo if there is intersection
        if index_tri.shape[0]>0:
            isIntersect=True;
            iInfo.icoordinate=euclid.Point3(locations[0,0],locations[0,1],locations[0,2]);
            iInfo.triangleID=index_tri[0];
            iInfo.normal=euclid.Vector3(self.model.face_normals[index_tri,0],self.model.face_normals[index_tri,1],self.model.face_normals[index_tri,2]);
        
            if len(self.iInfos)>0:
                self.connect(self.iInfos[-1],iInfo);
            self.iInfos.append(iInfo);
            if self.points is None:
                self.points=locations;
            else:
                self.points=np.concatenate((self.points,locations));
            self.find_CuttingVectors();
        return isIntersect;
    
    def intersect_on_new_model(self):
        for prev_iInfo in self.prev_iInfos:
            ray=euclid.Ray3(prev_iInfo.icoordinate,-prev_iInfo.cutting_vector);    
            iInfo=IntersectionInfo();
            mx=-1;
            iInfo_temp=IntersectionInfo();
#            ###find nearest intersection
#            for i,triangle in enumerate(self.model.triangles):
#                (isIntersect,iInfo_temp)=triangle.intersect(ray);
#                if isIntersect:    
#                    #print("intersection_temp in outer loop")
#                    #print(iInfo_temp)
#                    d=(iInfo_temp.icoordinate-ray.p).magnitude_squared();
#                    if mx==-1 or d<mx:
#                        iInfo=iInfo_temp;
#                        iInfo.triangleID=i;
#                        mx=d;
            ###find farest intersection
            for i,triangle in enumerate(self.model.triangles):
                (isIntersect,iInfo_temp)=triangle.intersect(ray);
                if isIntersect:    
                    #print("intersection_temp in outer loop")
                    #print(iInfo_temp)
                    d=(iInfo_temp.icoordinate-ray.p).magnitude_squared();
                    if d>mx:
                        iInfo=iInfo_temp;
                        iInfo.triangleID=i;
                        mx=d;
            if mx>-1:
                if len(self.iInfos)>0:
                    self.connect(self.iInfos[-1],iInfo);
                self.iInfos.append(iInfo);
                self.points.extend((iInfo.icoordinate[0],iInfo.icoordinate[1],iInfo.icoordinate[2]));
#                self.find_CuttingVectors();
#                print("cutting vector points:")
#                print(self.cutting_vector_points)
    
    def line_intersect(self,ray1,ray2):
        """
            find intersection point between two rays in 3D
        """
        iInfo=IntersectionInfo();
        small_num=0.000001;
        den=ray2.v.cross(ray1.v);
        d=den.magnitude();
        t=-1;
        #if two lines are not parallel
        if d>small_num:
            g=ray2.p-ray1.p;
            num=ray2.v.cross(g);
            n=num.magnitude();
            t=n/d;
            if(num.dot(den)<0):
                t=-t
            iInfo.icoordinate=ray1.p+t*ray1.v;
        return(t,iInfo);
        
    def generate_CuttingVector(self,iInfo1,iInfo2):
        """
            generate cutting vector on iInfo1 given iInfo2
        """
        v=iInfo2.icoordinate-iInfo1.icoordinate;
        vector=iInfo1.normal.cross(v);
        vector.normalize();
        return vector;
            
    def find_MeanCuttingVector(self):
        """
            find average of all cutting vector
        """
        vector=euclid.Vector3(0,0,0);
        #generate cutting vector for last iInfo
        self.iInfos[-1].cutting_vector=self.generate_CuttingVector(self.iInfos[-1],self.iInfos[0]);
        #find average cutting vector
        for iInfo in self.iInfos:
            vector+=iInfo.cutting_vector;
        return vector/len(self.iInfos);
    
    def find_CuttingVectorByMean(self):
        """
            find average of all cutting vector,
            project the mean cutting vector onto triangles
        """
        mean_vector=self.find_MeanCuttingVector();
        for i,iInfo in enumerate(self.iInfos):
            mean_vector_proj=mean_vector-mean_vector.dot(iInfo.normal)/iInfo.normal.magnitude_squared()*(iInfo.normal);
            mean_vector_proj.normalize();
            self.iInfos[i].cutting_vector=mean_vector_proj;
            cut_end=iInfo.icoordinate+mean_vector_proj*self.cutting_vector_length;
            pairs=np.array([[self.iInfos[i].icoordinate[0],self.iInfos[i].icoordinate[1],self.iInfos[i].icoordinate[2]],\
                            [cut_end[0],cut_end[1],cut_end[2]]]).reshape((2,3));
    
            if self.cutting_vector_points_by_mean is None:
                self.cutting_vector_points_by_mean=pairs;
            else:
#                print(self.cutting_vector_points_by_mean.shape);
#                print(pairs.shape)
                self.cutting_vector_points_by_mean=np.concatenate((self.cutting_vector_points_by_mean,pairs));
            
    def find_CuttingVectors(self):
        """
            find cutting vector on intersection point
        """
        if self.cutting_vector_points is None:
            start_len=0;
        else:
            start_len=len(self.cutting_vector_points)//2;
            
        for i in range(start_len,len(self.iInfos)-1):
            vector=self.generate_CuttingVector(self.iInfos[i],self.iInfos[i+1])
            self.iInfos[i].cutting_vector=vector;
            cut_end=self.iInfos[i].icoordinate+vector*self.cutting_vector_length;
            pairs=np.array([[self.iInfos[i].icoordinate[0],self.iInfos[i].icoordinate[1],self.iInfos[i].icoordinate[2]],\
                            [cut_end[0],cut_end[1],cut_end[2]]]).reshape((2,3));
    
            if self.cutting_vector_points is None:
                self.cutting_vector_points=pairs;
            else:
#                print(self.cutting_vector_points.shape);
#                print(pairs.shape)
                self.cutting_vector_points=np.concatenate((self.cutting_vector_points,pairs));
                
            
    def find_connect_point(self,iInfo,ray_proj,triangle_dic):
        """
            find vector on intersection point, called in connect()
        """
        #set small number for floating point problem
        small_num=0.000001;
        ###find connecting point
        t=-1;
        triangle=self.model.triangles[iInfo.triangleID];
        vertex0=euclid.Point3(triangle[0,0],triangle[0,1],triangle[0,2]);
        vertex1=euclid.Point3(triangle[1,0],triangle[1,1],triangle[1,2]);
        vertex2=euclid.Point3(triangle[2,0],triangle[2,1],triangle[2,2]);
        
        
        rays=[euclid.Ray3(vertex0,vertex1),\
              euclid.Ray3(vertex1,vertex2),\
              euclid.Ray3(vertex2,vertex0)]
        #iterate edges in triangle to find closest intersection for ray_proj
        #and update iInfo
        ray_id=0;
        for i,ray in enumerate(rays):
            print("ray"+str(i)+":");
            (t_temp,iInfo_temp)=self.line_intersect(ray_proj,ray);
            if (t_temp<t or t<0) and t_temp>small_num:
                print(t_temp)
                t=t_temp;
                iInfo.icoordinate=iInfo_temp.icoordinate;
                ray_id=i;
        #find next triangleID
        triangle=self.model.faces[iInfo.triangleID];
        for i,tri_temp in enumerate(self.model.faces):
            #find triangle that consists of two vertice to build ray
            #and find triangle whose ID is not yet in triangle_dic
            if triangle[ray_id] in tri_temp and triangle[(ray_id+1)%3] in tri_temp and i not in triangle_dic:
                iInfo.triangleID=i;
                break;
        return (t,ray_id);
            
    def connect(self,iInfo_start,iInfo_end):
        """
            find connecting points along surface
        """
        #dictionay to keep track of triangle gone through
        triangle_dic={};
        print("=========================")
        print("start ID is")
        print(iInfo_start.triangleID)
        print("end ID is")
        print(iInfo_end.triangleID)
        
        iInfo=iInfo_start.copy();
        iInfo_prev=iInfo.copy();
        counter=0;
        
#        print("triangles")
#        print(self.model.triangles);
#        print(self.model.triangles.shape)
#        print("faces")
#        print(self.model.faces)
#        print(self.model.faces.shape)
        
        while(iInfo.triangleID!=iInfo_end.triangleID):
            
            triangle_dic[iInfo.triangleID]=counter;
            print("triangle Info:")
            print("triangleID is "+str(iInfo.triangleID))
            
            counter+=1;
            #check if triangle normal is too close to previous triangle normal
            #we want to continue the vector direction if the two normals are similar 
            if iInfo_prev.normal.dot(iInfo.normal)/iInfo.normal.magnitude_squared() >0.9:
                v=iInfo_end.icoordinate-iInfo_prev.icoordinate;
            else:
                v=iInfo_end.icoordinate-iInfo.icoordinate;
            #get projected vector of v on triangle
            v_proj=v-v.dot(iInfo.normal)/iInfo.normal.magnitude_squared()*(iInfo.normal);
            v_proj.normalize();
            #build ray with projected vector
            ray_proj=euclid.Ray3(iInfo.icoordinate,v_proj);
            print("ray_proj is:")
            print(ray_proj)
            #keep track of previous iInfo
            iInfo_prev=iInfo.copy();
            #find intersection with t and ray_id, iInfo passed by reference
            t,ray_id=self.find_connect_point(iInfo,ray_proj,triangle_dic);
            print('t is:')
            print(t)
            #check if t < 0, which is intersection in wrong direction
            if(t<0):
                print("error: connecting point in wrong direction");
                break;
#            #check if intersection is inside triangle
#            if not self.model.triangles[iInfo.triangleID].inside_check(iInfo.icoordinate):
#                print("error: connecting point is not in triangle")
#                print("wrong connecting point:")
#                print(iInfo.icoordinate)
#                break;
            #check if triangle found is correct
            if iInfo.triangleID in triangle_dic:
                print("error: wrong triangle found")
                break;
            #update iInfo.normal
            iInfo.normal=euclid.Vector3(self.model.face_normals[iInfo.triangleID,0],\
                                        self.model.face_normals[iInfo.triangleID,1],\
                                        self.model.face_normals[iInfo.triangleID,2]);
        
            print('connecting point'+str(counter)+" inside triangle"+str(iInfo.triangleID));
            print(iInfo.icoordinate);
            
            iInfoTemp=iInfo.copy();
            self.iInfos.append(iInfoTemp);
            new_point=np.array([iInfo.icoordinate[0],iInfo.icoordinate[1],iInfo.icoordinate[2]]).reshape((1,3));
            self.points=np.concatenate((self.points,new_point));
            
    def spline(self):
        pass;    
    def draw(self):
        #pass
#        colors=np.random.uniform(size=points.shape);
#        temp=pyrender.Mesh.from_points(points,colors=colors);
                
        #create point_mesh
        tfs = np.tile(np.eye(4), (len(self.points), 1, 1));
        tfs[:,:3,3] = self.points;
        point_mesh = pyrender.Mesh.from_trimesh(sm, poses=tfs);
        point_mesh.name="point_mesh";
        
        #create cutting_vector_mesh
        if self.end:
            cutting_vector_mesh=pyrender.Primitive(positions=self.cutting_vector_points_by_mean,mode=1);
            cutting_vector_mesh = pyrender.Mesh([cutting_vector_mesh]);
            cutting_vector_mesh.name="cutting_vector_mesh";
            return (point_mesh,cutting_vector_mesh);
        else:
            if self.cutting_vector_points is not None:
                cutting_vector_mesh=pyrender.Primitive(positions=self.cutting_vector_points,mode=1);
                cutting_vector_mesh = pyrender.Mesh([cutting_vector_mesh]);
                cutting_vector_mesh.name="cutting_vector_mesh";
                return (point_mesh,cutting_vector_mesh);
            else:
                return (point_mesh,);