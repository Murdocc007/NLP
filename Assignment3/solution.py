from nltk.corpus import wordnet 
from nltk.tokenize.treebank import TreebankWordTokenizer
import sys


def computerOverlap( synset, sentence ):
    gloss = set(TreebankWordTokenizer().tokenize(synset.definition()))
    sentence = set(sentence.split(" "))
    return len( gloss.intersection(sentence) )

def simplifiedLesk( word, sentence ):
    best_sense = None
    max_overlap = 0
    word=wordnet.morphy(word) if wordnet.morphy(word) is not None else word
    for sense in wordnet.synsets(word):
        overlap = computerOverlap(sense,sentence)
        signature=sense.hyponyms()
        for h in signature:
            overlap += computerOverlap( h, sentence )
        if overlap > max_overlap:
                max_overlap = overlap
                best_sense = sense
    return best_sense


sentence = raw_input("Enter the Sentence :")
word = raw_input("Enter the word :")

res = simplifiedLesk(word,sentence)
print "\n\nSynset:",res
print "Meaning:",res.definition()
