import praw
import threading 
import time
import pylab as plt


def printDict(dic):      #Prints a dict in desired form
	for key,value in dic.items():
		print(key, ' : ', value)

reddit = praw.Reddit(client_id = '', #IMPORTANT: Change these fields to your corresponding reddit application fields 
									 #https://redditclient.readthedocs.io/en/latest/oauth/
					 client_secret = '', 
					 username = '',
					 password = '',
					 user_agent = 'whatever') #this field wont affect anything

subredditIn = input("What subreddit would you like to search? /r/").strip()
subreddit = reddit.subreddit(subredditIn)


duration = input("How long would you like to search new comments for (Minutes) ")


num = input("How many topics are you searching for? ").strip() 
valueDict = {} #Dictionary to hold the number of occurences of searched for words String/Integer
nicknameDict = {} #Dictionary to hold the aliases or things to attribute to searched for words String/List


for n in range(int(num)):   #Load up both the dictionaries here
	scan = input("Enter topics you are searching for in form (Topic: Keywords (single-word) seperated by spaces. \nFor example: Donald Trump:trump donald president. Type BREAK to stop entering topics ")
	print("\n")
	if scan.lower() == "break":
		break
	broken = scan.split(":")
	
	keyVal = broken[0].strip()
	keyWords = broken[1].split()
	valueDict.update({keyVal: 0})
	nicknameDict.update({keyVal : keyWords})

printDict(valueDict)
print('\n')
printDict(nicknameDict)

start = time.time()

def tallyUp(): #Add up how many of each keyword comes up
	global subreddit
	global valueDict
	global nicknameDict
	global start
	ctr = 0
	for comment in subreddit.stream.comments():
		ctr+=1
		end = time.time()  
		elapse = end - start  ##calculate elapsed time 
		commentArr = comment.body.lower().split()
		for key in nicknameDict:   
			for item in nicknameDict[key]:
				if item.lower() in commentArr:   #Search to see if any keywords are found, do not double count for one topic
					valueDict[key]+=1
					printDict(valueDict)
					print('Total Comments Processed: ',ctr,'Time Elapsed: ', elapse,'\n\n')
					break
			continue

t = threading.Thread(target = tallyUp)
t.daemon = True
t.start() 

time.sleep(int(duration) * 60)

numberedList = []
freqList = []
LABELS = [] 

for n in range(int(num)):
	numberedList.append(n+1) 

for key in valueDict:
	freqList.append(valueDict[key])

for key in valueDict:
	LABELS.append(key)


plt.bar(numberedList, freqList, align='center')
plt.xticks(numberedList, LABELS)
plt.xticks(rotation=90)
plt.xtics(size = 10)
plt.show()