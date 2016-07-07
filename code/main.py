import csv
import copy
import os
from math import asin,acos,atan,sqrt,sin,cos,tan,pi
import classes
from datetime import datetime
import time
from classes import *
from tools import *
from load import *

x = Site(1,0,0)
y = Spot(1,0,180)
z = Shop(1,0,93)

def main():
	[ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier] = LoadAll()
	print len(ls_site)
	for site in ls_otoorder:
		print site.oid,site.spotid,site.shopid,site.ptime,site.dtime,site.num
		print ls_otoorder[GetId(site.oid)].oid,ls_spot[GetId(site.spotid)].sid,ls_shop[GetId(site.shopid)].sid
	return

if __name__ == "__main__":
    main()