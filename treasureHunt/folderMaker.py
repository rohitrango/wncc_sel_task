"""
This is the programming task for WnCC Conveners.
Program assumes the format - 
<Question>
<Option 1>
<Option 2>

<Answer>

....(Next question)

IMPORTANT - Please don't put extra newlines after the last answer.
Non-recursive solution is implemented. :P 
Thanks for viewing (and contributing) to this code.
"""
import os,sys

if len(sys.argv) < 2 :					#You can provide the input file name as a parameter, if you don't, program assumes the name "input.txt"		
	textFile = "input.txt"
else:
	textFile = sys.argv[1]

#Now to take the contents of the file. 

questionNo = 1							#this variable tracks question number
myFile = open(textFile)					#opening the input file
myContent = myFile.readlines()			
myFile.close()			
	
index = 0								#iterate thru all items in the input.txt file
while index < len(myContent):

	options = []
	question = myContent[index]
	index+=1
	while(myContent[index]!='\n'):
		options.append( myContent[index][0:len(myContent[index])-1] )			# to omit the \n part from the file name
		index+=1
	index+=1
	answer = myContent[index][0:len(myContent[index])-1]				#to omit the \n part of the file name
	index+=2

	# At this point we have the question, list of options and the answer, time to make the directories 

	localFileText = "q"+str(questionNo)+".txt"			#creating the question number file text
	localFile = open(localFileText,"w")
	localFile.write(question)
	localFile.close()
	questionNo+=1

	for myOption in options:
		os.mkdir(myOption)

	os.chdir(os.path.join(os.getcwd(),answer))

	#folders made and we go to the next folder
	#Make the win.txt file
winFile = open("win.txt","w")
winFile.write("You Win!\n")
winFile.close()


