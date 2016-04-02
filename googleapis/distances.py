import sys,requests,json

class Places:
	def __init__(self,dest,distance,value):				#value is the numerical value
		self.dest = dest
		self.distance = distance
		self.value = value

	def getValue(self):
		return self.value

	#value will be -1 if too far, -2 if not found

myfile = open("input.txt")
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

link = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s"
sourceData = requests.get(link%(parseSource,parseSource))
sourceJsonData = json.loads(sourceData.text)

if(sourceJsonData['status'] == "NOT_FOUND"):
	print "Source value is incorrect.\n"
	sys.exit()

else:												# source place exists
	places = []

	for i in range(len(parseLocations)):
		sourceData = requests.get(link%(parseSource,parseLocations[i]))
		sourceJsonData = json.loads(sourceData.text)

		destStatus = sourceJsonData['status']

		if(destStatus=="NOT_FOUND"):
			temp = Places(mylocations[i],"Not Found",-2)

		elif(destStatus=="ZERO_RESULTS"):
			temp = Places(mylocations[i],"No driving routes available", -1)

		elif(destStatus=="OK"):
			distance = sourceJsonData['routes'][0]['legs'][0]['distance']['text']
			value = sourceJsonData['routes'][0]['legs'][0]['distance']['value']
			temp = Places(mylocations[i],distance,value)

		places.append(temp)		#All values inserted

	places.sort(key=lambda Places : Places.value)		#Sort according to distance value

	outputFileName = raw_input("Please provide an output file name. (with .txt)\n")

	outputFile = open(outputFileName,"w")
	outputFile.write("Source - %s \n\n"%(source))

	for place in places:
		outputFile.write("Destination : %s \n"%(place.dest))
		outputFile.write("Distance : %s \n\n"%(place.distance))
	
	outputFile.close()








