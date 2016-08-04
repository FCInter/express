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
import operator

def AssignOTO(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoorder,ls_courier):
	ls_fulltask = []
	ls_otoodr_sort = sorted(ls_otoorder, key = operator.attrgetter('ptime'))
	ls_asgn_odr = []
	ls_asgn_dtsk = []
	num_otoorder = len(ls_otoodr_sort)
	num_site = len(ls_site)
	ls_pure_oto = []
	fulltask = 0
	ComputeOTODDL(ls_otoodr_sort,ls_site,ls_spot,ls_shop)
	ls_osite = GroupTasks(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoodr_sort)
	# print ls_osite[0].ls_dtask[0]
	# print ComputeTripVol(ls_osite[0].ls_dtask[0])
	# print ComputeTripCost(ls_osite[0].ls_dtask[0],ls_site,ls_spot,ls_shop,1)
	count = 0
	count_not = 0
	for i in range(0,num_site):
		num_dtask = len(ls_osite[i].ls_dtask)
		num_oto = len(ls_osite[i].ls_oto)
		if num_oto == 0:
			for j in range(0,num_dtask):
				ls_osite[i].ls_fulltask.append({"id":[copy(i),copy(j)],"task":copy(ls_osite[i].ls_dtask[j]["task"]),"assigned":0})
				count = copy(count) + 1
			ls_osite[i].ls_dtask = []
		# else:
		# 	loc1 = Site(ls_osite[i].sid,ls_osite[i].lng,ls_osite[i].lat)
		# 	loc2 = GetLoc(ls_osite[i].ls_oto[0][0].shopid,ls_site,ls_spot,ls_shop)
		# 	earliest = copy(ls_osite[i].ls_oto[0][0].ptime) - TravelTime(loc1,loc2)
		# 	for j in range(0,num_dtask):
		# 		cost = ComputeTripCost(ls_osite[i].ls_dtask[j],ls_site,ls_spot,ls_shop)
		# 		if cost < earliest:
		# 			ls_osite[i].ls_fulltask.append({"id":[copy(i),copy(j)],"task":copy(ls_osite[i].ls_dtask[j]),"assigned":0})
		# 			count = copy(count) + 1
		# 	templs = deepcopy(ls_osite[i].ls_dtask)
		# 	ls_osite[i].ls_dtask = []
		# 	for j in range(0,num_dtask):
		# 		isfound = 0
		# 		for k in range(0,len(ls_osite[i].ls_fulltask)):
		# 			if ls_osite[i].ls_fulltask[k]["task"] == templs[j]:
		# 				isfound = 1
		# 				break
		# 		if isfound == 0:
		# 			ls_osite[i].ls_dtask.append(copy(templs[j]))
		# 			count_not = copy(count_not) + 1
	print 'count is ',count, 'count_not is ', count_not
	# crir_id = 0
	# num_crir = len(ls_courier)
	# count_taken = 0
	# for i in range(0,num_site):
	# 	num_oto = len(ls_osite[i].ls_oto)
	# 	if num_oto > 0:
	# 		continue
	# 	num_fulltask = len(ls_osite[i].ls_fulltask)
	# 	count_assigned = 0
	# 	count_assigned_pp = 0
	# 	need_change = 1
	# 	for j in range(0,num_fulltask):
	# 		if crir_id < num_crir:
	# 			ls_courier[crir_id].volume = ComputeTripVol(ls_osite[i].ls_fulltask[j]["task"])
	# 			ls_osite[i].ls_fulltask[j]["assigned"] = 1
	# 			ls_courier[crir_id].ls_odr.append(copy(ls_osite[i].ls_fulltask[j]))
	# 			# [lng,lat] = GetLngLat(ls_osite[i].ls_fulltask[j]["task"][-2][0],ls_site,ls_spot,ls_shop)
	# 			ls_courier[crir_id].availng = ls_osite[i].lng
	# 			ls_courier[crir_id].availat = ls_osite[i].lat
	# 			ls_courier[crir_id].availt = ComputeTripCost(ls_osite[i].ls_fulltask[j]["task"],ls_site,ls_spot,ls_shop) + copy(ls_courier[crir_id].t)
	# 			ls_courier[crir_id].availv = 0
	# 			ls_courier[crir_id].lng = ls_osite[i].lng
	# 			ls_courier[crir_id].lat = ls_osite[i].lat
	# 			# print 'sender ' + str(crir_id) + ' takes misson ' + str(i) + ', ' + str(j) + ' of site ' + str(ls_osite[i].sid) + ' at time ' + str(ls_courier[crir_id].t)
	# 			count_taken = copy(count_taken) + 1
	# 			# print ls_osite[i].ls_fulltask[j]["task"]
	# 			# print ComputeTripVol(ls_osite[i].ls_fulltask[j]["task"])
	# 			# break
	# 			count_assigned_pp = copy(count_assigned_pp) + 1
	# 			ls_courier[crir_id].t = copy(ls_courier[crir_id].availt)
	# 			ls_courier[crir_id].lng = copy(ls_courier[crir_id].availng)
	# 			ls_courier[crir_id].lat = copy(ls_courier[crir_id].availat)
	# 			need_change = 1
	# 			if count_assigned_pp >= 3:
	# 				crir_id = copy(crir_id) + 1
	# 				count_assigned_pp = 0
	# 				need_change = 0
	# 	if need_change:
	# 		crir_id = copy(crir_id) + 1
	# print 'In total, ' + str(count_taken) + ' dtasks have been taken'
	count_oto_notassigned = 0
	for i in range(0,num_site):
		# if i < 8:
		# 	continue
		if i > 10:
			break
		num_oto = len(ls_osite[i].ls_oto)
		print 'site ' + str(i) + ', with ' + str(num_oto) + ' oto orders ..................'
		if num_oto == 0:
			continue
		num_dtask = len(ls_osite[i].ls_dtask)
		if num_dtask == 0:
			print 'NO dtasks!!!!!!!!!!'
			continue
		for j in range(0,num_oto):
			print 'The ' + str(j) + ' th oto of site ' + str(i) + '....'
			mindist = 10000000
			bsf = -1
			bspos = -1
			for k in range(0,num_dtask):
				[tempdis,posinsrt] = DistubOTODTask(ls_osite[i].ls_oto[j],ls_osite[i].ls_dtask[k],ls_site,ls_spot,ls_shop)
				# print ls_osite[i].ls_dtask[k]
				# print ls_osite[i].ls_oto[j][0].shopid,ls_osite[i].ls_oto[j][0].spotid
				# print tempdis,posinsrt
				# break
				if tempdis < mindist:
					if tempdis > 0:
						bsf = copy(k)
						tempdis = copy(mindist)
						bspos = copy(posinsrt)
			if bsf >= 0:
				templs = deepcopy(ls_osite[i].ls_dtask[bsf])
				# print ls_osite[i].ls_oto[j][1], 'pos to insert ', posinsrt
				ls_osite[i].ls_dtask[bsf] = {}
				ls_osite[i].ls_dtask[bsf] = InsertOTODTask(ls_osite[i].ls_oto[j],bspos,templs,ls_site,ls_spot,ls_shop)
				# print ls_osite[i].ls_dtask[bsf][0][0]
				if 'S' in ls_osite[i].ls_dtask[bsf]["task"][0][0]:
					print bspos
					print ls_osite[i].ls_dtask[bsf]["task"][0][0]
				# print templs
				# print ls_osite[i].ls_dtask[bsf]
				# print ls_osite[i].ls_oto[j][1]
			# break
		# break
		templs = deepcopy(ls_osite[i].ls_oto)
		ls_osite[i].ls_oto = []
		ls_osite[i].ls_oto = [x for x in templs if x[1] == 0]



		count_oto_notassigned = copy(count_oto_notassigned) + len(ls_osite[i].ls_oto)
		print str(count_oto_notassigned) + ' orders not assigned !!!!!!'
		f = open('../results/' + ls_osite[i].sid + '.csv','w')
		writer = csv.writer(f)
		for j in range(0,len(ls_osite[i].ls_dtask)):
			writer.writerow(ls_osite[i].ls_dtask[j]["task"])
		# writer.writerows(ls_osite[i].ls_dtask["task"])
		f.close()
	print 'currently, there are still ' + str(count_oto_notassigned) + ' oto orders waiting to be assigned'

	# while(len(ls_asgn_odr) < num_order):
	# 	[isfound,order,task] = FindBestMatch(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoodr_sort,ls_asgn_dtsk,ls_asgn_odr)
	# 	break
	# 	if isfound:
	# 		fulltask = ExpandTask(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoodr_sort,ls_asgn_dtsk,ls_asgn_odr)
	# 		ls_fulltask.append(copy(fulltask))
	# 	else:
	# 		ls_pure_oto = AssignPureOTO(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoodr_sort,ls_asgn_dtsk,ls_asgn_odr)


	return [ls_fulltask,ls_pure_oto]

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
		new_res_raw = []
		new_res_raw = RmCross(res_raw,o_graph)
		# print res
		tcost1 = ComputeTimeTbl([res_raw],ls_site,ls_spot,ls_shop)
		tcost2 = ComputeTimeTbl([res],ls_site,ls_spot,ls_shop)
		# tcost3 = copy(tcost1) + copy(tcost2)
		tcost3 = ComputeTimeTbl([new_res],ls_site,ls_spot,ls_shop)
		tcost4 = ComputeTimeTbl([new_res_raw],ls_site,ls_spot,ls_shop)
		if tcost3[0]['cost'] == min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost'],tcost4[0]['cost']]):
			ls_res.append(copy(new_res))
			# if 'B3681' in o_graph.nodes():
			# 	print 'new_res win',new_res,min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost']])
			# 	print res,tcost2[0]['cost']
		elif tcost4[0]['cost'] == min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost'],tcost4[0]['cost']]):
			ls_res.append(copy(new_res_raw))
		elif tcost2[0]['cost'] == min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost'],tcost4[0]['cost']]):
			ls_res.append(copy(res))
			# if 'B2350' in o_graph.nodes():
			# 	print 'res win', res,min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost']])
			# if res != new_res:
			# 	print res
			# 	print new_res
			# 	print 'tcost2 is ', tcost2[0]['cost'], ' tcost3 is ', tcost3[0]['cost']
			# 	temp_dis = DistSum(res,ls_site,ls_spot,ls_shop)
			# 	print 'total dist of res is ', temp_dis
			# 	temp_dis = DistSum(new_res,ls_site,ls_spot,ls_shop)
			# 	print 'total dist of new_res is ', temp_dis

		elif tcost1[0]['cost'] == min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost'],tcost4[0]['cost']]):
			ls_res.append(copy(res_raw))
			# if 'B3681' in o_graph.nodes():
			# 	print 'res_raw win', res_raw,min([tcost1[0]['cost'],tcost2[0]['cost'],tcost3[0]['cost']])
		# if 'B3681' in o_graph.nodes():
		# 	print '***********************'
		# 	print res, tcost2[0]['cost']
		# 	print new_res, tcost3[0]['cost']
		# 	print res_raw, tcost1[0]['cost']
		# 	print '***********************'
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

def ComputeOTODDL(ls_otoorder,ls_site,ls_spot,ls_shop):
	num_order = len(ls_otoorder)
	for i in range(0,num_order):
		order = copy(ls_otoorder[i])
		loc1 = GetLoc(order.shopid,ls_site,ls_spot,ls_shop)
		loc2 = GetLoc(order.spotid,ls_site,ls_spot,ls_shop)
		trvlt = TravelTime(loc1,loc2)
		ls_otoorder[i].ddl = copy(ls_otoorder[i].dtime) - copy(trvlt)
		if ls_otoorder[i].ddl < ls_otoorder[i].ptime:
			# print 'ddl should have been ', ls_otoorder[i].ddl
			ls_otoorder[i].ddl = copy(ls_otoorder[i].ptime)
			# print ls_otoorder[i].oid, ls_otoorder[i].ptime,ls_otoorder[i].dtime,ls_otoorder[i].ddl
	return

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

def ComputeTripCost(trip,ls_site,ls_spot,ls_shop,*arg):
	prev = 0
	prev = GetLoc(copy(trip[0][0]),ls_site,ls_spot,ls_shop)
	table = {}
	table['trip'] = copy(trip)
	cost = 0
	length = len(trip)
	i = 1
	isbreak = 0
	if len(arg) > 0:
		isbreak = arg[0]
	for step in trip:
		locid = copy(step[0])
		bag = copy(step[1])
		loc = 0
		loc = GetLoc(locid,ls_site,ls_spot,ls_shop)
		# print step
		t_travel = TravelTime(prev,loc)
		if 'S' in locid:
			t_proc = 0
		else:
			t_proc = ProcTime(bag)
		if bag == 0:
			t_proc = 0
		# print prev.sid,locid,bag
		prev = 0
		prev = GetLoc(locid,ls_site,ls_spot,ls_shop)
		# print 'travel time: ', t_travel, 'process time: ',t_proc
		cost = copy(cost) + copy(t_travel) + copy(t_proc)
		i = copy(i) + 1
		if i > length - isbreak:
			break
	table['cost'] = copy(cost)
	return cost

def ComputeTripVol(trip):
	volume = 0
	for step in trip:
		volume = copy(volume) + copy(int(step[1]))
	return volume

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

def DistSum(path,ls_site,ls_spot,ls_shop):
	dist = 0.0
	sumt = 0
	for i in range(0,len(path)-1):
		loc1 = 0
		loc2 = 0
		loc1 = GetLoc(path[i][0],ls_site,ls_spot,ls_shop)
		loc2 = GetLoc(path[i+1][0],ls_site,ls_spot,ls_shop)
		temp_dis = Dist(loc1,loc2)
		t = Round(temp_dis/0.25)
		print 'dist of this step is ' + str(temp_dis) + ' , round t is ' + str(t)
		sumt = copy(sumt) + copy(t)
		dist = copy(dist) + copy(temp_dis)
	print 'sumt is ' +str(sumt)
	return dist

def DistByName(nm1,nm2,ls_site,ls_spot,ls_shop):
	dist = 0
	loc1 = GetLoc(nm1,ls_site,ls_spot,ls_shop)
	loc2 = GetLoc(nm2,ls_site,ls_spot,ls_shop)
	dist = Dist(loc1,loc2)
	return dist

def DistubOTODTask(otoodr,dtask,ls_site,ls_spot,ls_shop):
	distb = 100000000
	bsf = -1
	temp_distb = 0
	origt = ComputeTripCost(dtask["task"],ls_site,ls_spot,ls_shop)
	newt = 0
	templs = {}
	length = len(dtask["task"]) - 1
	for i in range(1,length):
		templs = {"starttime":copy(dtask["starttime"]),"task":[],"hasoto":dtask["hasoto"]}
		if 'S' in dtask["task"][i][0]:
			continue
		tempid = copy(i) + 1
		# print tempid
		for j in range(0,tempid):
			templs["task"].append(copy(dtask["task"][j]))
		templs["task"].append([copy(otoodr[0].shopid),str(copy(otoodr[0].num)),copy(otoodr[0].ptime),copy(otoodr[0].ddl)])
		templs["task"].append([copy(otoodr[0].spotid),str(-copy(otoodr[0].num)),copy(otoodr[0].dtime)])
		totalv = int(copy(otoodr[0].num))
		for j in range(tempid,len(dtask["task"])):
			templs["task"].append(dtask["task"][j])
			totalv = copy(totalv) + int(dtask["task"][j][1])
			if totalv > 140:
				# print 'cannot accomodate, too much'
				continue
		# print dtask
		# print templs
		[sintvl,eintvl,hasoto] = FindSEIntvl(templs,ls_site,ls_spot,ls_shop)
		# print [sintvl,eintvl,hasoto]
		if eintvl < 0:
			# print 'too late...'
			continue
		# if sintvl <= 0:
		# 	newt = ComputeTripCost(templs["task"],ls_site,ls_spot,ls_shop)
		# else:
		newt = ComputeTripCost(templs["task"],ls_site,ls_spot,ls_shop) + copy(sintvl)
		temp_distb = copy(newt) - copy(origt)
		if temp_distb < distb:
			distb = copy(temp_distb)
			bsf = copy(i)
		# break
		# if hasoto == 0:
		# 	while(1):
		# 		print 'oto not found!!!!!!!!!!!!'
	if bsf < 0:
		# print 'cannot insert, maybe too large....'
		return [-1,-1]
	if distb > origt + TravelTimeByName(otoodr[0].shopid,otoodr[0].spotid,ls_site,ls_spot,ls_shop):
		# print 'this oto odr starts too late or too far ....'
		return [-1,-1]
	return [distb,bsf]

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

def FindBestMatch(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoodr_sort,ls_asgn_dtsk,ls_asgn_odr):
	isfound = 0
	tarorder = 0
	tartask = 0
	num_order = len(ls_otoodr_sort)
	num_site = len(ls_dtask)
	for i in range(0,num_site):
		num_dtask = len(ls_dtask[i])
		# for j in range(0,num_dtask):
		# 	print ls_dtask[i][j]

		break
	# for i in range(0,num_order):
	# 	if i in ls_asgn_odr:
	# 		continue
	# 	order = copy(ls_otoodr_sort[i])
	# 	sloc = GetLoc(order.shopid,ls_site,ls_spot,ls_shop)


	return [isfound,tarorder,tartask]

def FindDTasks(ls_site,ls_spot,ls_shop,istart,iend,ls_dorder,CAPACITY):
	total_worker = 0
	cost = 0
	ls_dtask = []
	for i in range(0,len(ls_site)):
		if i < istart:
			continue
		if i >= iend:
			break
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
		ls_dtask.append(copy(ls_res))
		total_worker = copy(total_worker) + len(ls_res)
		cost = copy(cost) + min_cost
	return ls_dtask

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

def FindSEIntvl(dtask,ls_site,ls_spot,ls_shop):
	length = len(dtask["task"])
	hasoto = 0
	ls_oto_pos = []
	for i in range(0,length):
		if len(dtask["task"][i]) == 4:
			hasoto = 1
			ls_oto_pos.append(copy(i))
	if hasoto == 0:
		return [-1, -1, 0]
	ls_s_e = []
	latest = 100000000
	earliest = -10000000
	for pos in ls_oto_pos:
		step_count = copy(length) - copy(pos) - 1
		# idbf = copy(pos) - 1
		tbfr = ComputeTripCost(dtask["task"],ls_site,ls_spot,ls_shop,step_count)
		template = copy(dtask["task"][pos][3]) - copy(tbfr)
		tempearly = copy(dtask["task"][pos][2]) - copy(tbfr)
		if template < latest:
			latest = copy(template)
		if tempearly > earliest:
			earliest = copy(tempearly)
		if earliest > latest:
			return [-1, -1 , 1]
	if latest < dtask["starttime"]:
		return [-1, -1, 1]
	if earliest < dtask["starttime"]:
		earliest = copy(dtask["starttime"])
		# ls_s_e.append([copy(dtask[pos][2]) - copy(tbfr), copy(dtask[pos][3]) - copy(tbfr)])
	return [earliest, latest, 1]

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

def GroupTasks(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoorder):
	num_site = len(ls_dtask)
	num_oto = len(ls_otoorder)
	osite = 0
	ls_osite = []
	for i in range(0,num_site):
		osite = 0
		num_dtask = len(ls_dtask[i])
		[lng, lat] = GetLngLat(ls_dtask[i][0][0][0],ls_site,ls_spot,ls_shop)
		osite = 0
		osite = TaskPersite(ls_dtask[i][0][0][0],lng,lat)
		for j in range(0,num_dtask):
			osite.ls_dtask.append({"starttime":0,"task":copy(ls_dtask[i][j]),"hasoto":0})
		ls_osite.append(copy(osite))
	for i in range(0,num_oto):
		s_loc = GetLoc(copy(ls_otoorder[i].shopid),ls_site,ls_spot,ls_shop)
		mindist = 10000000
		id_bsf = -1
		for j in range(0,num_site):
			temp_dis = Dist(s_loc,ls_osite[j])
			if temp_dis < mindist:
				mindist = copy(temp_dis)
				id_bsf = copy(j)
		ls_osite[id_bsf].ls_oto.append([copy(ls_otoorder[i]),0])
	return ls_osite

def InsertOTODTask(otoodr,posinsrt,dtask,ls_site,ls_spot,ls_shop):
	templs = {}
	templs = deepcopy(dtask)
	tempid = copy(posinsrt) + 1
	dtask = {"starttime":0,"task":[],"hasoto":1}
	for i in range(0,tempid):
		dtask["task"].append(deepcopy(templs["task"][i]))
	dtask["task"].append([copy(otoodr[0].shopid),str(copy(otoodr[0].num)),copy(otoodr[0].ptime),copy(otoodr[0].ddl)])
	dtask["task"].append([copy(otoodr[0].spotid),str(-copy(otoodr[0].num)),copy(otoodr[0].dtime)])
	for i in range(tempid,len(templs["task"])):
		dtask["task"].append(deepcopy(templs["task"][i]))
	otoodr[1] = 1
	return dtask

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
	# print x
	if float(x) < 0:
		return Round(copy(3.0 * sqrt(-float(x)) + 5.0))
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
	if 'B' in o_graph.nodes():
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
	ischange = 0
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
						# print 'Find intersection!!!!!!!!'
						ischange = 1
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
	if ischange == 0:
		return res
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

def TravelTimeByName(nm1,nm2,ls_site,ls_spot,ls_shop):
	#return in minutes with rounding finished
	t = 0
	dist = DistByName(nm1,nm2,ls_site,ls_spot,ls_shop)
	t = dist / speed
	t = Round(copy(t))
	return t

