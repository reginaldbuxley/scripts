from os.path import expanduser
import random
import pronouncing
import markovify
import re

def doTheyRhyme(text1, text2):
    # all the rhymes from the zero last word
    try:
        if (getLastWord(text1) in pronouncing.rhymes(getLastWord(text2))) or (getLastWord(text2) in pronouncing.rhymes(getLastWord(text1))):
            return True
        else:
            return False
    except:
        return False

def getLastWord(text1):
    return str.lower(re.sub('[^a-zA-Z0-9\n\']', '', text1.rsplit(None, 1)[-1]))
    

def readFile(path):
    with open(path) as f:
        text = f.read()
    if f.closed is False:
        f.close()
    return(text)

def getShortSentence(text_model, length):
    sent = None
    while sent is None:
        sent = text_model.make_short_sentence(length)
        
        if (sent is not None):
            rhymes = pronouncing.rhymes(getLastWord(sent))
            if (len(rhymes) < 2):
                sent = None

    return(sent)

def getSuessSentence(text_model, length):
    #generate a sentence
    sent1 = None
    sent2 = None

    while sent2 is None:
        print (".",end="",flush=True)
        #sent1 = text_model.make_sentence()
        sent1 = getShortSentence(text_model,length)

        if sent1 is not None:
            last_word = getLastWord(sent1)
            
            #last_word = last_word.capitalize()
            rhymes = pronouncing.rhymes(last_word)

            if len(rhymes) > 2 and rhymes is not None: 
                for rhyme in rhymes:
                    try:
                        x = str(rhyme).capitalize()
                        sent2 = text_model.make_sentence_with_start(beginning=x)
                    except Exception as e:
                        #print ("e = " + str(e))
                        continue
            else:
                    sent2 = None
                        

        else:
            sent1 = None
            sent2 = None

            
    print()              
    sent2 = re.sub('___BEGIN__ ','',sent2)
    return(str(sent1)+" "+str(sent2))


    #return (sent1 + " " + sent2)


    
################
print ("HERE WE GO!")

home = expanduser("~")
print (home)

text1 = ""
text2 = ""
text3 = ""

path1 = ""
path2 = ""
path3 = ""

path1 = home + "/text_data/oz.txt"
text1 = text1 + readFile(path1)    

path2 = home + "/text_data/alice.txt"
text2 = text2 + readFile(path2)

path3 = home + "/text_data/threepigs.txt"
text3 = text3 + readFile(path3)

print (len(text1))
print (len(text2))
print (len(text3))

text_model1 = markovify.Text(text1,state_size=1)
text_model2 = markovify.Text(text2,state_size=1)
text_model3 = markovify.Text(text3,state_size=1)

    #combined text models do not seem to work correctly
    #throws : unorderable types: int() < NoneType()
#text_model = markovify.combine([ model_a, model_b ], [ 1.5, 1 ])
#text_model = markovify.combine([ text_model1, text_model2],[1,2])

text_model = markovify.Text(text1+text2+text3, state_size=3)
sent1 = None 
sent2 = None
print ("++")

sSent = None

for i in range(3):
    while sSent is None:
        sSent = getSuessSentence(text_model,80)
    print (sSent)
    sSent = None





#while sent1 is None and sent2 is None:
while 1 == 2:
    sent1 = getShortSentence(text_model,35)
    sent2 = getShortSentence(text_model,35)

    if doTheyRhyme(sent1,sent2):
            print (sent1 + " " + sent2)
    else:
        print (".",end="",flush=True)
        sent1 = None
        sent2 = None






