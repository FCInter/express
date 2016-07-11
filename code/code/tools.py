import csv
import copy
import os
from math import asin,acos,atan,sqrt,sin,cos,tan,pi
import classes
from datetime import datetime
import time
from classes import *

def Dist(p1,p2):
	#return in km, no rounding
	dist = 0.0
	R = 6378137.0
	lat1 = float(copy.copy(p1.lat))
	lat2 = float(copy.copy(p2.lat))
	lng1 = float(copy.copy(p1.lng))
	lng2 = float(copy.copy(p2.lng))
	dlat = float(lat1 - lat2) / 2.0
	dlng = float(lng1 - lng2) / 2.0
	dist = 2.0 * R * asin(sqrt( sin(pi*dlat/180.0)*sin(pi*dlat/180.0) + cos(pi*lat1/180.0)*cos(pi*lat2/180.0)*sin(pi*dlng/180.0)*sin(pi*dlng/180.0) ))
	dist = copy.copy(dist) / 1000.0
	return dist

def GetId(str_id):
	index = 0
	index = int(str_id[1:len(str_id)]) - 1
	return index

def ProcTime(x):
	#return in minutes with rounding finished
	t = 3.0 * sqrt(float(x)) + 5.0
	t = Round(copy.copy(t))
	return t

def Round(t):
	if t - float(int(copy.copy(t))) < 0.5:
		t = int(copy.copy(t))
	else:
		t = int(copy.copy(t)) + 1
	return t

def TravelTime(p1,p2):
	#return in minutes with rounding finished
	t = 0
	dist = Dist(p1,p2)
	t = dist / speed
	t = Round(copy.copy(t))
	return t