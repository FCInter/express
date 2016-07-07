import csv
import copy
import os
import datetime
import time
from datetime import datetime
from classes import *

def LoadAll():
	fname1 = '../data/1.csv'
	fname2 = '../data/2.csv'
	fname3 = '../data/3.csv'
	fname4 = '../data/4.csv'
	fname5 = '../data/5.csv'
	fname6 = '../data/6.csv'
	ls_site = LoadSite(fname1)
	ls_spot = LoadSpot(fname2)
	ls_shop = LoadShop(fname3)
	ls_dorder = LoadDOrder(fname4)
	ls_otoorder = LoadOtOOrder(fname5)
	ls_courier = LoadCourier(fname6)
	return [ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier]

def LoadSite(filename):
	ls_site = []
	f = open(filename,'rU')
	rdr = csv.reader(f)
	i = 0
	lsd = list(rdr)
	del lsd[0]
	for row in sorted(lsd,key=lambda x: (x[0])):
		sid = row[0]
		lng = float(row[1])
		lat = float(row[2])
		x = Site(sid,lng,lat)
		ls_site.append(x)
	return ls_site

def LoadSpot(filename):
	ls_spot = []
	f = open(filename,'rU')
	rdr = csv.reader(f)
	i = 0
	lsd = list(rdr)
	del lsd[0]
	for row in sorted(lsd,key=lambda x: (x[0])):
		sid = row[0]
		lng = float(row[1])
		lat = float(row[2])
		x = Spot(sid,lng,lat)
		ls_spot.append(x)
	return ls_spot

def LoadShop(filename):
	ls_shop = []
	f = open(filename,'rU')
	rdr = csv.reader(f)
	i = 0
	lsd = list(rdr)
	del lsd[0]
	for row in sorted(lsd,key=lambda x: (x[0])):
		sid = row[0]
		lng = float(row[1])
		lat = float(row[2])
		x = Shop(sid,lng,lat)
		ls_shop.append(x)
	return ls_shop

def LoadDOrder(filename):
	ls_dorder = []
	f = open(filename,'rU')
	rdr = csv.reader(f)
	i = 0
	lsd = list(rdr)
	del lsd[0]
	for row in sorted(lsd,key=lambda x: (x[0])):
		oid = row[0]
		spotid = row[1]
		siteid = row[2]
		num = int(row[3])
		x = DOrder(oid,spotid,siteid,num)
		ls_dorder.append(x)
	return ls_dorder

def LoadOtOOrder(filename):
	#the ptime and dtime are all in minutes
	ls_otoorder = []
	f = open(filename,'rU')
	rdr = csv.reader(f)
	i = 0
	lsd = list(rdr)
	del lsd[0]
	for row in sorted(lsd,key=lambda x: (x[0])):
		oid = row[0]
		spotid = row[1]
		shopid = row[2]
		str_ptime = copy.copy(str_date) + 'T' + copy.copy(row[3]) + ':00'
		str_dtime = copy.copy(str_date) + 'T' + copy.copy(row[4]) + ':00'
		ptime = int(time.mktime(datetime.strptime(str_ptime,"%Y-%m-%dT%H:%M:%S").timetuple())/60.0)
		dtime = int(time.mktime(datetime.strptime(str_dtime,"%Y-%m-%dT%H:%M:%S").timetuple())/60.0)
		num = int(row[5])
		x = OtOOrder(oid,spotid,shopid,ptime,dtime,num)
		ls_otoorder.append(x)
	return ls_otoorder

def LoadCourier(filename):
	ls_courier = []
	f = open(filename,'rU')
	rdr = csv.reader(f)
	i = 0
	lsd = list(rdr)
	del lsd[0]
	for row in sorted(lsd,key=lambda x: (x[0])):
		cid = row[0]
		x = Courier(cid)
		ls_courier.append(x)
	return ls_courier


