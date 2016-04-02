"""
This script takes a file input.txt for all destination values. Takes the input from the user(via terminal). Gives a sorted list of nearest locations.
User is prompted to enter the output file name in .txt format as well.
Bird's eye view will be implemented soon.
Please wait for sometime, requests may take time to download.
"""
import sys,requests,json

class Places:
	def __init__(self,dest,distance,value):				#value is the numerical value
		self.dest = dest
		self.distance = distance
		self.value = value

	def getValue(self):
		return self.value

	#value will be -1 if too far, -2 if not found
	#this class will hold the name of the place, the distance and its numerical value

myfile = open("input.txt")							#taking all the destination values
mylocations = myfile.readlines()
myfile.close()

for i in range(len(mylocations)):
	mylocations[i] = mylocations[i][:-1]				#to omit the \n in all the places

source = raw_input("What is the name of the source place?\n")		#source input taken

# Creating new strings for passing in the API and getting JSON data (replacing <space> by plus

parseSource = source.replace(" ","+")
parseLocations = mylocations
for i in range(len(mylocations)):
	parseLocations[i] = mylocations[i].replace(" ","+")

# Checking whether source place exists or not

link = "http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s"
sourceData = requests.get(link%(parseSource,parseSource))
sourceJsonData = json.loads(sourceData.text)

if(sourceJsonData['status'] == "NOT_FOUND"):			#will exit if the source place doesn't exist
	print "Source value is incorrect.\n"
	sys.exit()

else:												# source place exists
	places = []
	max_value = -3									#to print the Not Found and no routes at the end. (after all nearest locations are the priority)
	for i in range(len(parseLocations)):
		sourceData = requests.get(link%(parseSource,parseLocations[i]))
		sourceJsonData = json.loads(sourceData.text)

		destStatus = sourceJsonData['status']

		if(destStatus=="NOT_FOUND"):
			temp = Places(mylocations[i],"Location not found",-2)

		elif(destStatus=="ZERO_RESULTS"):
			temp = Places(mylocations[i],"No driving routes available", -1)

		elif(destStatus=="OK"):
			distance = sourceJsonData['routes'][0]['legs'][0]['distance']['text']
			value = sourceJsonData['routes'][0]['legs'][0]['distance']['value']
			temp = Places(mylocations[i],distance,value)
		max_value = max(temp.value,max_value)
		places.append(temp)		#All values inserted

	for i in range(len(places)):
		if(places[i].value== -2):
			places[i].value = max_value + 2
		elif(places[i].value== -1):
			places[i].value = max_value + 1

	places.sort(key=lambda Places : Places.value)		#Sort according to distance value

	outputFileName = raw_input("Please provide an output file name. (with .txt)\n")

	outputFile = open(outputFileName,"w")
	outputFile.write("Source - %s \n\n"%(source))

	for place in places:
		outputFile.write("Destination : %s \n"%(place.dest))
		outputFile.write("Distance : %s \n\n"%(place.distance))
	
	outputFile.close()








