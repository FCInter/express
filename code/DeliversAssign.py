from xml.dom import minidom
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
CAPACITY = 140
[ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier] = LoadAll()
num_dorder = len(ls_dorder)
total_worker = 0
cost = 0
istart = 32
iend = 33

def loadTime(demand):
    return 3*sqrt(demand)+5
[ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier] = LoadAll()
num_dorder = len(ls_dorder)
total_worker = 0
cost = 0
ls_dtask = []
istart = 0
iend = 300
# ls_dtask = FindDTasks(ls_site,ls_spot,ls_shop,istart,iend,ls_dorder,CAPACITY)
# print 'total_worker is ',total_worker
# print 'total cost is ', cost
# print 'ls_dtask is ', ls_dtask
# ExportDTaskToCSV(ls_dtask,ls_site)
ls_dtask = []
ls_dtask = LoadDTaskFmCSV('../results/tempres/',ls_site,ls_spot,ls_shop)
ls_oSite = GroupTasks(ls_site,ls_spot,ls_shop,ls_dtask,ls_otoorder)

spotDic = {site.sid : (site.lat , site .lng) for site in ls_spot}
shopDic = {shop.sid : (shop.lat, shop.lng) for shop in ls_shop}
siteDic = {Site.sid : (Site.lat, Site.lng) for Site in ls_site}
EOrderDic = {order.oid : order  for order in ls_otoorder}
deliverId = 0
for site in ls_site:
    [ls_spot_per_site,temp_order] = FindSpotPerSite(site,ls_spot,ls_dorder)
    doc = minidom.parse("../jsprit-solver/output/solution"+site.sid+"_problem.xml")
    solutions = doc.getElementsByTagName("solution")
    solution = solutions[0]
    routes = solution.getElementsByTagName('route')
    ls_routes = []
    Route4Site =[]
    for i in range(0,len(routes)): 
        route = routes[i]
        acts = route.getElementsByTagName("act")
        Route4Site =[]
        for act in acts :
            
            Dtype = str(act.getAttribute('type'))
            arrTime = float(act.getElementsByTagName('arrTime')[0].firstChild.data)
            endTime = float(act.getElementsByTagName('endTime')[0].firstChild.data)
            routeNum = i
            if Dtype =='service':
                SpotId = act.getElementsByTagName('serviceId')[0].firstChild.data
                actDic = {'type':Dtype, 'Spotid':str(SpotId), \
                          'arrTime':arrTime, 'endTime':endTime}
                #print SpotId
            else :
                SpotId = act.getElementsByTagName('shipmentId')[0].firstChild.data
                actDic = {'type':Dtype, 'Spotid':str(SpotId), 'arrTime':arrTime, 'endTime':endTime}
            actDic.update({'routeNum':routeNum})
            Route4Site.append(actDic)
        ls_routes.append(Route4Site)
    PureRoutes = []
    RoutesWithO2O = []

    rtNum = []
    rtWithO2ONum = []
    for j in range(0,len(ls_routes)):
        rout = ls_routes[j]
        is_containO2O = 0
        for i in range(0,len(rout)):
            act= rout[i]
            if act['type'] != 'service':
                is_containO2O = 1
        if is_containO2O == 1:
            rtWithO2ONum.append(j)
        else:
            rtNum.append(j)

    #calculate the total time of pure dvelivery route cost
    pureRouteCost = []
    for i in rtNum:
        route = ls_routes[i]
        startPosition = siteDic[site.sid]
        time = 0
        for act in route:
            endPosition =  spotDic[act['Spotid']]
            demand =   temp_order[act['Spotid']]
            distance = Dist(Spot('from',startPosition[0],startPosition[1]),\
                           Spot('to',endPosition[0],startPosition[1]))
            time = time + distance / 0.25 + loadTime(demand)
          #  if abs(time - float(act['endTime'])) > 1 :
           #                     print(abs(time - float(act['endTime'])))
            startPosition = endPosition
        endPosition = siteDic[site.sid]
        distance = Dist(Spot('from',startPosition[0],startPosition[1]),\
                           Spot('to',endPosition[0],startPosition[1]))
        time = time + distance / 0.25
        pureRouteCost.append(time)

    #calculate the last start time of route with o2o and end time 
    rtWithOStart =[]
    rtWithOEnd = []

    for i in rtWithO2ONum:
        route = ls_routes[i]
        time = 0 
        endTime
        for i in range(0,len(route)):
            act = route[i]
            if act['type'] != 'service':
                break;
        Eorder = EOrderDic[act['Spotid']]
        time = Eorder.ptime
        endTime = time
        startPosition = shopDic[Eorder.shopid]
        for j in range(1,i+1):
            act = route[i-j]
            endPosition =  spotDic[act['Spotid']]
            demand =   temp_order[act['Spotid']]
            distance = Dist(Spot('from',startPosition[0],startPosition[1]),\
                           Spot('to',endPosition[0],startPosition[1]))
            time = time - distance / 0.25 - loadTime(demand)  
            startPosition = endPosition
        rtWithOStart.append(time)
        startPosition = shopDic[Eorder.shopid]
        for k in range(i+1,len(route)):
            act = route[k]
            if act['type'] == 'shipment':
                Eorder = EOrderDic[act['Spotid']]
                endTime = Eorder.ptime
            else:

                if act['type']== 'service':
                    endPosition =  spotDic[act['Spotid']]
                    demand =   temp_order[act['Spotid']]
                else:
                    Eorder = EOrderDic[act['Spotid']]
                    endPosition = spotDic[Eorder.spotid]
                    demand = Eorder.num
            distance = Dist(Spot('from',startPosition[0],startPosition[1]),\
                           Spot('to',endPosition[0],startPosition[1]))
            endTime = endTime + distance / 0.25 + loadTime(demand)  
            startPosition = endPosition
        endPosition = siteDic[site.sid]
        distance = Dist(Spot('from',startPosition[0],startPosition[1]),\
                           Spot('to',endPosition[0],startPosition[1]))
        endTime = endTime + distance / 0.25
        rtWithOEnd.append(endTime)
        

    rtflag =[1]*len(rtNum)
    rtOflag = [1]*len(rtWithO2ONum)
    DendTime = 720
    sortedOStart = sorted(range(len(rtWithO2ONum)), key =lambda k :rtWithOStart[k],\
                         reverse =True)
    sortedOEnd = sorted(range(len(rtWithO2ONum)), key =lambda k :rtWithOEnd[k],\
                        reverse = True)
    sortedPureCost = sorted(range(len(pureRouteCost)), key =lambda k :pureRouteCost[k],\
                        reverse = True)
    lastOrouteT=0
    deliversRouteNum = []
    deliveryEndTime=720
    while( sum(rtflag)!=0 or sum(rtOflag) != 0 ):
    #while(deliverId <3):
        routeNum=[]
        #find the last start oRoute
        lastOrouteT = 0
        Dstart =0
        Dend = 0
        if sum(rtOflag)!=0:
            for i in sortedOStart:
                    if rtOflag[i] ==1 :
                        Dstart = rtWithOStart[i]
                        Dend   =  rtWithOEnd[i] 
                        rtOflag[i]=0
                        routeNum.append({'Num':rtWithO2ONum[i],'startT':Dstart,\
                                         'endT':rtWithOEnd[i]})
                        break

            #add  oRoute (if exit) start before 
            if sum(rtOflag)!=0:
                for i in sortedOEnd:
                        if rtOflag[i] ==1 and  rtWithOEnd[i] < Dstart:
                            rtOflag[i]=0
                            #print(rtWithO2ONum[i])
                            Dstart = rtWithOStart[i]
                            routeNum.append({'Num':rtWithO2ONum[i],'startT':Dstart,\
                                                  'endT':rtWithOEnd[i]})




        if sum(rtflag) != 0:
            if routeNum != [] :
                for i in sortedPureCost:
                    if rtflag[i] == 1 and pureRouteCost[i] < Dstart:
                        Dstart = Dstart - pureRouteCost[i]
                        routeNum.append({'Num':rtNum[i],'startT':Dstart,\
                                                      'endT':Dstart+ pureRouteCost[i]})
                        rtflag[i] = 0
            else:
                for i in sortedPureCost:
                    if rtflag[i] == 1 and pureRouteCost[i]+Dend < deliveryEndTime:
                        Dstart = Dend
                        Dend = Dend + pureRouteCost[i]
                        routeNum.append({'Num':rtNum[i],'startT':Dstart,\
                                                      'endT':Dend})
                        rtflag[i] = 0
        deliversRouteNum.append(routeNum)
        deliverId = deliverId + 1
        print(+deliverId)
     #generate results here            
        
        