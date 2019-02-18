#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:38:24 2019

@author: weilunhuang
"""

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
        
