from xml.dom import minidom
doc = minidom.Document()
doc.toprettyxml(encoding='utf-8')
problem = doc.createElement('problem')
problem.setAttribute('xmlns','http://www.w3schools.com')
problem.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
problem.setAttribute('xsi:schemaLocation','http://www.w3schools.com vrp_xml_schema.xsd')
doc.appendChild(problem)
problemType = doc.createElement('problemType')
problem.appendChild(problemType)
fleetSize = doc.createElement('fleetSize')
fleetSize.appendChild(doc.createTextNode("INFINITE"))
problemType.appendChild(fleetSize)
fleetComposition = doc.createElement('fleetComposition')
fleetComposition.appendChild(doc.createTextNode('HOMOGENEOUS'))
problemType.appendChild(fleetComposition)

vehicles = doc.createElement('vehicles')
problem.appendChild(vehicles)

vehicle = doc.createElement('vehicle')
vehicles.appendChild(vehicle)

v_id = doc.createElement('id')
vehicle.appendChild(v_id)
v_id.appendChild(doc.createTextNode('Site'))

v_typeId = doc.createElement('typeId')
vehicle.appendChild(v_typeId)
v_typeId.appendChild(doc.createTextNode("v8"))

vLocation = doc.createElement('startLocation')
vehicle.appendChild(vLocation)
vlID = doc.createElement('id')
vLocation.appendChild(vlID)
vlID.appendChild(doc.createTextNode('Site'))
vCoord = doc.createElement('coord')
vLocation.appendChild(vCoord)
vCoord.setAttribute('x','0')
vCoord.setAttribute('y','0')

vtimeSchedule = doc.createElement('timeSchedule')
vehicle.appendChild(vtimeSchedule)
vStartT = doc.createElement('start')
vStartT.appendChild(doc.createTextNode('0.0'))
vEndT = doc.createElement('end')
vEndT.appendChild(doc.createTextNode('9999.00'))
vtimeSchedule.appendChild(vStartT)
vtimeSchedule.appendChild(vEndT)

vReturn2Site = doc.createElement('returnToDepot')
vehicle.appendChild(vReturn2Site)
vReturn2Site.appendChild(doc.createTextNode('true'))

vehicleTypes = doc.createElement('vehicleTypes')
problem.appendChild(vehicleTypes)
vType = doc.createElement('type')
vehicleTypes.appendChild(vType)
vTypeId = doc.createElement('type')
vType.appendChild(vTypeId)
vTypeId.appendChild(doc.createTextNode('v8'))
vCapacity = doc.createElement('capacity')
vType.appendChild(vCapacity)
vCapacity.appendChild(doc.createTextNode('140'))
vCosts = doc.createElement('costs')
vType.appendChild(vCosts)
vCFixed = doc.createElement('fixed')
vCosts.appendChild(vCFixed)
vCFixed.appendChild(doc.createTextNode('0.0'))
vCdistance = doc.createElement('distance')
vCosts.appendChild(vCdistance)
vCdistance.appendChild(doc.createTextNode('1.0'))
vCTime = doc.createElement('time')
vCosts.appendChild(vCTime)
vCTime.appendChild(doc.createTextNode('0.0'))

services = doc.createElement('services')
problem.appendChild(services)

def addService(services,newOrder):
    
    newService = doc.createElement('service')
    newService.setAttribute('id',newOrder['orderID'])
    newService.setAttribute('type','service')
    services.appendChild(newService)
    
    sLocationId = doc.createElement('locationId')
    newService.appendChild(sLocationId)
    sLocationId.appendChild(doc.createTextNode(newOrder['SId']))
    
    coord = doc.createElement('coord')
    newService.appendChild(coord)
    coord.setAttribute('x',newOrder['lat'])
    coord.setAttribute('y',newOrder['lng'])
    demand = doc.createElement('capacity-demand')
    newService.appendChild(demand)
    demand.appendChild(doc.createTextNode(newOrder['demand']))
    
    duration = doc.createElement('duration')
    newService.appendChild(duration)
    duration.appendChild(doc.createTextNode(newOrder['duration']))
    
    timeWs = doc.createElement('timeWindows')
    newService.appendChild(timeWs)
    timeWindow = doc.createElement('timeWindow')
    newService.appendChild(timeWindow)
    start = doc.createElement('start')
    timeWindow.appendChild(start)
    start.appendChild(doc.createTextNode(newOrder['start']))
    end = doc.createElement('end')
    timeWindow.appendChild(end)
    end.appendChild(doc.createTextNode(newOrder['end']))

addService(services,{"orderID":"sb01","SId":"B555","lat":"25","lng":"15",\
            "demand":"100","duration":"1","start":"0.0","end":"9999"})
#addService(services,{"orderID":"sb02","SId":"B556","lat":"20","lng":"15",\
#            "demand":"80","duration":"1","start":"0.0","end":"9999"})
#addService(services,{"orderID":"sb03","SId":"B557","lat":"-5","lng":"10",\
#            "demand":"60","duration":"1","start":"0.0","end":"9999"})
#addService(services,{"orderID":"sb01","SId":"B555","lat":"25","lng":"-15",\
#           "demand":"130","duration":"1","start":"0.0","end":"9999"})

o2oOrders =  doc.createElement('shpments')
problem.appendChild(o2oOrders)

def addO2OService(o2oOrders, newO2OService):
    newOrder = doc.createElement('shipment')
    o2oOrders.appendChild(newOrder)
    newOrder.setAttribute('id',newO2OService['orderID'])
    
    pickUp = doc.createElement('pickup')
    newOrder.appendChild(pickUp)
    pCoord =doc.createElement('coord')
    pickUp.appendChild(pCoord)
    pCoord.setAttribute('x',newO2OService['plat'])
    pCoord.setAttribute('y',newO2OService['plng'])
    
    pTimeWds = doc.createElement('timeWindows')
    pickUp.appendChild(pTimeWds)
    pTW = doc.createElement('timeWindow')
    pTimeWds.appendChild(pTW)
    
    pStart = doc.createElement('start')
    pStart.appendChild(doc.createTextNode(newO2OService['pStart']))
    pEnd = doc.createElement('end')
    pEnd.appendChild(doc.createTextNode(newO2OService['pEnd']))
    pTW.appendChild(pStart)
    pTW.appendChild(pEnd)
    
    delivery = doc.createElement('delivery')
    newOrder.appendChild(delivery)
    dCoord =doc.createElement('coord')
    delivery.appendChild(dCoord)
    dCoord.setAttribute('x',newO2OService['dlat'])
    dCoord.setAttribute('y',newO2OService['dlng'])
    
    dTimeWds = doc.createElement('timeWindows')
    delivery.appendChild(dTimeWds)
    dTW = doc.createElement('timeWindow')
    dTimeWds.appendChild(dTW)
    
    dStart = doc.createElement('start')
    dStart.appendChild(doc.createTextNode(newO2OService['dStart']))
    dEnd = doc.createElement('end')
    dEnd.appendChild(doc.createTextNode(newO2OService['dEnd']))
    dTW.appendChild(dStart)
    dTW.appendChild(dEnd)
    
    capacity_dimentions = doc.createElement('capacity-dimensions')
    newOrder.appendChild(capacity_dimentions)
    dimention = doc.createElement('dimention')
    capacity_dimentions.appendChild(dimention)
    dimention.setAttribute('index','0')
    dimention.appendChild(doc.createTextNode(newO2OService['capacity']))
       
    
addO2OService(o2oOrders,{"orderID":"o2o0001","plat":"10","plng":"-9","pStart":"100","pEnd":"150",\
                        "dlat":"-8","dlng":"15","dStart":"230","dEnd":"240","capacity":"10"})

fXML = file("/home/xfz/sandBox/exp/input/test.xml","wb")
doc.writexml(fXML,'/t','/t','/n',"utf-8")
fXML.close()
print("all done")

doc.toprettyxml()


