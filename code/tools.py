import csv
from copy import copy
from copy import deepcopy
import os
from math import asin,acos,atan,sqrt,sin,cos,tan,pi
import classes
from datetime import datetime
import time
from classes import *
import numpy as np
from numpy import mean, std
import matplotlib.pyplot as plt
import networkx as nx

def BuildKNNGraph(site,ls_spot_per_site,ls_nbrs,temp_order,CAPACITY):
	o_graph = nx.Graph()
	o_graph.add_node(site.sid)
	for spot in ls_spot_per_site:
		o_graph.add_node(spot.sid)
		o_graph.add_edge(site.sid,spot.sid,weight = Dist(site,spot))
	for j in range(0,len(ls_nbrs)):
		nbrs = copy(ls_nbrs[j])
		for tpk in nbrs:
			if temp_order[ls_spot_per_site[j].sid] + temp_order[ls_spot_per_site[tpk[1]].sid]<=CAPACITY:
				o_graph.add_edge(ls_spot_per_site[j].sid,ls_spot_per_site[tpk[1]].sid,weight = tpk[0])
	return o_graph

def Dist(p1,p2):
	#return in km, no rounding
	dist = 0.0
	R = 6378137.0
	lat1 = float(copy(p1.lat))
	lat2 = float(copy(p2.lat))
	lng1 = float(copy(p1.lng))
	lng2 = float(copy(p2.lng))
	dlat = float(lat1 - lat2) / 2.0
	dlng = float(lng1 - lng2) / 2.0
	dist = 2.0 * R * asin(sqrt( sin(pi*dlat/180.0)*sin(pi*dlat/180.0) + cos(pi*lat1/180.0)*cos(pi*lat2/180.0)*sin(pi*dlng/180.0)*sin(pi*dlng/180.0) ))
	dist = copy(dist) / 1000.0
	return dist

def FindNaiveAssign(site,o_graph,CAPACITY,temp_order):
	ls_res = []
	temp_graph = deepcopy(o_graph)
	# KNNGraph(temp_graph,k,site.sid)
	r = 0
	while temp_graph.number_of_edges()>0:
		res = []
		# print 'round ',r,'................'
		r = r + 1
		# print temp_graph.number_of_edges()
		nbr = KNNGraph(site.sid,temp_graph,1)[0][0]
		res.append([copy(site.sid),0])
		# print nbr
		total_bag = 0
		while total_bag + temp_order[nbr] <= CAPACITY:
			res.append([copy(nbr),temp_order[nbr]])
			# print 'nbr is ', nbr, 'bag is ', temp_order[nbr]
			# print 'number of neighbors is ', temp_graph.neighbors(nbr)
			if len(temp_graph.neighbors(nbr)) <= 1:
				temp_graph.remove_node(nbr)
				total_bag = copy(total_bag) + copy(temp_order[nbr])
				break
			total_bag = copy(total_bag) + copy(temp_order[nbr])
			new_start = copy(nbr)
			nbr = ''
			ls_nbr = KNNGraph(new_start,temp_graph,2)
			# print 'ls_nbr is ',ls_nbr
			if ls_nbr[0][0] == site.sid:
				nbr = copy(ls_nbr[1][0])
			else:
				nbr = copy(ls_nbr[0][0])
			temp_graph.remove_node(new_start)
		ls_res.append(copy(res))
		# print 'total_bag is ', total_bag
	return ls_res

def FindSpotPerSite(site,ls_spot,ls_order):
	num_order = len(ls_order)
	ls_spot_per_site = []
	temp_order = {}
	for j in range(0,num_order):
		if site.sid == ls_order[j].siteid:
			ls_spot_per_site.append(copy(ls_spot[GetId(ls_order[j].spotid)]))
			spotid = GetId(ls_order[j].spotid)
			temp_order[ls_order[j].spotid] = ls_order[j].num
	return [ls_spot_per_site,temp_order]

def GetId(str_id):
	index = 0
	index = int(str_id[1:len(str_id)]) - 1
	return index

def KNNGraph(node,o_graph,k):
	ls_nbr = []
	knn = []
	ls_nbrnodes = o_graph.neighbors(node)
	for nbrnode in ls_nbrnodes:
		ls_nbr.append([copy(nbrnode),copy(o_graph[nbrnode][node]['weight'])])
	# print ls_nbr
	knn = copy(sorted(ls_nbr,key=lambda x:(x[1]))[0:k])
	# print knn
	return knn

def KNNLoc(ls_loc,k):
	num_loc = len(ls_loc)
	ls_nbr = []
	ls_nbrs = []
	k = min([num_loc,copy(k)])
	for i in range(0,num_loc):
		loc = copy(ls_loc[i])
		ls_nbr = []
		for j in range(0,num_loc):
			if i == j:
				continue
			loc2 = copy(ls_loc[j])
			dist = Dist(loc,loc2)
			ls_nbr.append([dist,j])
		ls_tpk = copy(sorted(ls_nbr,key=lambda x: (x[0]))[0:k])
		ls_nbrs.append(copy(ls_tpk))
		# print loc.sid, 'has tpk neighbors : '
		# for tpk in ls_tpk:
		# 	print ls_loc[tpk[1]].sid
	return ls_nbrs

def PlotLoc(ls_loc):
	num = len(ls_loc)
	x = []
	y = []
	for i in range(0,num):
		loc = copy(ls_loc[i])
		x.append(copy(loc.lng))
		y.append(copy(loc.lat))
	plt.scatter(x,y,color = 'g')

	plt.show()

	return

def PlotLocs(ls_site,ls_spot,ls_shop):
	num_site = len(ls_site)
	num_spot = len(ls_spot)
	num_shop = len(ls_shop)
	x = []
	y = []
	for i in range(0,num_spot):
		loc = copy(ls_spot[i])
		x.append(copy(loc.lng))
		y.append(copy(loc.lat))
	plt.scatter(x,y,color = 'g')
	x = []
	y = []
	for i in range(0,num_site):
		loc = copy(ls_site[i])
		x.append(copy(loc.lng))
		y.append(copy(loc.lat))
	plt.scatter(x,y,color = 'r')
	x = []
	y = []
	for i in range(0,num_shop):
		loc = copy(ls_shop[i])
		x.append(copy(loc.lng))
		y.append(copy(loc.lat))
	plt.scatter(x,y,color = 'k')
	plt.savefig('../figures/alllocs.pdf',format = 'pdf')
	plt.show()
	return

def PlotSpotPerSite(ls_site,ls_spot, ls_order):
	num_site = len(ls_site)
	num_spot = len(ls_spot)
	num_order = len(ls_order)
	min_size = 0
	max_size = 140
	min_r = 20
	max_r = 400
	x = []
	y = []
	ls_id = []
	ls_oid_per_site = []
	num = 0
	for i in range(0,num_site):
		ls_id = []
		ls_oid_per_site = []
		x = []
		y = []
		print 'The ' + str(i) + ' th site...........'
		site = copy(ls_site[i])
		for j in range(0,num_order):
			if site.sid == ls_order[j].siteid:
				ls_oid_per_site.append(j)
				spotid = GetId(ls_order[j].spotid)
				ls_id.append(ls_order[j].spotid)
				x.append(copy(ls_spot[spotid].lng))
				y.append(copy(ls_spot[spotid].lat))

		for j in range(0,len(x)):
			r = int(float(min_r) + float(ls_order[ls_oid_per_site[j]].num - min_size) * float(max_r - min_r) / float(max_size - min_size))
			plt.scatter(x[j],y[j],color = 'g',s = r)
		# for j, txt in enumerate(ls_id):
		# 	plt.annotate(txt,(x[j],y[j]))
		# plt.xlim(120.8,122.2)
		# plt.ylim(30.6,32.0)
		plt.scatter(site.lng,site.lat,color = 'r', s = 210)
		plt.savefig('../figures/site' + str(i+1) + 'spot.jpg',format = 'jpg')
		plt.clf()
		num = copy(num) + len(ls_id)
		# if i == 5:
		# break
	print 'total spot is ' + str(num)
	return

def ProcTime(x):
	#return in minutes with rounding finished
	t = 3.0 * sqrt(float(x)) + 5.0
	t = Round(copy(t))
	return t

def ODDist(ls_order,ls_ori,ls_dest,*ls_ori2):
	avg_dist = 0.0
	std_dist = 0.0
	ls_dist = []
	for order in ls_order:
		id_ori = 0
		id_dest = GetId(order.spotid)
		if hasattr(order,'siteid') :
			id_ori = GetId(order.siteid)
			dist = Dist(ls_ori[id_ori],ls_dest[id_dest])
			print order.siteid,order.spotid,dist
		elif hasattr(order,'shopid') :
			id_ori = GetId(order.shopid)
			dist = Dist(ls_ori[id_ori],ls_dest[id_dest])
			print order.shopid,order.spotid,dist
		elif hasattr(order,'oriid') :
			id_ori = GetId()
			if 'A' in order.oriid:
				dist = Dist(ls_ori[id_ori],ls_dest[id_dest])
			if 'B' in order.oriid:
				dist = Dist(ls_ori2[id_ori],ls_dest[id_dest])
		ls_dist.append(dist)
	avg_dist = mean(ls_dist)
	std_dist = std(ls_dist)
	return [avg_dist,std_dist]

def Round(t):
	if t - float(int(copy(t))) < 0.5:
		t = int(copy(t))
	else:
		t = int(copy(t)) + 1
	return t

def TravelTime(p1,p2):
	#return in minutes with rounding finished
	t = 0
	dist = Dist(p1,p2)
	t = dist / speed
	t = Round(copy(t))
	return t