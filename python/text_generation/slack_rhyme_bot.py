import datetime
import os
import re
import pronouncing
import markovify
from slackclient import SlackClient
import codecs
import sys

#this is a windows thing when sending wacky chars to print()
os.system("chcp 65001")

sent_pair_gen_num = 3
stub_sent_num = 100000
stub_sent_length = 35 #max length of a "short sentence"
sent_length = 70 #2x short sent len - allows for more flows in the pairing

# Get raw text as string.
# I am using a flat file of lyrics scraped from the web.
with open("c:/temp/markov_chain_data_lyrics.txt") as f:
    text = f.read()

# Build the model.
# text_model = markovify.Text(text)
more_text = ""
text_model = markovify.NewlineText(text,state_size=1)
gen_sentence = None

for i in range(stub_sent_num):
    while gen_sentence is None:
        gen_sentence = text_model.make_short_sentence(stub_sent_length)
        
        if (more_text.find(gen_sentence)) > 0:
            gen_sentence = None
            
    more_text = more_text + gen_sentence + ".\n"
    print(".", end="", flush=True)

print()

try:
    del text_model
    text_model = markovify.NewlineText(text + "\n" + more_text,state_size=2)
except Exception as e:
    print(str(e))

print("done generating sentences.")
# setup slack
SLACK_TOKEN = "slack_token_goes_here"
sc = SlackClient(SLACK_TOKEN)
FINAL_TEXT = ""
LAST_LAST_WORD = ""
LAST_WORD = ""
attempt_ctr = 0

try:
    for i in range(sent_pair_gen_num):
        ZERO_TEXT = None
        ONE_TEXT = None
        
        attempt_ctr = 0
        int_ctr = 0

        while ZERO_TEXT is None:
            
            
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
                        attempt_ctr = attempt_ctr + 1
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

                            # if (ONE_LAST_WORD not in
                            # pronouncing.rhymes(ZERO_LAST_WORD)):
                            if (ONE_LAST_WORD not in zero_rhymes):
                                # it does not rhyme, try a new sentence by
                                # setting this back to None
                                ONE_TEXT = None

                            if (attempt_ctr > 100):
                                # our first sentence must be trash, reset!
                                attempt_ctr = 0
                                int_ctr = int_ctr + 1
                                ONE_TEXT = None
                                ZERO_TEXT = None

                    if (ZERO_TEXT is not None) and (ONE_TEXT is not None):
                        print("we are saying", ZERO_LAST_WORD,
                              "rhymes with", ONE_LAST_WORD)
                        FINAL_TEXT = FINAL_TEXT + ZERO_TEXT + ". " + ONE_TEXT + ". " + "\n"
                
except Exception as e:
    pass
    print(str(e))

try:
    debug = sc.api_call("chat.postMessage", channel='#slackchan',
    text=FINAL_TEXT, username='botname',
    icon_emoji=':musical_score:',)
    print()
    print(FINAL_TEXT)
except Exception as e:
    pass
