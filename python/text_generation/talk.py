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
    return str.lower(re.sub('[^a-zA-Z0-9\n]', '', text1.rsplit(None, 1)[-1]))
    

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
            if (len(rhymes) < 4):
                sent = None

    return(sent)

def getSuessSentence(text_model):
    print ("Into the Suess")
    #generate a sentence
    sent1 = None
    sent2 = None

    while sent1 is None:
        #sent1 = text_model.make_sentence()
        sent1 = getShortSentence(text_model,140)
        last_word = getLastWord(sent1)
        #print (last_word)
        rhymes = pronouncing.rhymes(last_word)
        
        if len(rhymes) > 0 and sent1 is not None:
            for rhyme in rhymes:
                try:
                    #print(rhyme)
                    sent2 = text_model.make_sentence_with_start(beginning=rhyme)
                    if sent2 is not None:
                        print (sent1 + sent2)
                except Exception as e:
                    pass
                    #print (str(e))
                    sent1 = None 
                    sent2 = None

        else:
            sent1 = None
            sent2 = None
                


    return(sent1+" "+sent2)
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

text_model1 = markovify.Text(text1,state_size=3)
text_model2 = markovify.Text(text2,state_size=3)
text_model3 = markovify.Text(text3,state_size=3)



text_model = markovify.combine([text_model1, text_model2, text_model3],[1,1,1])

sent1 = None 
sent2 = None
print ("++")

while sent1 is None and sent2 is None:
    sent1 = getShortSentence(text_model,140)
    sent2 = getShortSentence(text_model,140)

    if doTheyRhyme(sent1,sent2):
            print (sent1 + " " + sent2)
    else:
        print ("nope :-(")
        sent1 = None
        sent2 = None





