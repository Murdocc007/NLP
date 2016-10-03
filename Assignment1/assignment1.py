#author: Aditya Mahajan (AXM156630)
from __future__ import division
import re

class BiGram:

    zeroCountSmoothProb=0 #static variable to store the good turing probability of the bigrams with
    def __init__(self,words):
        self.words=words
        self.count=0
        self.smoothProb=0
        self.addOneProb=0
        self.prob=0

    def getWords(self):
        return self.words

    def setCount(self,val):
        self.count=val

    def getCount(self):
        return self.count

    def getUnsmoothProb(self):
        return self.prob

    def getSmoothProb(self):
        return self.smoothProb

    def setUnsmoothProb(self,val):
        self.prob=val

    def setSmoothProb(self,val):
        self.smoothProb=val

    def setAddOneProb(self,val):
        self.addOneProb=val

    def getAddOneProb(self):
        return self.addOneProb

class UniGram:
    def __init__(self,word):
        self.word=word
        self.count=0
        self.prob=0
        self.smoothProb=0
        self.addOneProb=0

    def getWord(self):
        return self.word

    def setCount(self,val):
        self.count=val

    def getCount(self):
        return self.count

    def getUnsmoothProb(self):
        return self.prob

    def getSmoothProb(self):
        return self.smoothProb

    def setUnsmoothProb(self,val):
        self.prob=val

    def setSmoothProb(self,val):
        self.smoothProb=val

    def setAddOneProb(self,val):
        self.addOneProb=val

    def getAddOneProb(self):
        return self.addOneProb

#returns a list of tokens
def tokenizer(fileName,isFile=True):
    if(isFile==True):
        file=open(fileName,'r+')
        txt=file.read()
        file.close()
        return re.findall(r'(?ms)\W*(\w+)', txt)  # split words
    else:
        return re.findall(r'(?ms)\W*(\w+)', fileName)

#return a list of unigrams
def generateUnigrams(tokens):
    tokens.sort()
    prev=None
    #a list of the unigrams object
    unigrams=[]
    count=0
    flag=-1
    for idx,token in enumerate(tokens):
        if(token!=prev and idx!=0):
            temp=UniGram(prev)
            temp.setCount(count)
            unigrams.append(temp)
            count=1
        else:
            count+=1
        prev=token
    #setting the last unigram
    temp=UniGram(prev)
    temp.setCount(count)
    unigrams.append(temp)
    unigrams.sort(key=lambda k:k.getWord())
    return unigrams

#return a list of bigrams
def generateBigrams(tokens):
    bigramtokens=zip(*[tokens[i:] for i in range(2)])
    bigramtokens.sort()
    #a list of bigram objects
    bigrams=[]
    prev=None
    count=0
    for idx,token in enumerate(bigramtokens):
        if(token!=prev and idx!=0):
            temp=BiGram(prev)
            temp.setCount(count)
            bigrams.append(temp)
            count=1
        else:
            count+=1
        prev=token
    temp=BiGram(prev)
    temp.setCount(count)
    bigrams.append(temp)
    bigrams.sort(key=lambda k:k.getWords())
    return bigrams

#set the good turing probabilities of the bigrams
def setGoodTuringBigramProbability(bigrams,unigrams):
    #countmap stores the number of bigrams which occur with a given number of occcurences
    countMap=dict()
    for bigram in bigrams:
        if bigram.getCount() in countMap:
            countMap[bigram.getCount()]+=1
        else:
            countMap[bigram.getCount()]=1
    for c in countMap:
        prob=0
        Nc=countMap[c]
        Nc1=0
        if(c+1 in countMap):
            Nc1=countMap[c+1]
        if(c==0):
            prob=(Nc1)/len(unigrams)
        else:
            temp=((c+1)*(Nc1))/Nc
            prob=temp/len(unigrams)
        #need to optimize this inner loop
        #setting the smooth probabilities
        #of all bigrams with the given count
        for item in bigrams:
            if(item.getCount()==c):
                item.setSmoothProb(prob)
    BiGram.zeroCountSmoothProb=countMap[1]/len(bigrams) #N1/N,probability of count=0 bigrams

#finds a unigram with the given word
def findUnigram(unigrams,word):
    for unigram in unigrams:
        if(unigram.getWord()==word):
            return unigram
    return -1

#sets the unsmooth probabilities of the bigrams
def setUnsmoothBigramProbability(bigrams,unigrams):
    for bigram in bigrams:
        prob=0
        count=bigram.getCount()
        #get the first word in bigram
        firstword=bigram.getWords()[0]
        unigram=findUnigram(unigrams,firstword)
        if(unigram==-1):
            print firstword
        prob=count/(unigram.getCount())
        bigram.setUnsmoothProb(prob)

#sets the add one probabilities of the bigrams
def setAddOneBigramProbability(bigrams,unigrams):
    for bigram in bigrams:
        prob=0
        count=bigram.getCount()
        #get the first word in bigram
        firstword=bigram.getWords()[0]
        unigram=findUnigram(unigrams,firstword)
        prob=(count+1)/(unigram.getCount()+len(unigrams))#(C(Wn,Wn-1)+1)/(C(Wn-1)+V)
        bigram.setAddOneProb(prob)

def distinctCountBigram(Bigrams):
    map=[]
    for obj in Bigrams:
        if obj.getCount() not in map:
            map.append(obj.getCount())
    map.sort()
    print map

#return the count of a particular unigram
def getUnigramsCount(Unigrams,word):
    for unigram in Unigrams:
        if(unigram.getWord()==word):
            return unigram.getCount()
    return -1

#calculates the probability of the sentence
#takes 3 arguments, the Sentence,Bigrams and
# the type; which can be of 3
# types; unsmooth, goodturing and addone
def calculateSentenceProbability(Sentence,Bigrams,Unigrams,type='unsmooth'):
    Sentence=re.findall(r'(?ms)\W*(\w+)', Sentence) #tokenize the sentence
    bigramtokens=zip(*[Sentence[i:] for i in range(2)])
    prob=1
    if(type=='unsmooth'):
        for token in bigramtokens:
            found=-1
            for temp in Bigrams:
                if(temp.getWords()==token):
                    prob=prob*temp.getUnsmoothProb()
                    found=1
            if(found==-1): #if the token doesn't exist in the bigrams then return 0 as the probability
                prob=0.0
                # break
    elif(type=='addone'):
        for token in bigramtokens:
            found=-1
            for temp in Bigrams:
                if(temp.getWords()==token):
                    prob=prob*temp.getAddOneProb()
                    found=1
            if(found==-1): # if the token is not in the bigrams, then multiply it with 1/(C(Wn-1)+V)
                prob=prob*(1/(getUnigramsCount(Unigrams,token[0])+len(Unigrams)))
    else:
        for token in bigramtokens:
            found=-1
            for temp in Bigrams:
                if(temp.getWords()==token):
                    prob=prob*temp.getSmoothProb()
                    found=1
            if(found==-1):
                prob=prob*BiGram.zeroCountSmoothProb
    return prob

#print the bigrams count table in to the given file
def printBigramTable(bigrams,tokens,filename):
    file=open(filename,'w')
    #get the maximum length of the tokens for the maximum padding
    maxlen=0
    for token in tokens:
        if(len(token)>maxlen):
            maxlen=len(token)
    n=len(tokens)
    #make a matrix of size n+1xn+1
    matrix=[[0 for i in range(n+1)] for j in range(n+1)]

    for i in range(n):
        matrix[0][i+1]=tokens[i]
    for i in range(n):
        matrix[i+1][0]=tokens[i]
    for i in range(1,n+1):
        for j in range(1,n+1):
            for bigram in bigrams:
                if(bigram.getWords()[0]==tokens[i-1] and bigram.getWords()[1]==tokens[j-1]):
                    matrix[i][j]=bigram.getCount()
    #print the matrix
    for i in range(n+1):
        for j in range(n+1):
            file.write(str(matrix[i][j])+' '*(maxlen-len(str(matrix[i][j]))+1))
        file.write('\n')

#print the bigram probability table into the given file
def printBigramProbabilities(bigrams,tokens,filename,type='unsmooth'):
    file=open(filename,'w')
    #get the maximum length of the tokens for the maximum padding
    maxlen=0
    for token in tokens:
        maxlen=max(maxlen,len(token))
    n=len(tokens)
    #make a matrix of size n+1xn+1
    matrix=[[0.0 for i in range(n+1)] for j in range(n+1)]

    for i in range(n):
        matrix[0][i+1]=tokens[i]
    for i in range(n):
        matrix[i+1][0]=tokens[i]
    for i in range(1,n+1):
        for j in range(1,n+1):
            for bigram in bigrams:
                if(bigram.getWords()[0]==tokens[i-1] and bigram.getWords()[1]==tokens[j-1]):
                    if type=='unsmooth':
                        matrix[i][j]=bigram.getUnsmoothProb()
                    elif type=='addone':
                        matrix[i][j]=bigram.getAddOneProb()
                    else:
                        matrix[i][j]=bigram.getSmoothProb()
                    maxlen=max(maxlen,len(str(matrix[i][j])))
    #print the matrix
    for i in range(n+1):
        for j in range(n+1):
            file.write(str(matrix[i][j])+' '*(maxlen-len(str(matrix[i][j]))+1))
        file.write('\n')

if __name__ == "__main__":
    filePath='./NLPCorpusTreebank2Parts-CorpusA-Unix.txt'
    tokens=tokenizer(filePath)
    bigrams=generateBigrams(tokens)
    unigrams=generateUnigrams(tokens)


    setUnsmoothBigramProbability(bigrams,unigrams)
    setAddOneBigramProbability(bigrams,unigrams)
    setGoodTuringBigramProbability(bigrams,unigrams)

    s1="The president has relinquished his control of the company's board."
    s2="The chief executive officer said the last year revenue was good."

    print 'First sentence is "'+s1+'"'
    print 'Second sentence is "'+s2+'"'

    tokens1=tokenizer(s1,isFile=False)
    bigrams1=generateBigrams(tokens1)

    tokens2=tokenizer(s2,isFile=False)
    bigrams2=generateBigrams(tokens2)


    printBigramTable(bigrams1,tokens1,'./countTable1.txt')
    printBigramTable(bigrams2,tokens2,'./countTable2.txt')

    printBigramProbabilities(bigrams,tokens1,'./unsmooth1.txt')
    printBigramProbabilities(bigrams,tokens2,'./unsmooth2.txt')

    printBigramProbabilities(bigrams,tokens1,'./addOne1.txt',type='addone')
    printBigramProbabilities(bigrams,tokens2,'./addOne2.txt',type='addone')

    printBigramProbabilities(bigrams,tokens1,'./goodTuring1.txt',type='goodturing')
    printBigramProbabilities(bigrams,tokens2,'./goodTuring2.txt',type='goodturing')

    print 'Unsmooth probability'
    print 'Sentence 1: ',
    print calculateSentenceProbability(s1,bigrams,unigrams)
    print 'Sentence 2: ',
    print calculateSentenceProbability(s2,bigrams,unigrams)

    print 'Addone probability'
    print 'Sentence 1: ',
    print calculateSentenceProbability(s1,bigrams,unigrams,type='addone')
    print 'Sentence 2: ',
    print calculateSentenceProbability(s2,bigrams,unigrams,type='addone')

    print 'GoodTuring probability'
    print 'Sentence 1: ',
    print calculateSentenceProbability(s1,bigrams,unigrams,type='goodturing')
    print 'Sentence 2: ',
    print calculateSentenceProbability(s2,bigrams,unigrams,type='goodturing')




