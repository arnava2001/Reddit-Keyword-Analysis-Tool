import praw

reddit = praw.Reddit(client_id = '', #IMPORTANT: Change these fields to your corresponding reddit application fields 
									 			   #https://redditclient.readthedocs.io/en/latest/oauth/
					 client_secret = '', 
					 username = '',
					 password = '',
					 user_agent = 'whatever') #this field wont affect anything

subList = list(reddit.user.subreddits(limit=None))

for sub in subList:
	sub.unsubscribe()