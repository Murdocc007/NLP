import time
import json
import requests
import collections,itertools
import nltk
import nltk.classify.util, nltk.metrics
from nltk.corpus import wordnet as wn
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
stopset = set(stopwords.words('english'))


#Dependency Parser
def syntacticDependencyParsing(string):
    res = {}
    try:
        ajaxurl='http://demo.ark.cs.cmu.edu/parse/api/v1/parse'
        r = requests.get(ajaxurl + '?sentence=' + string)
        json_data=json.loads(r.content)
        print 'Number of relations:',
        print len(json_data['sentences'][0]['relations'])
        tokens=json_data['sentences'][0]['tokens']
        for temp in json_data['sentences'][0]['relations']:
            relation= temp[1]
            tuple_start=temp[2][0]
            tuple_end=temp[2][1]
            term_start=int(tuple_start[1][-1])-1
            term_end=int(tuple_end[1][-1])-1
            print 'Relation: '+relation,
            print tokens[term_start]+'  -->  '+tokens[term_end]
            try:
                res[relation] += 1
            except:
                res[relation] = 1
    except:
        flag = 1
    return res

def syntacticDependencyParsing_feats(words):
    res = []
    #print words
    for word in syntacticDependencyParsing(words):
        res.append((word, True))

    return dict(res)

def foo(fileName,featcreator):
    negfeats=[]
    posfeats=[]
    with open(fileName, "r") as ins:
        posCount = 0
        negCount = 0
        for line in ins:
            #print posCount
            s=line.split('\t')
            s[1]=s[1].lower()
            if s[0]=='1' and posCount<50:
                posCount += 1
                posfeats.append([featcreator(s[1]),'pos'])
            elif s[0]=='0' and negCount<50:
                negCount += 1
                negfeats.append([featcreator(s[1]),'neg'])


    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = posfeats[:poscutoff] + negfeats[:negcutoff]
    testfeats = posfeats[poscutoff:] + negfeats[negcutoff:]

    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    return classifier


url='/home/aditya/Desktop/Aditya/NLP/Assignments/FinalProject/data.txt'



print "syntacticDependencyParsing"
foo(url,syntacticDependencyParsing_feats)