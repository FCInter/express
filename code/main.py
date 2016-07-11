import csv
from copy import copy
import os
from math import asin,acos,atan,sqrt,sin,cos,tan,pi
import classes
from datetime import datetime
import time
from classes import *
from tools import *
from load import *
import networkx as nx

# x = Site(1,121.21514,31.04986)
# y = Spot(1,121.214355,31.050442)
# print Dist(x,y)
# z = Shop(1,0,93)
CAPACITY = 140
def main():
	[ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier] = LoadAll()
	num_dorder = len(ls_dorder)
	total_worker = 0
	for i in range(0,len(ls_site)):
		site = copy(ls_site[i])
		ls_spot_per_site = []
		ls_res = []
		temp_order = {}
		[ls_spot_per_site,temp_order] = FindSpotPerSite(site,ls_spot,ls_dorder)
		ls_nbrs = KNNLoc(ls_spot_per_site,5)
		o_graph = BuildKNNGraph(site,ls_spot_per_site,ls_nbrs,temp_order,CAPACITY)
		ls_res = FindNaiveAssign(site,o_graph,CAPACITY,temp_order)
		# print ls_res
		print len(ls_res)
		total_worker = copy(total_worker) + len(ls_res)
		# if i >10:
		# 	break
	print 'total_worker is ',total_worker
		# break
	# PlotLoc(ls_spot)
	# PlotLocs(ls_site,ls_spot,ls_shop)
	# PlotSpotPerSite(ls_site,ls_spot,ls_dorder)
	# print len(ls_site)
	# for site in ls_otoorder:
	# 	print site.oid,site.spotid,site.shopid,site.ptime,site.dtime,site.num
	# 	print ls_otoorder[GetId(site.oid)].oid,ls_spot[GetId(site.spotid)].sid,ls_shop[GetId(site.shopid)].sid
	# print ODDist(ls_dorder,ls_site,ls_spot)
	# print ODDist(ls_otoorder,ls_shop,ls_spot)
	return

if __name__ == "__main__":
    main()