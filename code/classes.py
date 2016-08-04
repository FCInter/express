# import csv
# from copy import copy
# import os
# from math import asin,acos,atan,sqrt,sin,cos,tan,pi
# import classes
# from datetime import datetime
# import time
# from classes import *
# from tools import *
# from load import *
# import networkx as nx

class Site(object):
	"""docstring for Site"""
	sid = 0
	lat = 0.0
	lng = 0.0
	def __init__(self,sid,lng,lat):
		self.sid = sid
		self.lat = lat
		self.lng = lng

class Spot(object):
	"""docstring for Spot"""
	sid = 0
	lat = 0.0
	lng = 0.0
	def __init__(self,sid,lng,lat):
		self.sid = sid
		self.lat = lat
		self.lng = lng

class Shop(object):
	"""docstring for Shop"""
	sid = 0
	lat = 0.0
	lng = 0.0
	def __init__(self,sid,lng,lat):
		self.sid = sid
		self.lat = lat
		self.lng = lng

class DOrder(object):
	"""docstring for Order"""
	oid = 0
	spotid = 0
	siteid = 0
	num = 0
	def __init__(self, oid,spotid,siteid,num):
		self.oid = oid
		self.spotid = spotid
		self.siteid = siteid
		self.num = num

class OtOOrder(object):
	"""docstring for OtOOrder"""
	oid = 0
	spotid = 0
	shopid = 0
	ptime = 0
	dtime = 0
	num = 0
	ddl = 0
	def __init__(self, oid,spotid,shopid,ptime,dtime,num):
		self.oid = oid
		self.spotid = spotid
		self.shopid = shopid
		self.ptime = ptime
		self.dtime = dtime
		self.num = num
		self.ddl = 0

class Courier(object):
	"""docstring for Courier"""
	cid = 0
	ls_odr = []
	capacity = 140
	volume = 0
	lng = 0
	lat = 0
	avait = 0
	availng = 0
	availat = 0
	avaiv = 0
	def __init__(self, cid):
		self.cid = cid
		self.ls_odr = []
		self.capacity = 140
		self.volume = 0
		self.lng = 0
		self.lat = 0
		self.avait = 0
		self.availng = 0
		self.availat = 0
		self.avaiv = 0

class GOrder(object):
	"""docstring for StartPoint"""
	oid = 0
	oriid = 0
	destid = 0
	ptime = 0
	dtime = 0
	num = 0
	def __init__(self, oid,oriid,destid,ptime,dtime,num):
		self.oid = oid
		self.oriid = oriid
		self.destid = destid
		self.ptime = ptime
		self.dtime = dtime
		self.num = num

class TaskPersite(object):
	sid = 0
	lng = 0
	lat = 0
	ls_dtask = []
	ls_oto = []
	ls_fulltask = []
	def __init__(self, sid, lng, lat):
		self.sid = sid
		self.lng = lng
		self.lat = lat
		self.ls_dtask = []
		self.ls_oto = []
		self.ls_fulltask = []

speed = 0.25
str_date = '1970-01-01'

def main():
	print speed
	difflng1 = 121.481796 - 121.486181
	difflat1 = 31.268236 - 31.270203
	difflng2 = 121.483459 - 121.486181
	difflat2 = 31.26614 - 31.270203
	dir1 = DirTwoPi(difflng1,difflat1)
	dir2 = DirTwoPi(difflng2,difflat2)
	print dir1, dir2
	print ComputeDirDiff(dir1, dir2)
	return

if __name__ == "__main__":
    main()