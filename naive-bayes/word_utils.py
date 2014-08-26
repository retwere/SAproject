""" """

import re


def normalize(word):
    """Normalizes the input word. Right now it only lowercases it and removes
    non alpha-characters. Could replace with a stemmer in the future."""
    return re.sub('[^a-z]', '', word.lower())


def words(text):
    """An iterator over the words in text."""
    for word in text.split(' '):
        norm = normalize(word)
        if not norm:
            continue

        yield norm

def word_count(text):
    """Counts the number of times each word occurs in text."""
    counts = {}
    for word in words(text):
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
