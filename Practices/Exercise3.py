#!/usr/bin/env python
# coding: utf-8

# In[57]:


import nltk
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from itertools import chain


#  # Algoritmo Lesk
# 
# Inspirado en el algoritmo de [Nurendra Choudhary](https://github.com/Akirato/Lesk-Algorithm/blob/master/leskAlgorithm.py), hecho en Python2

# In[58]:


def overlapcontext(synset, sentence):
    tokenize = []
    tokenize += word_tokenize(synset.definition())
    tokenize += chain(*[word_tokenize(eg) for eg in synset.examples()])
    return len(set(tokenize).intersection(sentence))


# In[59]:


def lesk( word, sentence ):
    bestsense = None
    maxoverlap = 0
    word=wordnet.morphy(word) if wordnet.morphy(word) is not None else word
    for sense in wordnet.synsets(word):
        overlap = overlapcontext(sense, set(sentence.split(' ')))
        for h in sense.hyponyms():
            overlap += overlapcontext(h, set(sentence.split(' ')))
        if overlap > maxoverlap:
                maxoverlap = overlap
                bestsense = sense
    return bestsense


# In[60]:


synset = lesk("bank","Yesterday I went to the bank to withdraw the money and the credit card did not work")
print("Synset:",synset)
if synset is not None:
    print("Significado:",synset.definition())
    num=0
    print("\nEjemplos:")
    for i in synset.examples():
        num=num+1
        print(str(num)+'.'+')',i)


# In[ ]:




