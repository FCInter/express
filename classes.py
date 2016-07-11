

class Site(object):
	"""docstring for Site"""
	sid = 0
	lat = 0.0
	lng = 0.0
	def __init__(self,sid,lng,lat):
		self.sid = sid
		self.lat = lat
		self.lng = lng

class Spot(object):
	"""docstring for Spot"""
	sid = 0
	lat = 0.0
	lng = 0.0
	def __init__(self,sid,lng,lat):
		self.sid = sid
		self.lat = lat
		self.lng = lng

class Shop(object):
	"""docstring for Shop"""
	sid = 0
	lat = 0.0
	lng = 0.0
	def __init__(self,sid,lng,lat):
		self.sid = sid
		self.lat = lat
		self.lng = lng

class DOrder(object):
	"""docstring for Order"""
	oid = 0
	spotid = 0
	siteid = 0
	num = 0
	def __init__(self, oid,spotid,siteid,num):
		self.oid = oid
		self.spotid = spotid
		self.siteid = siteid
		self.num = num

class OtOOrder(object):
	"""docstring for OtOOrder"""
	oid = 0
	spotid = 0
	shopid = 0
	ptime = 0
	dtime = 0
	num = 0
	def __init__(self, oid,spotid,shopid,ptime,dtime,num):
		self.oid = oid
		self.spotid = spotid
		self.shopid = shopid
		self.ptime = ptime
		self.dtime = dtime
		self.num = num

class Courier(object):
	"""docstring for Courier"""
	cid = 0
	ls_odr = []
	capacity = 140
	volume = 0
	lng = 0
	lat = 0
	def __init__(self, cid):
		self.cid = cid

class GOrder(object):
	"""docstring for StartPoint"""
	oid = 0
	oriid = 0
	destid = 0
	ptime = 0
	dtime = 0
	num = 0
	def __init__(self, oid,oriid,destid,ptime,dtime,num):
		self.oid = oid
		self.oriid = oriid
		self.destid = destid
		self.ptime = ptime
		self.dtime = dtime
		self.num = num

speed = 0.25
str_date = '1970-01-01'

def main():
	print speed
	return

if __name__ == "__main__":
    main()