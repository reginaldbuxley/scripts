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
            if (len(rhymes) < 1):
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

            if len(rhymes) > 3 and rhymes is not None: 
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

