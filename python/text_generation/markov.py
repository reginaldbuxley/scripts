#!/usr/bin/python3
#this finally came in handy!

import warnings
import sys
import re
#import language_check
import markovify
import praw
from slackclient import SlackClient

# setup language helper
#tool = language_check.LanguageTool('en-US')

# setup slack
SLACK_TOKEN = "xXtokenXx"
sc = SlackClient(SLACK_TOKEN)


subreddit = 'Pizza'
sent_gen = 3



r = praw.Reddit(user_agent='comment grabber')
submissions = r.get_subreddit(subreddit).get_hot(limit=15)
text = ""
counter = 0

print("Starting comment scrump for " + str(subreddit))
#print (str(len(submissions)) + " submissions.")

for post in submissions:
    counter = counter + 1
    text = text + str(post.selftext)
    text = text + str(post.title)
    print("Grabbing comments for submission #" + str(counter))
    flat_comments = praw.helpers.flatten_tree(post.comments)
    for comment in flat_comments:
        try:
            text = text + str(comment.body)
        except:
            pass


# Build the model.
text_model_a = markovify.NewlineText(text, state_size=2)
print("Generating new sentences from the initial set, count =  ", sent_gen)

new_text = text
del text

for i in range(sent_gen):
    temp_sent = None
    while temp_sent is None:
        temp_sent = text_model_a.make_sentence()

    #matches = tool.check(temp_sent)
    #temp_sent = language_check.correct(temp_sent, matches)

    new_text = new_text + temp_sent + "\n"
    print(".", end="", flush=True)
print("")

# don't need this var anymore
del text_model_a


text_model_b = markovify.NewlineText(new_text, state_size=2)
end_result = ""


for i in range(3):
    fail_flag = False
    try:
        local_sent_ctr = 0
        local_sent = None
        while local_sent is None:
            local_sent_ctr = local_sent_ctr + 1
            local_sent = text_model_b.make_sentence()
            print("[SENTENCE GENERATION ATTEMPT " +
                  str(local_sent_ctr) + " FOR SENTENCE #" + str(i + 1) + "]")
        #matches = tool.check(local_sent)
        #local_sent = language_check.correct(local_sent, matches)
        try:
            print("[BEGIN TESTS]")

            if text_model_b.test_sentence_input(local_sent):
                print("Sentence Input Test Passed")
            else:
                print("Sentence Input Test Failed")
                fail_flag = True

            print("[END TESTS]")

            if fail_flag == True:
                print("Some tests failed")
            else:
                print("All tests passed")

            print("[SENTENCE] => " + str(local_sent))

            end_result = end_result + local_sent + " "

        except Exception as e:
            pass
            print("[TESTING THREW EXCEPTION] => " + str(e))
            print("[SENTENCE] => " + str(local_sent))
            i = i - 1

    except Exception as e:
        pass
        print("[THE WHOLE THING WENT WRONG JIM!]")
        print(str(e))

    print("-----------------------------")


try:
    # clean up the sentence a bit
    end_result = re.sub(r'\.([a-zA-Z])', r'. \1', end_result)
    # due to the above clean up, need to "re-fix" .com links
    end_result = re.sub('. com', '.com', end_result)
    # due to the above clean up, need to "re-fix" .net links
    end_result = re.sub('. net', '.net', end_result)
    # due to the above clean up, need to "re-fix" .org links
    end_result = re.sub('. org', '.org', end_result)
    # due to the above clean up, need to "re-fix" www links
    end_result = re.sub('www. ', 'www.', end_result)
    #matches = tool.check(end_result)
    #end_result = language_check.correct(end_result, matches)

    #end_result = "Sory, my englishe is not good. " + end_result
    # this guy will return info in his fail, so let's grab it'
    debug = None
    debug = sc.api_call("chat.postMessage", channel='#thesugarshack', text=str(end_result), username='chip', icon_emoji=':no_good:')

except Exception as e:
    pass
    print(str(e))
    print(debug)

print(end_result)

#del r
warnings.simplefilter("ignore", ResourceWarning)
