# Copyright 2014 Jake Fowler and Stephen Ra 

"""Count up the total number of words in each category, and the total number of
distinct words overall."""

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class Counter(MRJob):
    """A simple counter."""
    
    INPUT_PROTOCOL = JSONProtocol

    def mapper(self, key, value):
        category = key[0]
        
        # for the total in the category
        yield (category,'total'), value

        # for the number of distinct words (it counts even if it occurs 0 times)
        yield (category, 'distinct'), 1
        
    def reducer(self, key, values):
        yield key, sum(values)



if __name__ == '__main__':
    Counter().run()

