import warnings
import praw
from datetime import datetime

r = praw.Reddit(user_agent='PythonApp')

subreddit_ = 'showerthoughts'
submissions = r.get_subreddit(subreddit_).get_top(limit=5000)
text = ""
counter = 1

#print ("Starting comment scrump for " + str(subreddit))
#print ("Score, Author, Date, FullName, ID, ParentID, BodyLength")

try:
    for post in submissions:
        x = (post.title).encode('utf_8')
        print(x.decode('utf_8', errors='replace'))
        counter = counter + 1

    #rof
except Exception as e:
    print(str(e))

warnings.simplefilter("ignore", ResourceWarning)

