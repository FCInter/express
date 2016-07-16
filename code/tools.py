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
from numpy import mean, std, abs
import matplotlib.pyplot as plt
import networkx as nx
import itertools
from shapely.geometry import LineString as LS

def ApprxHamilt(ls_res_raw,ls_site,ls_spot,ls_shop):
	ls_res = []
	site = copy(ls_res_raw[0][0][0])
	for res_raw in ls_res_raw:
		res = []
		if len(res_raw) < 0:
			ls_enum = EnumArrg(res_raw)
			min_cost = 1000000
			bsf = []
			for enum in ls_enum:
				[cost] = ComputeTimeTbl([enum],ls_site,ls_spot,ls_shop)
				# print enum, cost['cost']
				if cost['cost'] <min_cost:
					min_cost = copy(cost['cost'])
					bsf = []
					bsf = copy(enum)
			ls_res.append(copy(bsf))
			continue
		o_graph = 0
		o_graph = nx.Graph()
		for i in range(0,len(res_raw)-1):
			loc1 = GetLoc(res_raw[i][0],ls_site,ls_spot,ls_shop)
			o_graph.add_node(res_raw[i][0],lng = loc1.lng, lat = loc1.lat, bag = copy(res_raw[i][1]))
			for node in o_graph.nodes():
				if node != res_raw[i][0]:
					loc2 = GetLoc(node,ls_site,ls_spot,ls_shop)
					o_graph.add_edge(res_raw[i][0],node,weight=Dist(loc1,loc2))
		T = nx.minimum_spanning_tree(o_graph)
		o_mgraph = 0
		o_mgraph = nx.MultiGraph()
		for i in range(0,len(res_raw)-1):
			o_mgraph.add_node(res_raw[i][0])
		for edge in T.edges(data=True):
			o_mgraph.add_edge(edge[0],edge[1],weight = edge[2]['weight'])
		ls_to_match = []
		for node in o_mgraph.nodes():
			num_nbr = len(o_mgraph.neighbors(node))
			if num_nbr%2 != 0:
				ls_to_match.append(copy(node))
		path = []
		if len(ls_to_match) < 8:
			ls_match = MinPfctMatching(ls_to_match,ls_site,ls_spot,ls_shop)
			for match in ls_match:
				o_mgraph.add_edge(match[0],match[1],weight = match[2])
			path = list(nx.eulerian_circuit(o_mgraph,source = site))
		else:
			for edge in T.edges(data=True):
				o_mgraph.add_edge(edge[0],edge[1],weight = edge[2]['weight'])
			path = list(nx.eulerian_circuit(o_mgraph,source = site))
		res.append([site,0])
		ls_loc = []
		ls_loc.append(site)
		bag = 0
		for segment in path:
			for loc in segment:
				if loc not in ls_loc:
					ls_loc.append(copy(loc))
					for step in res_raw:
						if step[0] == loc:
							bag = copy(step[1])
							break
					res.append([copy(loc),copy(bag)])
		res.append([site,0])
		new_res = []
		new_res = RmCross(res,o_graph)
		# print res
		tcost1 = ComputeTimeTbl([res_raw],ls_site,ls_spot,ls_shop)
		tcost2 = ComputeTimeTbl([res],ls_site,ls_spot,ls_shop)
		tcost3 = copy(tcost1) + copy(tcost2)
		tcost3 = ComputeTimeTbl([new_res],ls_site,ls_spot,ls_shop)
		if tcost1 == min([tcost1,tcost2,tcost3]):
			ls_res.append(copy(res_raw))
		elif tcost2 == min([tcost1,tcost2,tcost3]):
			ls_res.append(copy(res))
		elif tcost3 == min([tcost1,tcost2,tcost3]):
			ls_res.append(copy(new_res))
	return ls_res

def BuildKNNGraph(site,ls_spot_per_site,ls_nbrs,temp_order,CAPACITY):
	o_graph = nx.Graph()
	o_graph.add_node(site.sid,bag = 0, lng = site.lng, lat = site.lat)
	for spot in ls_spot_per_site:
		o_graph.add_node(spot.sid, bag = temp_order[spot.sid], lng = spot.lng, lat = spot.lat)
		o_graph.add_edge(site.sid,spot.sid,weight = Dist(site,spot))
	for j in range(0,len(ls_nbrs)):
		nbrs = copy(ls_nbrs[j])
		for tpk in nbrs:
			if temp_order[ls_spot_per_site[j].sid] + temp_order[ls_spot_per_site[tpk[1]].sid]<=CAPACITY:
				o_graph.add_edge(ls_spot_per_site[j].sid,ls_spot_per_site[tpk[1]].sid,weight = tpk[0])
	return o_graph

def ComputeCoorDirctn(lng1,lat1,lng2,lat2):
	dirctn = 0.0
	difflat = lat2 - lat1
	difflng = lng2 - lng1
	dirctn = DirTwoPi(difflng,difflat)
	return dirctn

def ComputeDirDiff(dir1,dir2):
	dirdiff = 0.0
	diffraw = 0.0
	diffraw = abs(dir1 - dir2)
	if diffraw > pi:
		dirdiff = 2.0 * pi - diffraw
	else:
		dirdiff = diffraw
	return dirdiff

def ComputeNodeDirctn(p1,p2,ls_site,ls_spot,ls_shop):
	[lng1,lat1] = GetLngLat(p1,ls_site,ls_spot,ls_shop)
	[lng2,lat2] = GetLngLat(p2,ls_site,ls_spot,ls_shop)
	return ComputeCoorDirctn(lng1,lat1,lng2,lat2)

def ComputeTimeTbl(ls_trip,ls_site,ls_spot,ls_shop):
	timetable = []
	timestamp = 0
	ls_cost = []
	for trip in ls_trip:
		# print trip
		prev = 0
		prev = GetLoc(copy(trip[0][0]),ls_site,ls_spot,ls_shop)
		table = {}
		table['trip'] = copy(trip)
		cost = 0
		for step in trip:
			locid = copy(step[0])
			bag = copy(step[1])
			loc = 0
			loc = GetLoc(locid,ls_site,ls_spot,ls_shop)
			# print step
			t_travel = TravelTime(prev,loc)
			t_proc = ProcTime(bag)
			if bag == 0:
				t_proc = 0
			# print prev.sid,locid,bag
			prev = 0
			prev = GetLoc(locid,ls_site,ls_spot,ls_shop)
			# print 'travel time: ', t_travel, 'process time: ',t_proc
			cost = copy(cost) + copy(t_travel) + copy(t_proc)
		table['cost'] = copy(cost)
		ls_cost.append(copy(table))
	return ls_cost

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

def DirTwoPi(difflng,difflat):
	dirctn = 0.0
	if difflng == 0.0:
		if difflat > 0.0:
			return pi/2.0
		elif difflat < 0.0:
			return pi * 1.5
		else:
			return 0.0
	if difflat == 0.0:
		if difflng > 0.0:
			return 0.0
		elif difflng < 0.0:
			return pi
	dirraw = atan(difflat/difflng)
	if difflng < 0.0:
		if difflat > 0.0:
			dirctn = copy(dirraw) + pi
		elif difflat < 0.0:
			dirctn = copy(dirraw) + pi
	elif difflng > 0.0:
		if difflat < 0.0:
			dirctn = copy(dirraw) + 2.0 * pi
		elif difflat > 0.0:
			dirctn = copy(dirraw)
	return dirctn

def ED(ls1,ls2):
	dist = 0.0
	# print ls1
	# print ls2
	for i in range(0,len(ls1)):
		dist = copy(dist) + copy((copy(ls1[i]) - copy(ls2[i]))*(copy(ls1[i]) - copy(ls2[i])))
	return dist

def EnumArrg(ls):
	ls_all_arrg = []
	head = [ls[0]]
	tail = [ls[-1]]
	ls_raw = copy(ls[1:(len(ls)-1)])
	ls_arrg_raw = list(itertools.permutations(ls_raw))
	for arrg_raw in ls_arrg_raw:
		arrg = copy(head) + list(copy(arrg_raw)) + copy(tail)
		ls_all_arrg.append(copy(arrg))
	return ls_all_arrg

def EnumHamilt(ls_res_raw,ls_site,ls_spot,ls_shop):
	ls_res = []
	ls_enum = []
	for res_raw in ls_res_raw:
		ls_enum = []
		if len(res_raw > 8):
			print 'I do not suggest you to enumerate paths, because you will have to search in a space with 40000+ items'
			return
		ls_enum = EnumArrg(res_raw)
		# print 'raw is', res_raw
		print 'number of enumerates is ', len(ls_enum)
		min_cost = 1000000
		bsf = []
		for enum in ls_enum:
			[cost] = ComputeTimeTbl([enum],ls_site,ls_spot,ls_shop)
			if cost['cost'] <min_cost:
				min_cost = copy(cost['cost'])
				bsf = []
				bsf = copy(enum)
		ls_res.append(copy(bsf))
	return ls_res

def ExchangeEndPt(edge1,edge2,o_graph):
	end11 = copy(edge1[0])
	end12 = copy(edge1[1])
	end21 = copy(edge2[0])
	end22 = copy(edge2[1])
	o_graph.remove_edge(end11,end12)
	o_graph.remove_edge(end21,end22)
	if nx.has_path(o_graph,end11,end21):
		o_graph.add_edge(end11,end22)
		o_graph.add_edge(end12,end21)
	else:
		o_graph.add_edge(end11,end21)
		o_graph.add_edge(end12,end22)
	return

def FindADir(site,o_graph,CAPACITY,temp_order,ls_site,ls_spot,ls_shop):
	ls_res = []
	temp_graph = deepcopy(o_graph)
	# GraphKNN(temp_graph,k,site.sid)
	r = 0
	prevdir = 0.0
	while temp_graph.number_of_edges()>0:
		res = []
		# print 'round ',r,'................'
		r = r + 1
		# print temp_graph.number_of_edges()
		nbr = GraphKNN(site.sid,temp_graph,1)[0][0]
		prevdir = ComputeNodeDirctn(site.sid,nbr,ls_site,ls_spot,ls_shop)
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
			ls_nbr = GraphDirKNN(site.sid,new_start,temp_graph,2,prevdir,ls_site,ls_spot,ls_shop)
			# print 'ls_nbr is ',ls_nbr
			if ls_nbr[0][0] == site.sid:
				nbr = copy(ls_nbr[1][0])
			else:
				nbr = copy(ls_nbr[0][0])
			temp_graph.remove_node(new_start)
			# print nbr
			prevdir = ComputeNodeDirctn(site.sid,nbr,ls_site,ls_spot,ls_shop)
		res.append([copy(site.sid),0])
		ls_res.append(copy(res))
	return ls_res

def FindADirFar(site,o_graph,CAPACITY,temp_order,ls_site,ls_spot,ls_shop):
	ls_res = []
	temp_graph = deepcopy(o_graph)
	# GraphKNN(temp_graph,k,site.sid)
	r = 0
	prevdir = 0.0
	while temp_graph.number_of_edges()>0:
		res = []
		# print 'round ',r,'................'
		r = r + 1
		# print temp_graph.number_of_edges()
		nbr = GraphKFN(site.sid,temp_graph,1)[0][0]
		prevdir = ComputeNodeDirctn(site.sid,nbr,ls_site,ls_spot,ls_shop)
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
			ls_nbr = GraphDirKNN(site.sid,new_start,temp_graph,2,prevdir,ls_site,ls_spot,ls_shop)
			# print 'ls_nbr is ',ls_nbr
			if ls_nbr[0][0] == site.sid:
				nbr = copy(ls_nbr[1][0])
			else:
				nbr = copy(ls_nbr[0][0])
			temp_graph.remove_node(new_start)
			# print nbr
			prevdir = ComputeNodeDirctn(site.sid,nbr,ls_site,ls_spot,ls_shop)
		res.append([copy(site.sid),0])
		ls_res.append(copy(res))
	return ls_res

def FindAFar(site,o_graph,CAPACITY,temp_order):
	ls_res = []
	temp_graph = deepcopy(o_graph)
	# GraphKNN(temp_graph,k,site.sid)
	r = 0
	while temp_graph.number_of_edges()>0:
		res = []
		# print 'round ',r,'................'
		r = r + 1
		# print temp_graph.number_of_edges()
		nbr = GraphKFN(site.sid,temp_graph,1)[0][0]
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
			ls_nbr = GraphKNN(new_start,temp_graph,2)
			# print 'ls_nbr is ',ls_nbr
			if ls_nbr[0][0] == site.sid:
				nbr = copy(ls_nbr[1][0])
			else:
				nbr = copy(ls_nbr[0][0])
			temp_graph.remove_node(new_start)
		res.append([copy(site.sid),0])
		ls_res.append(copy(res))
		# print 'total_bag is ', total_bag
	return ls_res

def FindNaiveAssign(site,o_graph,CAPACITY,temp_order):
	ls_res = []
	temp_graph = deepcopy(o_graph)
	# GraphKNN(temp_graph,k,site.sid)
	r = 0
	while temp_graph.number_of_edges()>0:
		res = []
		# print 'round ',r,'................'
		r = r + 1
		# print temp_graph.number_of_edges()
		nbr = GraphKNN(site.sid,temp_graph,1)[0][0]
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
			ls_nbr = GraphKNN(new_start,temp_graph,2)
			# print 'ls_nbr is ',ls_nbr
			if ls_nbr[0][0] == site.sid:
				nbr = copy(ls_nbr[1][0])
			else:
				nbr = copy(ls_nbr[0][0])
			temp_graph.remove_node(new_start)
		res.append([copy(site.sid),0])
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

def GetLngLat(locid,ls_site,ls_spot,ls_shop):
	lng = 0.0
	lat = 0.0
	if len(ls_spot) + len(ls_shop) == 0:
		lng = ls_site[GetId(locid)].lng
		lat = ls_site[GetId(locid)].lat
		return [lng,lat]
	if 'A' in locid:
		lng = ls_site[GetId(locid)].lng
		lat = ls_site[GetId(locid)].lat
	elif 'B' in locid:
		lng = ls_spot[GetId(locid)].lng
		lat = ls_spot[GetId(locid)].lat
	elif 'S' in locid:
		lng = ls_shop[GetId(locid)].lng
		lat = ls_shop[GetId(locid)].lat
	return [lng,lat]

def GetLoc(locid,ls_site,ls_spot,ls_shop):
	if len(ls_spot) + len(ls_shop) == 0:
		loc = copy(ls_site[GetId(locid)])
		return loc
	if 'A' in locid:
		loc = copy(ls_site[GetId(locid)])
	elif 'B' in locid:
		loc = copy(ls_spot[GetId(locid)])
	elif 'S' in locid:
		loc = copy(ls_shop[GetId(locid)])
	return loc

def GraphDirKNN(site,node,o_graph,k,prevdir,ls_site,ls_spot,ls_shop):
	# print 'inside GraphDirKNN...'
	ls_nbr = []
	knn = []
	newdir = 0.0
	ls_nbrnodes = o_graph.neighbors(node)
	for nbrnode in ls_nbrnodes:
		newdir = ComputeNodeDirctn(site,nbrnode,ls_site,ls_spot,ls_shop)
		# print site, nbrnode, newdir
		# print ComputeNodeDirctn(site,node,ls_site,ls_spot,ls_shop), prevdir
		dirdiff = ComputeDirDiff(prevdir, newdir)
		# print dirdiff
		ls_nbr.append([copy(nbrnode),copy(dirdiff)])
	knn = copy(sorted(ls_nbr,key=lambda x:(x[1]))[0:k])
	# print node, ':'
	# print sorted(ls_nbr,key=lambda x:(x[1]))
	return knn

def GraphKFN(node,o_graph,k):
	ls_nbr = []
	kfn = []
	ls_nbrnodes = o_graph.neighbors(node)
	for nbrnode in ls_nbrnodes:
		ls_nbr.append([copy(nbrnode),copy(o_graph[nbrnode][node]['weight'])])
	# print ls_nbr
	kfn = copy(sorted(ls_nbr,reverse=True,key=lambda x:(x[1]))[0:k])
	# print kfn
	return kfn

def GraphKNN(node,o_graph,k):
	ls_nbr = []
	knn = []
	ls_nbrnodes = o_graph.neighbors(node)
	for nbrnode in ls_nbrnodes:
		ls_nbr.append([copy(nbrnode),copy(o_graph[nbrnode][node]['weight'])])
	# print ls_nbr
	knn = copy(sorted(ls_nbr,key=lambda x:(x[1]))[0:k])
	# print knn
	return knn

def IsInline(point,seg1,seg2):
	distp1 = sqrt(ED(point,seg1))
	distp2 = sqrt(ED(point,seg2))
	len1 = sqrt(ED(seg1,seg2))
	if abs(copy(len1) - copy(distp1) - copy(distp2)) < 0.0000000001:
		return True
	else:
		return False
	return False

def IsIntersect(edge1,edge2,o_graph):
	lng11 = o_graph.node[edge1[0]]['lng']
	lng12 = o_graph.node[edge1[1]]['lng']
	lng21 = o_graph.node[edge2[0]]['lng']
	lng22 = o_graph.node[edge2[1]]['lng']
	lat11 = o_graph.node[edge1[0]]['lat']
	lat12 = o_graph.node[edge1[1]]['lat']
	lat21 = o_graph.node[edge2[0]]['lat']
	lat22 = o_graph.node[edge2[1]]['lat']
	l1 = LS([(lng11,lat11),(lng12,lat12)])
	l2 = LS([(lng21,lat21),(lng22,lat22)])
	if l1.intersects(l2):
		itsctpt = copy(list(l1.intersection(l2).coords)[0])
		if IsInline(itsctpt,[lng11,lat11],[lng12,lat12]) and IsInline(itsctpt,[lng21,lat21],[lng22,lat22]):
			return True
		else:
			return False
	else:
		return False
	return False

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

def MinPfctMatching(ls_to_match,ls_site,ls_spot,ls_shop):
	ls_match = []
	ls_all_arrg = itertools.permutations(ls_to_match)
	min_cost = 10000000.0
	j = 0
	cost = 0.0
	# for i in range(0,len(ls_to_match)):
	# 	loc1 = GetLoc(ls_to_match[j],ls_site,ls_spot,ls_shop)
	# 	loc2 = GetLoc(ls_to_match[j+1],ls_site,ls_spot,ls_shop)
	# 	cost = copy(cost) + Dist(loc1,loc2)
	# 	j = j + 2
	# 	if j>= len(ls_to_match):
	# 		break
	# print ls_to_match, cost
	for arrg in ls_all_arrg:
		cost = 0.0
		# print arrg
		# print 'length is ' , len(arrg)
		# print arrg[0],arrg[1]
		j = 0
		ls_temp_match = []
		for i in range(0,len(arrg)):
			# print i, 'start'
			loc1 = GetLoc(arrg[j],ls_site,ls_spot,ls_shop)
			# print i
			# print i + 1
			# print i , 'before'
			# i = copy(i) + 1
			# print i , 'after'
			# print copy(i) + 1
			loc2 = GetLoc(arrg[j+1],ls_site,ls_spot,ls_shop)
			dist = Dist(loc1,loc2)
			# print i
			# print i, 'end'
			ls_temp_match.append([loc1.sid,loc2.sid,dist])
			cost = copy(cost) + dist
			j = j + 2
			if j >= len(arrg):
				break
		if cost < min_cost:
			ls_match = []
			ls_match = copy(ls_temp_match)
			min_cost = copy(cost)
	# print ls_match , min_cost
	return ls_match

def PlotAssign(oplt,o_graph,ls_assign):
	for assign in ls_assign:
		for i in range(0,len(assign)-1):
			# print assign[i], assign[i+1]
			locid1 = copy(assign[i][0])
			locid2 = copy(assign[i+1][0])
			lng1 = o_graph.node[locid1]['lng']
			lng2 = o_graph.node[locid2]['lng']
			lat1 = o_graph.node[locid1]['lat']
			lat2 = o_graph.node[locid2]['lat']
			plt.plot([lng1,lng2],[lat1,lat2],linewidth = 2,color = 'b')

	return

def PlotGraph(o_graph,site,ls_spot):
	min_size = 0
	max_size = 140
	min_r = 20
	max_r = 400
	for node in o_graph.nodes():
		if node != site.sid:
			loc = GetLoc(node,ls_spot,[],[])
			r = 0.0
			r = int(float(min_r) + float(o_graph.node[loc.sid]['bag'] - min_size) * float(max_r - min_r) / float(max_size - min_size))
			plt.scatter(loc.lng,loc.lat,color = 'g', s = r)
			plt.annotate(loc.sid,(loc.lng,loc.lat))
	plt.scatter(site.lng,site.lat,color = 'r', s = float(max_r+min_r)/2.0)
	for edge in o_graph.edges():
		# print edge
		locid1 = copy(edge[0])
		locid2 = copy(edge[1])
		lng1 = o_graph.node[locid1]['lng']
		lng2 = o_graph.node[locid2]['lng']
		lat1 = o_graph.node[locid1]['lat']
		lat2 = o_graph.node[locid2]['lat']
		plt.plot([lng1,lng2],[lat1,lat2],linewidth = 0.5,color = '#808080')
		# break
	# plt.savefig('../figures/site' + str(GetId(site.sid)+1) + 'graph.jpg',format = 'jpg')
	# plt.clf()
	return plt

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

def PlotSpotPerSite(ls_site,ls_spot,ls_order):
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
		for j, txt in enumerate(ls_id):
			plt.annotate(txt,(x[j],y[j]))
		# plt.xlim(120.8,122.2)
		# plt.ylim(30.6,32.0)
		plt.scatter(site.lng,site.lat,color = 'r', s = 210)
		plt.savefig('../figures/site' + str(i+1) + 'spot.jpg',format = 'jpg')
		plt.clf()
		num = copy(num) + len(ls_id)
		# if i == 10:
		# 	break
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

def RmCross(res,o_graph):
	new_res = []
	toprint = 0
	if 'B0816' in o_graph.nodes():
		# print o_graph.nodes()
		toprint = 1
	i = 0
	ls_edges = deepcopy(o_graph.edges())
	siteid = copy(res[0][0])
	sitebag = copy(res[0][1])
	for edge in ls_edges:
		o_graph.remove_edge(edge[0],edge[1])
	# print o_graph.edges(data = True)
	# print o_graph.nodes()
	for i in range(0,len(res)-1):
		# print res[i][0],res[i][1]
		o_graph.add_edge(res[i][0],res[i+1][0])
	# print 'BEFORE !!!!!!!!!!!!!!!!!!'
	# print res
	# print o_graph.edges()
	# print o_graph.nodes(data=True)
	isintsct = 1	
	while(isintsct):
		# print 'new round......'
		# print o_graph.edges()
		found = 0
		for i in range(0,len(o_graph.edges())):
			edge1 = copy(o_graph.edges()[i])
			found = 0
			for j in range(0,len(o_graph.edges())):
				if i == j:
					continue
				edge2 = copy(o_graph.edges()[j])
				if IsIntersect(edge1,edge2,o_graph):
					if set(edge1).isdisjoint(edge2):
						ExchangeEndPt(edge1,edge2,o_graph)
						found = 1
						break
			if found == 1:
				break
		# print 'end of for...'
		if found == 0:
			isintsct = 0
			# print 'No intersection!!!!!!!!!!'
			# break
		# else:
		# 	print 'still intersecting....'
	# new_res.append([siteid,sitebag])
	# startid = copy(siteid)
	# print 'before 2nd while loop...........'
	# print o_graph.edge[startid].keys()[0]
	# print siteid
	# print '.................AFTER'
	# print o_graph.edges()
	if len(o_graph.edges()) == 1:
		other = 0
		for node in o_graph.nodes():
			if node != siteid:
				other = copy(node)
				break
		path = [(siteid,other),(other,siteid)]
	else:
		path = list(nx.eulerian_circuit(o_graph,source = siteid))
	for segment in path:
		new_res.append([segment[0],o_graph.node[segment[0]]['bag']])
	new_res.append([siteid,sitebag])
	# print 'PATH............'
	# print path
	# while(o_graph.edge[startid].keys()[0] != siteid):
	# 	nextid = copy(o_graph.edge[startid].keys()[0])
	# 	bag = copy(o_graph.node[nextid]['bag'])
	# 	new_res.append([copy(nextid),copy(bag)])
	# 	startid = copy(nextid)
		# print startid
	# print 'end of 2nd while loop.............'
	# new_res.append([siteid,sitebag])
	# print o_graph.edges()
	# print new_res
	if toprint:
		# print o_graph.nodes()
		print new_res
	return new_res

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