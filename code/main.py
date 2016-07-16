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
import itertools
# from networkx.algorithms import tournament

# x = Site(1,121.21514,31.04986)
# y = Spot(1,121.214355,31.050442)
# print Dist(x,y)
# z = Shop(1,0,93)
CAPACITY = 140
# speed = 0.25
# str_date = '1970-01-01'

def main():
	[ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier] = LoadAll()
	num_dorder = len(ls_dorder)
	total_worker = 0
	cost = 0
	for i in range(0,len(ls_site)):
		site = copy(ls_site[i])
		ls_spot_per_site = []
		ls_res = []
		temp_order = {}
		[ls_spot_per_site,temp_order] = FindSpotPerSite(site,ls_spot,ls_dorder)
		ls_nbrs = KNNLoc(ls_spot_per_site,40)
		o_graph = BuildKNNGraph(site,ls_spot_per_site,ls_nbrs,temp_order,CAPACITY)
		oplt = PlotGraph(o_graph,site,ls_spot)
		ls_res_raw1 = FindNaiveAssign(site,o_graph,CAPACITY,temp_order)
		ls_res_raw2 = FindAFar(site,o_graph,CAPACITY,temp_order)
		ls_res_raw3 = FindADir(site,o_graph,CAPACITY,temp_order,ls_site,ls_spot,ls_shop)
		ls_res_raw4 = FindADirFar(site,o_graph,CAPACITY,temp_order,ls_site,ls_spot,ls_shop)
		# print len(ls_res_raw)
		print 'The ' + str(i) + ' th site ..............'
		tcost1 = 0
		tcost2 = 0
		tcost3 = 0
		tcost4 = 0
		ls_res1 = ApprxHamilt(ls_res_raw1,ls_site,ls_spot,ls_shop)
		ls_res2 = ApprxHamilt(ls_res_raw2,ls_site,ls_spot,ls_shop)
		ls_res3 = ApprxHamilt(ls_res_raw3,ls_site,ls_spot,ls_shop)
		ls_res4 = ApprxHamilt(ls_res_raw4,ls_site,ls_spot,ls_shop)
		ls_trip1 = ComputeTimeTbl(ls_res1,ls_site,ls_spot,ls_shop)
		ls_trip2 = ComputeTimeTbl(ls_res2,ls_site,ls_spot,ls_shop)
		ls_trip3 = ComputeTimeTbl(ls_res3,ls_site,ls_spot,ls_shop)
		ls_trip4 = ComputeTimeTbl(ls_res4,ls_site,ls_spot,ls_shop)
		for trip in ls_trip1:
			tcost1 = copy(tcost1) + copy(trip['cost'])
		for trip in ls_trip2:
			tcost2 = copy(tcost2) + copy(trip['cost'])
		for trip in ls_trip3:
			tcost3 = copy(tcost3) + copy(trip['cost'])
		for trip in ls_trip4:
			tcost4 = copy(tcost4) + copy(trip['cost'])
		min_cost = min([tcost1,tcost2,tcost3,tcost4])
		if tcost1 == min_cost:
			ls_res = copy(ls_res1)
		elif tcost2 == min_cost:
			ls_res = copy(ls_res2)
		elif tcost3 == min_cost:
			ls_res = copy(ls_res3)
		else:
			ls_res = copy(ls_res4)
		# for res in ls_res:
		# 	print res
		# break
		PlotAssign(oplt,o_graph,ls_res)
		oplt.savefig('../figures/site' + str(GetId(site.sid)+1) + 'zgraph.jpg',format = 'jpg')
		oplt.clf()
		total_worker = copy(total_worker) + len(ls_res)
		cost = copy(cost) + min_cost
		# if i == 30:
		# 	break
	print 'total_worker is ',total_worker
	print 'total cost is ', cost
		# break
	# PlotSpotPerSite(ls_site,ls_spot,ls_dorder)
	# print len(ls_site)
	return

if __name__ == "__main__":
    main()