# Resource Search Project CS 581 DBMS
# Task 1: Uninformed search with connection to MySQL database
# Date : April 4, 2016

import csv
import math
import json
import urllib.request
import mysql.connector
import datetime
import calendar

THRESHOLD = 100

class Point:
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long

    def __str__(self):
        return str(self.__dict__)
        
    def distanceEuclid(self,second):
        return math.sqrt((self.lat - second.lat) ** 2 + (self.long - second.long) ** 2)
    
    # Returns the distance between two points in meters, and time in seconds
    # append &units=imperial at the end of URL for solution in miles/feet
    def distanceFromAPI(self,second):
        originPt = str(self.lat) + "," + str(self.long)
        destPt = str(second.lat) + "," + str(second.long)
        
        key = ['AIzaSyDYn3jW7mEep-FEfN5jsKk8J93opDyFQc8', 
               'AIzaSyCad2_4JDRhH82KbFmd9yrsk1D3U3y4iYQ',
               'AIzaSyBI770fgXAr1C-AZPGLsJmqCeamuG60qbU',
               'AIzaSyC01WWuwA5YMJR_ydjCkOViuThqlAp3foU', 
               'AIzaSyDawxuEyXabWq_3zlGyjXl2c_ZtuV88ugI',
               'AIzaSyA5RKX_oKvoO6hg8_dsaJFq026YE1H3fTY',
               'AIzaSyDM4lJyl6lLGL1DnhBAX6aAbTybXd11CfA']
        
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking&origins="+ originPt + "&destinations="+ destPt + "&key=" + key[6]
        
        response = urllib.request.urlopen(url)
        responseData = response.read().decode('utf-8')
        jsonObj = json.loads(responseData)
        if jsonObj['status'] == 'OK':
            return (jsonObj['rows'][0]['elements'][0]['distance']['value'],jsonObj['rows'][0]['elements'][0]['duration']['value'])
        else:
            return None,None # throw exception
    
    # class method to extract the precomputed distances between nodes and parking blocks and between parking blocks
    # second parameter is taken as block_id
    def distanceFromDBDrive(self,secondBlockID):
        originPt = str(self.lat) + "," + str(self.long)
        #destPt = str(second.lat) + "," + str(second.long)

        query = ("SELECT distance,time FROM parkingproject.precomputeMatrix WHERE source_lat = %s and source_long = %s and end_block = %s;")
        
        cnx = connectToMySQL()
        cursor = cnx.cursor()
        cursor.execute(query,(self.lat,self.long,secondBlockID))
        #print(second.lat,second.long)
        for d,t in cursor:
            distance = d
            time = t

        return distance,time

    # source lat and source long will always be the start point where the request was submitted
    def distanceFromDBWalk(self,OriginBlockID):
        originPt = str(self.lat) + "," + str(self.long)

        query = ("SELECT distance,time FROM parkingproject.precomputeMatrixWalk WHERE dest_lat = %s and dest_long = %s and block_id = %s;")
        
        cnx = connectToMySQL()
        cursor = cnx.cursor()
        cursor.execute(query,(self.lat,self.long,OriginBlockID))

        for d,t in cursor:
            distance = d
            time = t

        return distance,time

# returns a MySQL connector object
def connectToMySQL(userName='root',password='password',DBName='parkingproject'):
	config = {
	  'user': userName,
	  'password': password,
	  'host': 'localhost',
	  'database': DBName,
	  'raise_on_warnings': True
	}

	return mysql.connector.connect(**config)

def closeConnection(cnxObj):
	if cnxObj.is_connected():
		cnxObj.close()
		return "Success. Connection closed."
	else:
		return "Failed. Connection is not open."

# Get all parking block id's to a list for easy access
def getParkingDataUninform():
	cnx = connectToMySQL()
	cursor = cnx.cursor()

	query = ("SELECT block_id,latitude,longitude,operational FROM parkingproject.edges;")

	cursor.execute(query)

	parkingData = []
	for block_id,lattitude,longitude,operational in cursor:
	    parkingDataDict = {}
	    parkingDataDict['blockID'] = block_id
	    parkingDataDict['midptLat'] = lattitude
	    parkingDataDict['midptLong'] = longitude
	    parkingDataDict['operational'] = operational
	    parkingData.append(parkingDataDict)

	closeConnection(cnx)

	return parkingData

def getParkingDataProbabilistic(daynm,hourDay):
    cnx = connectToMySQL()
    cursor = cnx.cursor()

    query = ("SELECT block_id, avg_avail, dayname, hour_of_day FROM parkingproject.probabilisticData where dayname = %s and hour_of_day = %s;")

    cursor.execute(query,(daynm,hourDay))

    parkingData = []
    for block_id,avg_avail,dayname,hour_of_day in cursor:
        parkingDataDict = {}
        parkingDataDict['blockID'] = block_id
        parkingDataDict['avg_avail'] = avg_avail
        parkingDataDict['dayname'] = dayname
        parkingDataDict['hour_of_day'] = hour_of_day
        parkingData.append(parkingDataDict)

    closeConnection(cnx)

    return parkingData

def getNearestSlot(sourcePt,parkingData):
    distanceArr = []
    for park in parkingData:
        xcord = float(park['midptLat'])
        ycord = float(park['midptLong'])
        parkingPt = Point(xcord,ycord)
        blockID = park['blockID']
        # dist,time = sourcePt.distanceFromAPI(parkingPt)
        dist,time = sourcePt.distanceFromDBDrive(blockID)
        # dist_w,time_w = orignalSource.distanceFromDBWalk(blockID)
        if dist == 0:
            dist = float('inf')
        distanceArr.append((park['blockID'],dist,time))

    distanceArr = sorted(distanceArr,key=lambda tup : tup[1],reverse= False)
    selectedSlot = distanceArr[0]
    #print(distanceArr)
    return(selectedSlot)

# logic for calculating force between source point and every parking slot
# always returns the highest attracting parking block id
def computeForceVector(sourcePt,parkingData,orignalSource,conjestion,probabilistic = False):
    forceVector = []
    #sourcePt = Point(37.8061858,-122.4188171)
    if not probabilistic:
        forceParam = 'operational'
    else:
        forceParam = 'avg_avail'
  
    for park in parkingData:
        # xcord = float(park['midptLat'])
        # ycord = float(park['midptLong'])
        # parkingPt = Point(xcord,ycord)
        blockID = park['blockID']
        # dist,time = sourcePt.distanceFromAPI(parkingPt) # Uncomment this part if you want to make calls to Google API
        dist,time = sourcePt.distanceFromDBDrive(blockID)
        dist_w,time_w = orignalSource.distanceFromDBWalk(blockID)
        if dist != 0:
            numerator = float(park[forceParam])*float(conjestion)
            force = numerator/(time + time_w) ** 2
        else:
            force = float('-inf')
        forceVector.append((park['blockID'],force,time,time_w))
        #break # remove break to execute for all spots

    forceVector = sorted(forceVector,key=lambda tup : tup[1],reverse= True)
    selectedSlot = forceVector[0]
    return(selectedSlot)


def searchSpotDetails(parkingData,blockID,methodName):
    if methodName == 'probabilistic':
        cnx = connectToMySQL()
        cursor = cnx.cursor()

        query = ("SELECT latitude,longitude FROM parkingproject.edges WHERE block_id = %s;") % blockID

        cursor.execute(query)
        
        for latitude,longitude in cursor:
            lat,long = latitude,longitude
        closeConnection(cnx)
        return lat,long
    else:
        for spot in parkingData:
            if spot['blockID'] == blockID:
                return spot['midptLat'],spot['midptLong']

# Valid values for methodName = 'uninformed' or 'probabilistic' or 'baseline' 
# Return values : selected slot ID, total parking time, driving time, walking time, waypoints and number of iterations
def parkingSearch(sourceLat,sourceLong,startTime,conjestion,methodName = "uninformed"):
    found = False
    # current time + time of selectedSlot = parkTime
    cnx = connectToMySQL()
    wayPoints = []
    source = Point(sourceLat,sourceLong)
    orignalSource = Point(sourceLat,sourceLong)
    sourceTime = datetime.datetime.strptime(startTime,"%Y-%m-%d %H:%M:%S")

    if methodName == "uninformed" or methodName == "baseline":
        parkingData = getParkingDataUninform()
    else: # methodName == Probabilistic
        parkingData = getParkingDataProbabilistic(calendar.day_name[sourceTime.weekday()],sourceTime.hour) # two parameters

    if methodName == "uninformed":
        probabilistic = False
    else:
        probabilistic = True

    i = 0
    timeToPark = 0
    while not found:
        if methodName == "baseline":
            selectedSlot = getNearestSlot(source,parkingData)
        else:
            selectedSlot = computeForceVector(source,parkingData,orignalSource,conjestion,probabilistic)
        
        parkTime = sourceTime + datetime.timedelta(seconds = (selectedSlot[2]))
        timeToPark += (selectedSlot[2])
        parkTimeDB = str(parkTime)

        query = ("SELECT available FROM availability WHERE block_id = %s and datetimestamp IN (SELECT max(datetimestamp) FROM availability WHERE block_id = %s and datetimestamp < %s);")

        cursor = cnx.cursor()
        cursor.execute(query,(selectedSlot[0],selectedSlot[0],parkTimeDB))

        for avail in cursor:
            available = avail[0] * conjestion

        if available < 1:
            i += 1
            source = Point(*searchSpotDetails(parkingData,selectedSlot[0],methodName))
            sourceTime = parkTime
            wayPoints.append(source)
            if i > THRESHOLD:
                return (-1,-1,-1,-1,-1,-1)
        else:
            found = True
            closeConnection(cnx)
            # time to walk is only added to the selected slot
            if methodName == "baseline": 
                walkingTime = orignalSource.distanceFromDBWalk(selectedSlot[0])[1]    
            else:
                walkingTime = selectedSlot[3] 

            timeToPark += walkingTime    
            return (selectedSlot[0],timeToPark,(timeToPark-walkingTime),walkingTime,wayPoints,i)


def __main__():
    print(parkingSearch(37.806054,-122.410329,'2012-04-06 00:06:32',1))
    # print(parkingSearch(37.806054,-122.410329,'2012-04-06 00:06:32',1,'probabilistic'))
    # print()
    
    # #Node_id: 7038; (Lat, Long): 37.806054, -122.410329; datetime: 2012-04-06 00:06:32
    print(parkingSearch(37.806054, -122.410329,'2012-04-06 00:06:32',1,'baseline'))
    print(parkingSearch(37.806054, -122.410329,'2012-04-06 00:06:32',1))
    print(parkingSearch(37.806054, -122.410329,'2012-04-06 00:06:32',1,'probabilistic'))
    
    #Node_id: 7029; (Lat, Long): 37.806584, -122.413821; datetime: 2012-05-02 18:56:18
    print(parkingSearch(37.806584, -122.413821,'2012-05-02 18:56:18',1,'baseline'))
    print(parkingSearch(37.806584, -122.413821,'2012-05-02 18:56:18',1))
    print(parkingSearch(37.806584, -122.413821,'2012-05-02 18:56:18',1,'probabilistic'))
    # print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',0.8))
    print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',0.6))
    print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',0.2))
    print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',1,'baseline'))

    

if __name__ == "__main__":
    __main__()
