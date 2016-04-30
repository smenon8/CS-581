import UninformedSearchWithDB as UDB
import importlib
import csv
importlib.reload(UDB)


def gatherData(methName,conjestion,outFile):
   
    cnx = UDB.connectToMySQL()
    cursor = cnx.cursor()

    #Create a list of date timestamps [Should be 4, verify with rajan and sreejith]
    datetimestampList = ['2012-04-11 17:30:00','2012-04-06 12:40:00'] # ,'2012-04-06 21:45:00','2012-04-06 09:45:00']

    # datetimestampList = ['2012-04-06 00:06:32', '2012-05-02 18:56:18','2012-04-07 13:21:35','2012-04-08 16:39:34',
                        #'2012-04-18 16:49:42','2012-04-09 9:28:31','2012-04-10 9:28:31','2012-04-13 22:40:53']

    wrtFLcontents = []
    for datetimestamp in datetimestampList:

        query = ("SELECT DISTINCT node_id,latitude,longitude FROM ParkingProject.nodes order by node_id;")
        cursor.execute(query)
        for node_id,latitude,longitude in cursor:
            if methName == 'gravity':
                result = UDB.parkingSearch(latitude, longitude, datetimestamp,conjestion)
            else:
                if methName == 'baseline':
                    result = UDB.parkingSearch(latitude, longitude, datetimestamp,conjestion,'baseline')
                else:
                    result = UDB.parkingSearch(latitude, longitude, datetimestamp,conjestion,'probabilistic')

            row_data = [str(datetimestamp),str(node_id),str(result[0]), str(result[1]), str(result[2]),str(result[3]),str(result[5])]
            print(row_data)
            if result[0] != -1:
                wrtFLcontents.append(row_data)
            
    writeFL = open(outFile,"w")    
    writer = csv.writer(writeFL)

    headStr = "Timestamp,Source_node_id,DestinationID,TotalTime,DrivingTime,WalkingTime,No_of_iteration"
    writer.writerow(headStr.split(","))

    for row_data in wrtFLcontents:
        writer.writerow(row_data)

    UDB.closeConnection(cnx)

    writeFL.close()

def __main__():
    gatherData('gravity',0.7,'/tmp/DataCollectionGravity_30.csv')

if __name__ == '__main__':
    __main__()
