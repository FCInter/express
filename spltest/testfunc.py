import csv
from copy import copy
import os
import datetime
import time
from datetime import datetime
from classes import *
from tools import *
from os.path import isfile, join

def ExportDTaskToCSV(ls_dtask,ls_site):
    for i in range(0,len(ls_dtask)):
        filepath = ''
        filepath = copy('../results/tempres/' + copy(ls_site[i].sid) + '/')
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        for j in range(0,len(ls_dtask[i])):
            filename = ''
            filename = copy(filepath) + str(j) + '.csv'
            f = open(filename,'a')
            writer = csv.writer(f)
            writer.writerows(ls_dtask[i][j])
            f.close()
    return

def LoadDTaskFmCSV(srcpath,ls_site,ls_spot,ls_shop):
    ls_dtask = []
    ls_sitename = sorted(os.listdir(srcpath))
    num_site = len(ls_sitename)
    for i in range(0,num_site):
        # [lng,lat] = GetLngLat(ls_sitename[i],ls_site,ls_spot,ls_shop)
        ls_this = []
        # osite = TaskPersite(ls_sitename[i],lng,lat)
        # print osite.sid,osite.lng,osite.lat
        mypath = ''
        mypath = srcpath + copy(ls_sitename[i]) + '/'
        onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
        num_file = len(onlyfiles)
        for j in range(0,num_file):
            filename = copy(mypath) + copy(onlyfiles[j])
            # print filename
            f = open(filename,'rb')
            rdr = csv.reader(f)
            ls_this.append(list(rdr))
            # osite.ls_dtask.append(list(rdr))
            f.close()
        # print ls_this
        # print len(ls_this)
        ls_dtask.append(ls_this)
        # print osite.ls_dtask
        # print len(osite.ls_dtask)
        # break

    return ls_dtask

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
        str_ptime = copy(str_date) + 'T' + copy(row[3]) + ':00'
        str_dtime = copy(str_date) + 'T' + copy(row[4]) + ':00'
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



def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y



[ls_site,ls_spot,ls_shop,ls_dorder,ls_otoorder,ls_courier] = LoadAll()

ls_org_oid = []
for i in range(0,len(ls_otoorder)):
    oid = copy(ls_otoorder[i].oid)
    ls_org_oid.append(copy(oid))


for i in range(0,len(ls_dorder)):
    oid = copy(ls_dorder[i].oid)
    ls_org_oid.append(copy(oid))

print len(ls_org_oid)

f = open('../results/test_out.csv','rb')
rdr = csv.reader(f)
table = list(rdr)
f.close()

print len(table)
ls_oid_assigned = []
for step in table:
    oid = copy(step[-1])
    if oid not in ls_oid_assigned:
        ls_oid_assigned.append(copy(oid))
print len(ls_oid_assigned)

ls_oid_missed = []
f = open('../results/missed.csv','a')
writer = csv.writer(f)
for i in range(0,len(ls_org_oid)):
    oid = copy(ls_org_oid[i])
    if oid not in ls_oid_assigned:
        print oid
        writer.writerow([oid])
        ls_oid_missed.append(copy(oid))
f.close()
print len(ls_oid_missed)

