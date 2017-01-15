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

#transform a crude line to a refined one
def transformText(line):
    #remove sgml tags
    tag=re.compile("\\<.*?>")
    line = tag.sub(" ",line)


    #remove digits
    tag=re.compile("[\\d+]")
    line = tag.sub("",line)

    #remove special characters
    tag=re.compile("[+^:,?;=%#&~`$!@*_)/(}{\\.]")
    line = tag.sub("",line)

    #remove possesives
    tag=re.compile("\\'s")
    line = tag.sub("",line)

    #replace the "'" with space
    tag=re.compile("\\'")
    line = tag.sub(" ",line)

    #replace the "-" with space
    tag=re.compile("-")
    line = tag.sub(" ",line)

    #replace multiple spaces with a single space
    tag=re.compile("\\s+")
    line = tag.sub(" ",line)

    #convert the line to lowercase
    line=line.lower()

    return line


#prioritizing lemma, adjective, verb and noun
def createLemmas(string):
    string=transformText(string)
    lemmatizer = WordNetLemmatizer()
    poss=['a','v','n']
    words=string.split()
    lemma={}
    for word in words:
        lemma[word]=word
        for p in poss:
            try:
                lemma[word]=lemmatizer.lemmatize(lemma[word],pos=p)
            except:
                lemma[word] = ''
    return lemma

#bigrams
def bigrams(string):
    string = transformText(string)
    words = string.split()
    bigrams = []
    i=1
    while i<len(words):
        bigrams.append([words[i-1],words[i]])
        i += 1

    return bigrams

#POS tagger
def posTagger(string):
    string = transformText(string)
    words = string.split()
    tags = nltk.pos_tag(words)
    res = {}
    for word,tag in tags:
        try:
            res[tag] += 1
        except:
            res[tag] = 1

    return res

#HyperNym
def hyperNym(string):
    string = transformText(string)
    words = string.split()
    res = []
    for word in words:
        try:
            for ss in wn.synsets(word):
                for hyper in ss.hypernyms():
                    res.append(str(hyper.lemmas()[0].name()))
        except:
            flag=1
    return list(set(res))

#SynoNym
def synoNym(string):
    string = transformText(string)
    words = string.split()
    res = []
    for word in words:
        try:
            for ss in wn.synsets(word):
                #print word, ss.lemmas()
                res.append(str(ss.lemmas()[0].name()))
        except:
            flag = 1
    
    return list(set(res))
    
#Dependency Parser
def syntacticDependencyParsing(string):
    res = {}
    try:
        ajaxurl='http://demo.ark.cs.cmu.edu/parse/api/v1/parse'
        r = requests.get(ajaxurl + '?sentence=' + string)
        json_data=json.loads(r.content)
        #print 'Number of relations:',
        #print len(json_data['sentences'][0]['relations'])
        tokens=json_data['sentences'][0]['tokens']
        for temp in json_data['sentences'][0]['relations']:
            relation= temp[1]
            tuple_start=temp[2][0]
            tuple_end=temp[2][1]
            term_start=int(tuple_start[1][-1])-1
            term_end=int(tuple_end[1][-1])-1
            #print 'Relation: '+relation,
            #print tokens[term_start]+'  -->  '+tokens[term_end]
            try:
                res[relation] += 1
            except:
                res[relation] = 1
    except:
        flag = 1
    return res


def create_uni_feats(words):
    words = words.split()
    return dict([(word,True) for word in words])

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    words = words.split()
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d=dict()
    for words in bigrams:
        d[words]=True
    return d

def stopword_filtered_word_feats(words):
    words = words.split()
    return dict([(word, True) for word in words if word not in stopset])

def lemmas_word_feats(words):
    words = words.split()
    res = []
    for word in words:
        word = transformText(word)
        if word not in stopset:
            lemmas = createLemmas(word)
            for lemma in lemmas:
                res.append((lemma, True))
    return dict(res)

def posTagger_feats(words):
    posTags = posTagger(words)
    #print posTags
    res = []
    for tags in posTags:
        res.append((tags, True))

    return dict(res)

def hyperNym_feats(words):
    res = []
    for word in hyperNym(words):
        res.append((word, True))

    return dict(res)

def synNym_feats(words):
    res = []
    for word in synoNym(words):
        res.append((word, True))

    return dict(res)

def syntacticDependencyParsing_feats(words):
    res = []
    #print words
    for word in syntacticDependencyParsing(words):
        res.append((word, True))

    return dict(res)

def all_feats(words):
    res = {}
    res = bigram_word_feats(words)
    for key in lemmas_word_feats(words):
        res[key] = True
    for key in posTagger_feats(words):
        res[key] = True
    for key in hyperNym_feats(words):
        res[key] = True
    for key in synNym_feats(words):
        res[key] = True
    for key in syntacticDependencyParsing_feats(words):
        res[key] = True
    return res

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


def customTest(string,classifier,featcreator):
    if classifier.classify(featcreator(string))=='pos':
        print ":)"
    elif classifier.classify(featcreator(string))=='neg':
        print ":("

url='./data.txt'
print
print
print "Baseline Strategy"
print "Each word is a feature itself"
baseline = foo(url,create_uni_feats)
print



print
print "Test Sample"
print "I do like Angels and Demons more then The Da Vinci Code."
s = "I do like Angels and Demons more then The Da Vinci Code."
print
print "Lemma features"
print lemmas_word_feats(s)
print
print "Bigram features"
print bigram_word_feats(s)
print
print "POSTager features"
print posTagger_feats(s)
print
print "syntacticDependencyParsing features"
print syntacticDependencyParsing_feats(s)
print
print "hyperNym_feats features"
print hyperNym_feats(s)
print
print "synNym_feats features"
print synNym_feats(s)
print

print "Baseline Classification of Test Sample"
customTest(s, baseline, create_uni_feats)
