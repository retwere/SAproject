# Copyright 2014 Jake Fowler and Stephen Ra

"""Helper functions for dealing with splitting text and normalizing words."""


import re


def normalize(word):
    """Return a normalized version of the word."""
    # for now, we just lowercase the word and remove any non-alpha characters
    # in the future, we could add a stemmer here, e.g.
    return re.sub('[^a-z]', '', word.lower())



def words(text):
    """An iterator over the words in text."""
    
    for word in text.split():
        norm = normalize(word)
        
        if not word:
            continue
            
        yield norm


def word_count(text):
    """Counts the words in the text."""
    
    counts = {}

    for word in words(text):
        if word in counts.keys() then:
            counts[word] += 1
        else:
            counts[word] = 1
