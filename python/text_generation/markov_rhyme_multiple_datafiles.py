import language_check
import datetime
import os
import re
import pronouncing
import markovify
from slackclient import SlackClient
import codecs
import sys

spelltool = language_check.LanguageTool('en-US')

os.system("chcp 65001")

sent_pair_gen_num = 3
stub_sent_num = 1000

#short sentence max() == 35 per some dude at a college
stub_sent_length = 35
sent_length = 75

# Get raw text as string.
# with open("h:/text_chain_data.txt") as f:
with open("c:/temp/oz.txt") as f:
    text1 = f.read()

f.close()

with open("c:/temp/myth.txt") as g:
    text2 = g.read()

g.close()

with open("c:/temp/limmy.txt") as h:
    text3 = h.read()

h.close()

print (len(text1))
print (len(text2))
print (len(text3))

text_model_1 = markovify.Text(text1,state_size=3)
text_model_2 = markovify.Text(text2,state_size=3)
text_model_3 = markovify.Text(text3,state_size=2)


# Build the model.
# text_model = markovify.Text(text)
more_text1 = ""
more_text2 = ""
more_text3 = ""

gen_sentence1 = None
gen_sentence2 = None
gen_sentence3 = None

for i in range(stub_sent_num):
    while gen_sentence1 is None:
        gen_sentence1 = text_model_1.make_short_sentence(stub_sent_length)
        
        if (gen_sentence1 is not None) and ((more_text1.find(gen_sentence1)) >= 0):
            gen_sentence1 = None

    while gen_sentence2 is None:
        gen_sentence2 = text_model_2.make_short_sentence(stub_sent_length)
    
        if (gen_sentence2 is not None) and ((more_text2.find(gen_sentence2)) >= 0):
            gen_sentence2 = None

    while gen_sentence3 is None:
        gen_sentence3 = text_model_3.make_short_sentence(stub_sent_length)
    
        if (gen_sentence3 is not None) and ((more_text3.find(gen_sentence3)) >= 0):
            gen_sentence3 = None
            
    more_text1 = more_text1 + gen_sentence1 + "\n"
    more_text2 = more_text2 + gen_sentence2 + "\n"
    more_text3 = more_text3 + gen_sentence3 + "\n"

    if(i%80 == 0):
            print("\n",end="",flush=True)
    if(i%1000 ==  0):
        print("\n",i,"\n",end="",flush=True)

    print(".", end="", flush=True)




print()

try:
    del text_model_1
    del text_model_2
    del text_model_3
    text_model_1 = markovify.Text(text1 + "\n" + more_text1,state_size=2)
    text_model_2 = markovify.Text(text2 + "\n" + more_text2,state_size=2)
    text_model_3 = markovify.Text(text3 + "\n" + more_text3,state_size=2)
    text_model = markovify.combine([ text_model_1, text_model_2, text_model_3], [ 2, 0.5, 1 ])
    

except Exception as e:
    print(str(e))

print("done generating sentences.")
# setup slack
SLACK_TOKEN = "token"
sc = SlackClient(SLACK_TOKEN)
FINAL_TEXT = ""
LAST_LAST_WORD = ""
LAST_WORD = ""
attempt_ctr = 0

try:
    for i in range(sent_pair_gen_num):
        ZERO_TEXT = None
        ONE_TEXT = None
        
        
        int_ctr = 0

        while ZERO_TEXT is None:
            attempt_ctr = 0
            int_ctr = int_ctr + 1

            ZERO_LAST_WORD = ""
            
            print("Attempt #", (i + 1), " of pair", (sent_pair_gen_num), ". First line attempt #",
                  (int_ctr + 1), ". Second  line attempt: ", (attempt_ctr))

            ZERO_TEXT = text_model.make_short_sentence(sent_length)

            if ZERO_TEXT is not None:
                attempt_ctr = attempt_ctr + 1

                # last word of zero sentence
                ZERO_LAST_WORD = ZERO_TEXT.rsplit(None, 1)[-1]
                # get rid of punctuation and lower
                ZERO_LAST_WORD = str.lower(
                    re.sub('[^a-zA-Z0-9 \n]', '', ZERO_LAST_WORD))
                ZERO_LAST_WORD = ZERO_LAST_WORD.strip()

                # all the rhymes from the zero last word
                zero_rhymes = pronouncing.rhymes(ZERO_LAST_WORD)

                # check zero sentence last word for rhymes and require more
                # than 2 words that rhyme
                if (len(zero_rhymes) == 0) or (len(zero_rhymes) < 3) or (ZERO_LAST_WORD in {'he','me','it'}):
                    # set text back to none, hopefully keeps us in the loop.
                    ZERO_TEXT = None
                    

                else:
                    
                    # zero sentence was good, so let us generate a new sentence
                    while (ONE_TEXT is None) and (ZERO_TEXT is not None):
                        
                        ONE_LAST_WORD = ""
                        
                        # ONE_TEXT = text_model.make_sentence()
                        ONE_TEXT = text_model.make_short_sentence(sent_length)

                        if (ONE_TEXT is not None):
                            attempt_ctr = attempt_ctr + 1 
                            # last word of one sentence
                            ONE_LAST_WORD = ONE_TEXT.rsplit(None, 1)[-1]
                            # get rid of punctuation and lower
                            ONE_LAST_WORD = str.lower(
                                re.sub('[^a-zA-Z0-9\n\.]', '', ONE_LAST_WORD))
                            ONE_LAST_WORD = ONE_LAST_WORD.strip()
                            ONE_LAST_WORD = re.sub(r'[\.]','',ONE_LAST_WORD)

                            # if (ONE_LAST_WORD not in
                            # pronouncing.rhymes(ZERO_LAST_WORD)):
                            if (ONE_LAST_WORD not in zero_rhymes):
                                # it does not rhyme, try a new sentence by
                                # setting this back to None
                                ONE_TEXT = None

                            if (attempt_ctr > 100):
                                # our first sentence must be trash, reset!
                                ZERO_TEXT = None

                    if (ZERO_TEXT is not None) and (ONE_TEXT is not None):
                        print("we are saying", ZERO_LAST_WORD,
                              "rhymes with", ONE_LAST_WORD)
                            
                        matches0 = spelltool.check(ZERO_TEXT)
                        matches1 = spelltool.check(ONE_TEXT)

                        ZERO_TEXT = language_check.correct(ZERO_TEXT, matches0)
                        ONE_TEXT = language_check.correct(ONE_TEXT, matches1)

                        FINAL_TEXT = FINAL_TEXT + ZERO_TEXT + " " + ONE_TEXT + " " + "\n"
                
except Exception as e:
    pass
    print(str(e))

try:
    matches = spelltool.check(FINAL_TEXT)
    FINAL_TEXT = language_check.correct(FINAL_TEXT, matches)

    debug = sc.api_call("chat.postMessage", channel='#botsrcool',
    text=FINAL_TEXT, username='WubblyDubbly',
    icon_emoji=':botz::',)
    print()
    print(FINAL_TEXT)
except Exception as e:
    pass
