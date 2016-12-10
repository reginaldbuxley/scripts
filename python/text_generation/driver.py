import markovify
import talk
from os.path import expanduser

talker = talk

q = "this is the sentence yo."
print (talker.getLastWord(q))
 


################
print ("HERE WE GO!")

home = expanduser("~")

text1 = ""
path1 = ""

path1 = home + "/text_data/showerthoughts_titles.txt"
text1 = text1 + talker.readFile(path1)    



text_model = markovify.Text(text1, state_size=3)
sent1 = None 
sent2 = None
print ("-o^o-")

sSent = None

for i in range(0):
    while sSent is None:
        sSent = talker.getSuessSentence(text_model,80)
    print (sSent)
    sSent = None


while sent1 is None and sent2 is None:
    print(".",end="",flush=True)
    sent1 = talker.getShortSentence(text_model,70)
    sent2 = talker.getShortSentence(text_model,70)

    if sent1 is not None and sent2 is not None:
        if talker.doTheyRhyme(sent1,sent2):
                print (sent1 + " " + sent2)
        else:
            sent1 = None
            sent2 = None






