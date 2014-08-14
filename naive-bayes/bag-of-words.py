# Copyright 2014 Jake Fowler and Stephen Ra

"""This MRJob takes as input the raw reviews (in the form (key=category,value=text)) 
and calculates the 'bag of words'---the output will consist of (key,value) pairs 
where key=(category,word) and value=number of times the word occurs in all reviews
of that category.

In addition, there are two special keys, (category, TOTAL) which counts the total 
number of words that occured in all reviews of that category; and 
(category, DISTINCT) which counts the total number of distinct words in that 
category."""

import re

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
    """ """

    INPUT_PROTOCOL = JSONProtocol
    
    TOTAL = 0
    DISTINCT = 1 
    
    # This needs to be set to a list of all possible categories.
    possible_categories = []
    

    def steps(self):
        return [
            MRStep(mapper=self.mapper_bag,
                   reducer=self.reducer_bag),
            MRStep(mapper=self.mapper_totals,
                   reducer=self.reducer_totals)
            ]


    def mapper_bag(self, category, text):
        """Iterate over each word in the text, adding one to that category's
        bag."""

        for word in words(text):
            # add an instance of this word to category's bag
            yield (category, word), 1
            
            for cat in possible_categories:
                # this ensures that the word appears in every bag
                yield (cat, word), 0


    def reducer_bag(self, key, values):
        """Calculate the total number of each word in each bag."""
        
        yield key, sum(values)


    def mapper_totals(self, key, value):
        """Iterate over each (category, word) pair and add it to the totals."""
        
        category = key[0]
        
        # we also need to preserve the individual word counts
        yield key, value
        
        # add to the total
        yield (category, self.TOTAL), value
        
        # add to the total number of distinct words. Here we take advantage of the 
        # fact that we have already reduced it to the point where each word has a 
        # single entry per category. We only have to check whether the value is 0 
        # or not.
        yield (category, self.DISTINCT), 0 if value == 0 else 1


    def reducer_totals(self, key, values):
        """Sum up the totals."""
        
        yield key, sum(values)
