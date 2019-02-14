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
cutting_vector_color=(1,0,0,1)

# =============================================================================
# IntersectionInfo class, to record intersection information
# =============================================================================
class IntersectionInfo(object):
    
    
    def __init__(self):
        self.icoordinate=None;
        self.normal=None;
        self.text_coordinate=None;
        self.triangleID=None;
        self.cutting_vector=None;
        
    def copy(self):
        iInfo=IntersectionInfo();
        iInfo.icoordinate=self.icoordinate;
        iInfo.normal=self.normal;
        iInfo.text_coordinate=self.text_coordinate;
        iInfo.triangleID=self.triangleID;
        iInfo.cutting_vector=self.cutting_vector;
        
        return iInfo;
        
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
# =============================================================================
# Ray_cast Class, to do ray-castin, find connecting points along surface
# =============================================================================    
class Ray_cast(object):
    def __init__(self,model):
        self.model=model;
        self.points=[];
        self.cutting_vector_points=[];#consists of pairs of point and cut_end point
        self.cutting_vector_points_new=[];
        self.iInfos=[];
    def build_ray(self,mouse_x,mouse_y,button,w,h):
        """
            build ray: from mouse position to a 3D ray (in world coordinate) starting from camera eye position
        """
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
#        print(vector_world);
#        print(M_modelview_inversed);
        #build ray, starting point is camera eye position
        ray=euclid.Ray3(euclid.Point3(M_modelview_inversed[12],M_modelview_inversed[13],M_modelview_inversed[14]),vector_world);
        return ray;
    def intersect(self,ray):
        """
            find intersection between ray and mesh model
        """
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
            
            if len(self.iInfos)>0:
                self.connect(self.iInfos[-1],iInfo);
            self.iInfos.append(iInfo);
            self.points.extend((iInfo.icoordinate[0],iInfo.icoordinate[1],iInfo.icoordinate[2]));
            self.find_CuttingVector();
            print("cutting vector points:")
            print(self.cutting_vector_points)
        return (mx>-1,iInfo);
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
    def find_center(self):
        """
            find center point of all intersection points
        """
        point=euclid.Point3(0,0,0)
        for iInfo in self.iInfos:
            point+=iInfo.icoordinate;
        return point/len(self.iInfos);
    def find_CuttingVectorNew(self):
        """
            find cutting vector on intersection point defined by center
        """
        pass;
#        center=self.find_center();
#        for i,iInfo in enumerate(self.iInfos):
#            d=center-iInfo.icoordinate;
#            d.normalize();
#            #if d and surface normal are too close
#            if d.dot(iInfo.normal)>0.95:
#                print()
#            else:
#                #get projected vector of d on triangle
#                d_proj=d-d.dot(iInfo.normal)/iInfo.normal.magnitude_squared()*(iInfo.normal);
#                v_proj.normalize();
            
    def find_CuttingVector(self):
        """
            find cutting vector on intersection point
        """
        print("len of cutting vector points(before)")
        print(len(self.cutting_vector_points))
        print("len of self.iInfos")
        print(len(self.iInfos))
        for i in range(len(self.cutting_vector_points)//6,len(self.iInfos)-1):
            print("i is")
            print(i)
            print("iInfos[i+1]:")
            print(self.iInfos[i+1].icoordinate)
            print("iInfos[i]:")
            print(self.iInfos[i].icoordinate)
            v=self.iInfos[i+1].icoordinate-self.iInfos[i].icoordinate;
            print("v is:")
            print(v)
            print("normal of iInfo i is")
            print(self.iInfos[i].normal)
            vector=self.iInfos[i].normal.cross(v);
            vector.normalize();
            print("vector is")
            print(vector);
            self.iInfos[i].cutting_vector=vector;
            cut_end=self.iInfos[i].icoordinate+vector;
            self.cutting_vector_points.extend((self.iInfos[i].icoordinate[0],self.iInfos[i].icoordinate[1],self.iInfos[i].icoordinate[2]));
            self.cutting_vector_points.extend((cut_end[0],cut_end[1],cut_end[2]));
        print("len of cutting vector points(after)")
        print(len(self.cutting_vector_points))
    def find_connect_point(self,iInfo,ray_proj,triangle_dic):
        """
            find vector on intersection point, called in connect()
        """
        #set small number for floating point problem
        small_num=0.000001;
        ###find connecting point
        t=-1;
        triangle=self.model.triangles[iInfo.triangleID];
        rays=[euclid.Ray3(triangle.vertices[0],triangle.vertices[1]),\
              euclid.Ray3(triangle.vertices[1],triangle.vertices[2]),\
              euclid.Ray3(triangle.vertices[2],triangle.vertices[0])]
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
        #iterate self.model.triangles to find next triangleID
        for i,tri_temp in enumerate(self.model.triangles):
            #find triangle that consists of two vertice to build ray
            #and find triangle whose ID is not yet in triangle_dic
            if triangle.vertex_indices[ray_id] in tri_temp.vertex_indices and triangle.vertex_indices[(ray_id+1)%3] in tri_temp.vertex_indices and i not in triangle_dic:
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
        
        while(iInfo.triangleID!=iInfo_end.triangleID):
            
            triangle_dic[iInfo.triangleID]=counter;
            print("triangle Info:")
            print("triangleID is "+str(iInfo.triangleID))
            print("vertices:")
            print(self.model.triangles[iInfo.triangleID].vertex_indices)
            print(self.model.triangles[iInfo.triangleID].vertices);
            
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
            iInfo.normal=self.model.triangles[iInfo.triangleID].plane.n;
            
            print('connecting point'+str(counter)+" inside triangle"+str(iInfo.triangleID));
            print(iInfo.icoordinate);
            
            iInfoTemp=iInfo.copy();
            self.iInfos.append(iInfoTemp);
            self.points.extend((iInfo.icoordinate[0],iInfo.icoordinate[1],iInfo.icoordinate[2]));
           
    def spline(self):
        pass;    
    def draw(self):
        #pass
        gl.glColor4f(*point_color);
        gl.glPointSize(5)
        pyglet.graphics.draw(len(self.points)//3,gl.GL_POINTS,('v3f',self.points));
        if len(self.points)//3>1:
            pyglet.graphics.draw(len(self.points)//3,gl.GL_LINE_STRIP,('v3f',self.points));
            gl.glColor4f(*cutting_vector_color);
            pyglet.graphics.draw(len(self.cutting_vector_points)//3,gl.GL_LINES,('v3f',self.cutting_vector_points));
            
