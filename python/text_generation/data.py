import warnings
#import pypyodbc
#import re
#import os
import praw
from datetime import datetime

r = praw.Reddit(user_agent='PythonApp')

subreddit_ = 'something'
submissions = r.get_subreddit(subreddit_).get_new(limit=5000)
text = ""
counter = 1

#print ("Starting comment scrump for " + str(subreddit))
print ("Score, Author, Date, FullName, ID, ParentID, BodyLength")

try:
    for post in submissions:
        
        post_author = str(post.author)
        post_author = post_author.replace('Redditor(user_name=\'','')
        post_author = post_author.replace('\')','')
        date = str(datetime.utcfromtimestamp(post.created_utc))
        #print ((post.score, post_author, date, post.fullname,post.id,post.num_comments, post.permalink, post.title))
        x = str((post.score, post_author, date, post.fullname,post.id,post.num_comments, post.permalink, post.title))
        x = x.replace('(','')
        x = x.replace(')','')
        #print (x)
        #print("Grabbing comments for submission #" + str(counter))
        
        flat_comments = praw.helpers.flatten_tree(post.comments)
        for comment in flat_comments:
            try:
                #comment_author  = re.sub('Redditor(user_name=\'', '', comment.author)
                #comment_author = re.sub('\')','',comment_author)
                comment_author = str(comment.author)
                comment_author  = comment_author.replace('Redditor(user_name=\'','')
                comment_author = comment_author.replace('\')','')
                date = str(datetime.utcfromtimestamp(comment.created_utc))
                body_length = len(str(comment.body)) - 2 #sub 2 for the padding 
                z = str((comment.score, comment_author, date, comment.fullname, comment.id, comment.parent_id, body_length))
                z = z.replace('(','')
                z = z.replace(')','')
                print (z)
                
            except:
                pass

        counter = counter + 1 

    #rof
except Exception as e:
    print(str(e))

warnings.simplefilter("ignore", ResourceWarning)

