from nltk.corpus import wordnet 
from nltk.tokenize.treebank import TreebankWordTokenizer
import sys


def computerOverlap( synset, sentence ):
    meaning_set = set(TreebankWordTokenizer().tokenize(synset.definition()))
    sentence = set(sentence.split(" "))
    return len( meaning_set.intersection(sentence) ) #get the intersection between the meaning and the sentence

def simplifiedLesk( word, sentence ):
    best_sense = None
    max_overlap = 0
    #get the base word for the inflected words
    word=wordnet.morphy(word) if wordnet.morphy(word) is not None else word
    for sense in wordnet.synsets(word):
        overlap = computerOverlap(sense,sentence)
        examples=sense.hyponyms() #computing the hyponyms of the words
        for h in examples:
            overlap += computerOverlap( h, sentence )#adding the overlap of the hyponyms of the words
        if overlap > max_overlap: #get the best overlap
                max_overlap = overlap
                best_sense = sense
    return best_sense


sentence = raw_input("Enter the Sentence :")
word = raw_input("Enter the word :")

res = simplifiedLesk(word,sentence)
print '\n'
print "Synset:",res
print "Meaning:",res.definition()
