import tkinter as tk
from tkinter import simpledialog
import praw
import threading 
import time
import pylab as plt

def printDict(dic):      #Prints a dict in desired form
	for key,value in dic.items():
		print(key, ' : ', value)

reddit = praw.Reddit(client_id = 'qT0K97rukViXDg', #IMPORTANT: Change these fields to your corresponding reddit application fields 
									 			   #https://redditclient.readthedocs.io/en/latest/oauth/
					 client_secret = '',
					 username = '',
					 password = '',
					 user_agent = 'whatever') #this field wont affect anything

ROOT = tk.Tk()  #Create base for GUI
ROOT.withdraw()

topicCT = int(simpledialog.askstring(title="Number", prompt="How many topics are you searching for?"))
subredditIn = simpledialog.askstring(title="Subreddit", prompt="What subreddit are you searching in?")
duration = int(simpledialog.askstring(title="time", prompt="How many minutes would you like to search for?"))
subreddit = reddit.subreddit(subredditIn) #aassign sub to search in based on user response

valueDict = {} #Dictionary to hold the number of occurences of searched for words String/Integer
nicknameDict = {} #Dictionary to hold the aliases or things to attribute to searched for words String/List

for n in range(topicCT):   #Load up both the dictionaries here
	scan = simpledialog.askstring(title="Topic Search "+str(n+1)+'/'+str(topicCT), prompt="Enter your search in the form Topic: phrase, phrase, phrase...")
	
	broken = scan.split(":")
	
	keyVal = broken[0].strip()
	keyWords = broken[1].strip().split(',')
	valueDict.update({keyVal: 0})
	nicknameDict.update({keyVal : keyWords})

start = time.time() #Start keeping track of time after the user inputs their searches

def tallyUp(): #Add up how many of each keyword comes up
	global subreddit
	global valueDict
	global nicknameDict
	global start
	ctr = 0
	for comment in subreddit.stream.comments():
		ctr+=1
		end = time.time()  
		elapse = end - start  #Calculate elapsed time for console display
		for key in nicknameDict:   
			for item in nicknameDict[key]:
				if item.lower() in comment.body.lower():   #Search to see if any keywords are found, do not double count for one topic
					valueDict[key]+=1
					printDict(valueDict)
					print('Total Comments Processed: ',ctr,'Time Elapsed: ', elapse,'\n\n')
					break
			continue

t = threading.Thread(target = tallyUp) #Daemon threads run until the program is done running(program doesnt wait on them to finish)
t.daemon = True
t.start() 

time.sleep(int(duration) * 60) #Runs the program for user inputted time converted to minutes

numberedList = []  #Lists to graph
freqList = []
LABELS = [] 

for n in range(topicCT):
	numberedList.append(n+1) 

for key in valueDict:
	freqList.append(valueDict[key])

for key in valueDict:
	LABELS.append(key)

plt.bar(numberedList, freqList, align='center')  #Code to create a bar graph with labels aligned 90 degrees
plt.xticks(numberedList, LABELS)
plt.xticks(rotation=90)
str1 = 'Topic Search in /r/' + subredditIn
plt.title(str1)
plt.show()