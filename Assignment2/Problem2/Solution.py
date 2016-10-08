from __future__ import division

#return the count of the words and the (tag,word) occurences
def count(fileName):
    file=open(fileName,'r')
    wordCount={} # a 1d dictionary of words
    tagWordCount={} # a 2d dictionary of tag words
    for line in file:
        words=line.split()
        for text in words:
            word,tag=text.split('_')
            #setting the wordCount
            if word in wordCount:
                wordCount[word]+=1
            else:
                wordCount[word]=1
            #setting the tagWordCount
            if word in tagWordCount:
                if tag in tagWordCount[word]:
                    tagWordCount[word][tag]+=1
                else:
                    tagWordCount[word][tag]=1
            else:
                tagWordCount[word]={}
                tagWordCount[word][tag]=1
    return wordCount,tagWordCount

#returns the most appropriate tag for a word which
#maximizes p(tag|word) in the form of a dictionary
def findTags(wordCount,tagWordCount):
    wordTag={}
    for word,word_count in wordCount.items():
        maxval=0
        for tag,tag_word_count in tagWordCount[word].items():
            prob=tag_word_count/word_count
            #setting the tag with max P(tag|word)
            if(prob>maxval):
                maxval=prob
                wordTag[word]=tag
    return wordTag

#return a list of words which contains the top 5 erroneous words
def topNErrorWords(fileName,wordTag,N):
    file=open(fileName,'r')
    totalError=0
    totalWords=0
    error={}
    for line in file:
        words=line.split()
        for text in words:
            totalWords+=1
            word,tag=text.split('_')
            if tag!=wordTag[word]:
               if word in error:
                   error[word]+=1
               else:
                   error[word]=1
    for word,val in error.items():
        totalError+=val
    print "Error: "+str(totalError/totalWords)
    res=sorted(error.items(),key=lambda x:x[1],reverse=True)
    return [x[0] for x in res[:N]]

#the top 5 erroneous tag words are "have","more","plans","that","'s"
#function applies 5 rules to the corresponding 5 most erroneous words
# and finds the corresponding total error
#return a list of words which contains the top 5 erroneous words
def topNErrorWordsCorrected(fileName,wordTag,N):
    file=open(fileName,'r')
    totalError=0
    totalWords=0
    errorWords=["that","more","have","'s","plans"]
    error={}
    prevTag=''
    for line in file:
        words=line.split()
        for text in words:
            totalWords+=1
            word,tag=text.split('_')
            if tag!=wordTag[word]:
                if word in errorWords:
                    if word=="that" and prevTag=="NNS" and tag=="WDT":
                        continue
                    elif word=="have" and prevTag=="PRP" and tag=="VBP":
                        continue
                    elif word=="more" and prevTag=="RB" and tag=="RBR":
                        continue
                    elif word=="plans" and prevTag=="IN" and tag=="NNS":
                        continue
                    elif word=="'s" and prevTag=="PRP" and tag=="VBZ":
                        continue
                if word in error:
                    error[word]+=1
                else:
                    error[word]=1
            prevTag=tag
    for word,val in error.items():
        totalError+=val
    print "Total number of erroneous tagged words after correction: "+str(totalError/totalWords)
    res=sorted(error.items(),key=lambda x:x[1],reverse=True)
    return [x[0] for x in res[:N]]


def writeNewTaggedFile(oldFileName,newFileName,wordTag):
    oldFile=open(oldFileName,'r')
    newFile=open(newFileName,'w')
    for line in oldFile:
        words=line.split()
        for text in words:
            word,tag=text.split('_')
            newFile.write(word+'_'+wordTag[word]+' ')
    oldFile.close()
    newFile.close()



if __name__=='__main__':
    fileName='./trainingdata.txt'
    wordCount,tagWordCount=count(fileName)
    wordTag=findTags(wordCount,tagWordCount)
    writeNewTaggedFile(fileName,'./newtaggeddata.txt',wordTag)
    top5ErrorWords=topNErrorWords(fileName,wordTag,5)
    print top5ErrorWords
    print topNErrorWordsCorrected(fileName,wordTag,5)














