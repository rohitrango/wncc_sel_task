"""
This script takes a file input.txt for all destination values. Takes the input from the user(via terminal). Gives a sorted list of nearest locations.
User is prompted to enter the output file name in .txt format as well.
Bird's eye view will be implemented soon.
Please wait for sometime, requests may take time to download.

EDIT: Bird's eye method has been implemented (using Haversine formula)
"""
import sys,requests,json
from math import sin,cos,atan2,pi,sqrt

def distance(self,other):																#was initially made as a class method	
																						#but later gave pains, so made it an independent function		
	if(other.lat==-1):																
		return -1																	#if destination isn't found, return -1 
	else:
		delLng = (other.lng-self.lng)*pi/180.0
		delLat = (other.lat-self.lat)*pi/180.0										#This is the Haversine formula that is used
		val = sin(delLat/2)**2 + cos(self.lat*pi/180.0)*cos(other.lat*pi/180.0)*(sin(delLng/2)**2)	
		temp = 2 * atan2(sqrt(val) , sqrt(1-val))		
		dist = temp*6373
		return dist

class Places:
	def __init__(self,dest,distance,value,lat,lng):										#value is the numerical value
		self.dest = dest
		self.distance = distance
		self.value = value
		self.lat = lat
		self.lng = lng

	#value will be -1 if too far, -2 if not found
	#this class will hold the name of the place, the distance and its numerical value

myfile = open("input.txt")																#taking all the destination values
mylocations = myfile.readlines()
myfile.close()

for i in range(len(mylocations)):
	mylocations[i] = mylocations[i][:-1]												#to omit the \n in all the places

source = raw_input("Enter source.\n")																	#source input 
print "Fetching data..."

# Creating new strings for passing in the API and getting JSON data (replacing <space> by plus

parseSource = source.replace(" ","+")
parseLocations = mylocations
for i in range(len(mylocations)):
	parseLocations[i] = mylocations[i].replace(" ","+")

# Checking whether source place exists or not

link = "http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s"
sourceData = requests.get(link%(parseSource,parseSource))
sourceJsonData = json.loads(sourceData.text)

	
sourceLat = sourceJsonData['routes'][0]['legs'][0]['end_location']['lat']				#source latitude and longitude
sourceLng = sourceJsonData['routes'][0]['legs'][0]['end_location']['lng']	
sourceDistance = sourceJsonData['routes'][0]['legs'][0]['distance']['text']				#source distance and its values
sourceDistanceValue = sourceJsonData['routes'][0]['legs'][0]['distance']['value']
sourcePlace = Places(source,sourceDistance,sourceDistanceValue,sourceLat,sourceLng)		#source Place object made 

places = []																				# source place exists
max_value = -3																			#to print the Not Found and no routes at the end. 
for i in range(len(parseLocations)):													#(after all nearest locations are the priority)
	sourceData = requests.get(link%(parseSource,parseLocations[i]))
	sourceJsonData = json.loads(sourceData.text)

	destStatus = sourceJsonData['status']												#status of the destination

	if(destStatus=="NOT_FOUND"):														#feeding in the parameters of the destination object
		temp = Places(mylocations[i],"Location not found",-2,-1,-1)						#-1 longitude latitude means place not found

	elif(destStatus=="ZERO_RESULTS"):													#feeding in the parameters of the destination object
		destinationReq = requests.get(link%(parseLocations[i],parseLocations[i]))		#getting request of the destination which is far away
		destinationData = json.loads(destinationReq.text)								#processing json
		temp = Places(mylocations[i],"No driving routes available", -1,destinationData['routes'][0]['legs'][0]['end_location']['lat'],destinationData['routes'][0]['legs'][0]['end_location']['lng'])

	elif(destStatus=="OK"):																#feeding in the parameters of the destination object
		endDistance = sourceJsonData['routes'][0]['legs'][0]['distance']['text']
		endValue = sourceJsonData['routes'][0]['legs'][0]['distance']['value']
		temp = Places(mylocations[i],endDistance,endValue,sourceJsonData['routes'][0]['legs'][0]['end_location']['lat'],sourceJsonData['routes'][0]['legs'][0]['end_location']['lng'])
	
	max_value = max(temp.value,max_value)
	places.append(temp)																	#All destination objects inserted

for i in range(len(places)):
	if(places[i].value== -2):
		places[i].value = max_value + 2
	elif(places[i].value== -1):
		places[i].value = max_value + 1

places.sort(key=lambda Places : Places.value)											#Sort according to distance value

outputFileName = raw_input("Please provide an output file name. (with .txt)\n")			#Give a file name

outputFile = open(outputFileName,"w")
outputFile.write("Source - %s \n\n"%(source))

for place in places:
	outputFile.write("Destination : %s \n"%(place.dest))
	outputFile.write("Distance by road : %s \n"%(place.distance))
	if(distance(sourcePlace,place)!=-1):
		outputFile.write("Bird's eye distance : %f km\n\n"%(distance(sourcePlace,place)))
	
outputFile.close()
