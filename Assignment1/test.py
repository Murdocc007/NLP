# __author__ = 'aditya'
#
# import  nltk
# from nltk.collocations import *
#
#
# def BiGram(fileName):
#     f = open(fileName, 'r')
#     words = nltk.word_tokenize(f.read())
#     #counting the frequency of the pairs
#     cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(words))
#
#     #counting the frequency of the distribution of the bigrams
#     fdist = nltk.FreqDist(nltk.bigrams(words))
#     for k,v in fdist.items():
#         print k,v
#
#     #mapping the pairs to the probabilities
#     cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)
#     for key in cprob_2gram.keys():
#         for val in cfreq_2gram[key].keys():
#             print cprob_2gram[key].prob(val)
#
#
# def BiGoodTuring(fileName):
#     f = open(fileName, 'r')
#     words = nltk.word_tokenize(f.read())
#     #counting the frequency of the pairs
#     cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(words))
#
#     #counting the frequency of the distribution of the bigrams
#     fdist = nltk.FreqDist(nltk.bigrams(words))
#     for k,v in fdist.items():
#         print k,v
#
#     #mapping the pairs to the probabilities
#     cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)
#     for key in cprob_2gram.keys():
#         for val in cfreq_2gram[key].keys():
#             print cprob_2gram[key].prob(val)
#
#
# def UniGram(fileName,GoodTuring=False):
#     f = open(fileName, 'r')
#     words = nltk.word_tokenize(f.read())
#     freq_1gram = nltk.FreqDist(words)
#     gd=nltk.probability.SimpleGoodTuringProbDist(freq_1gram)
#     if(GoodTuring==True):
#         for word in words:
#             print word,gd.prob(word)
#     else:
#         len_corpus = len(words)
#         for word in words:
#             print word,freq_1gram[word]/float(len_corpus)
#
# BiGoodTuring('/home/aditya/Desktop/Aditya/NLP/Assignment 1/test.txt')
# UniGram('/home/aditya/Desktop/Aditya/NLP/Assignment 1/test.txt',True)

