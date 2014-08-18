# Copyright 2014 Jake Fowler and Stephen Ra

"""This MRJob takes as input the raw reviews (in the form (key=category,value=text)) 
and calculates the 'bag of words'---the output will consist of (key,value) pairs 
where key=(category,word) and value=number of times the word occurs in all reviews
of that category."""

import re
import sys

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol



def words(text):
    """An iterator over the words in text."""

    for word in text.split():
        # normalize the word by lowercasing and dropping non-alpha characters
        key = re.sub('[^a-z]', '', word.lower())
        
        if not key:
            continue

        yield key


class BagOfWords(MRJob):
    """Counts how many times each word occurs in each 'bag' (i.e. category)."""

    INPUT_PROTOCOL = JSONProtocol
    
    # This needs to be set to a list of all possible categories.
    possible_categories = []
    

    def mapper(self, category, text):
        """Iterate over each word in the text, adding one to that category's
        bag."""

        for word in words(text):
            # add an instance of this word to category's bag
            yield (category, word), 1
            
            for cat in self.possible_categories:
                # this ensures that the word appears in every bag
                yield (cat, word), 0


    def reducer(self, key, values):
        """Calculate the total number of each word in each bag."""
        
        yield key, sum(values)




if __name__ == '__main__':
    #Read from stdin the list of possible categories (one per line)
    for line in sys.stdin.readlines():
        # Note: rstrip is needed to strip off trailing \n from line
        BagOfWords.possible_categories.append(line.rstrip()) 

    BagOfWords().run()
