## CS-581
### DBMS final project - Resource Search Project

### Group 2: Sreejith Menon, Rajan Shekar Bhandari, Thomas Dutta, Imran Choudhury

All scripts are stored under the folder script. The software assumes the availability of MySQL database for execution.


-------------------------------------------Requirements:-------------------------------------------------------------

Anaconda (RECOMMENDED)
https://www.continuum.io/
All .ipynb scripts can be run in IPython Notebook

OR 

Python 3.5
All .py scripts can be executed using command line arguments as described below.

--------------------------------------------Environment setup-------------------------------------------------------
The parking resource search highly depends on pre-computed distance and times between nodes which are stored in the MySQL database.

Please create a database ParkingProject in MySQL and the execute the below SQL.
SQL/Dump parking Project.sql

This will create all required tables and load the needed data onto the database.

------------------------------------Non-deterministic searches-------------------------------------------------------
UninformedSearchWithDB.py 
can be used for running the following algorithms:
1. Uninformed search with Greedy algorithm
2. Uninformed search with Gravitational pull algorithm
3. Historical parking search using Gravitational pull algorithm

****NOTE: The default connections are specified in the method.
connectToMySQL(userName='root',password='password',DBName='parkingproject'):
The method definition is at line number: 85

These defaults can be overridden to connect to a local instance by changing the below line
NOW: cnx = connectToMySQL()
Change it to: cnx = connectToMySQL(<user>,<password>,<dbname>)

The script can be run at command line using the below command
#### python UninformedSearchWithDB.py

#### The driving method is parkingSearch()
Expected parameters: source latitude, sournce longitude, request time, congestion percentage, method name
Valid values for methodName = 'uninformed' or 'probabilistic' or 'baseline' 
Return values : selected slot ID, total parking time, driving time, walking time, waypoints and number of iterations

The results on the screen are the method calls made inside the __main__() method.
For instance,
print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',1,'baseline'))  # returns the results found using baseline search

print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',1))  # returns the results found using uninformed search using gravitational pull algorithm

print(parkingSearch(37.808245,-122.415816,'2012-05-05 23:40:13',1,'probabilistic'))  # returns the results found using historical search using gravitational pull algorithm

#### Deterministic search
#### InformedSearchWithRealTimeData.ipynb

Make a Call to function in a seperate block in the notebook
#### findRealTimeParkingBlock(sourcePt,dest,time,congestionlevel,sourceId,drivetimeduration,iteration)

#### Definitions of the arguments
sourcePt – Source for the algorithm (provide any node end point value i.e. intersection value from database)
dest – Destination for the algorithm (source and destination are same in our implementation)
time – start datetime of algorithm
congestionlevel – provide value like 0, 20 , 30 etc.
sourceId – node Id of the intersection acting as sourcePt
drivetimeduration – provide as 0
iteration – provide as 0 

### Sample Run
findRealTimeParkingBlock(Point(37.806054, -122.410329),Point(37.806054, -122.410329),'2012-04-06 00:06:32',0,7038,0,0)


#### Simulation scripts
#### Simulation.py 
is a script used to simulate all the experiments

Experiments are conducted by making calls inside the __main__() function as described below:
All experiments can be conducted by making calls to the method:
gatherData(methName,conjestion,outFile)
Expected parameters: Algorithm or method name, congestion level and name of the output csv file expeceted
Accepted method names: gravity, baseline or probabilistic
Output: A CSV file with the specified outFile name having below header
Timestamp,Source_node_id,DestinationID,TotalTime,DrivingTime,WalkingTime,No_of_iteration

#### Additionals
The one time precomputations can be reconducted by using the below IPython Notebook code.
#### OneTimePreComputation.ipynb
