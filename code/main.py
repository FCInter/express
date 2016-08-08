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
	ls_dtask = []
	istart = 0
	iend = 1
	# ls_dtask = FindDTasks(ls_site,ls_spot,ls_shop,istart,iend,ls_dorder,CAPACITY)
	# print 'total_worker is ',total_worker
	# print 'total cost is ', cost
	# print 'ls_dtask is ', ls_dtask
	# ExportDTaskToCSV(ls_dtask,ls_site)
	ls_dtask = []
	ls_dtask = LoadDTaskFmCSV('../results/tempres/',ls_site,ls_spot,ls_shop)
	# f = open('../results/tempres/dtasks.csv','a')
	# writer = csv.writer(f)
	# writer.writerows(ls_dtask)
	# f.close()
	# f = open('../results/tempres/dtasks.csv','rb')
	# rdr = csv.reader(f)
	# ls_dtask = []
	# ls_dtask = list(rdr)
	# f.close()
	print 'after reading csv.....'
	print 'number of sites is ',len(ls_dtask)
	print 'number of oto orders is ',len(ls_otoorder)
	[ls_fulltask,ls_pureoto] = AssignOTO(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoorder,ls_courier)
	AddOrderId(ls_courier,ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder)
	ExportAsResult(ls_courier,ls_site,ls_spot,ls_shop)



	# AssignSender(ls_site,ls_spot,ls_shop,ls_fulltask,ls_pureoto)
	# print 'ls_dtask is ', len(ls_dtask[1])
	# for i in range(0,len(ls_dtask[1])):
	# 	print ls_dtask[1][i]
		# break
	# PlotSpotPerSite(ls_site,ls_spot,ls_dorder)
	# print len(ls_site)
	return

if __name__ == "__main__":
    main()