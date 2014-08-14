"""This is the 'trainer' for the Naive-Bayes model. It doesn't really have to 
do much though, because bag-of-words.py and counter.py have already done most 
of the work."""

import sys
import math

from mrjob.protocol import JSONProtocol
from mrjob.job import MRJob


class Trainer(MRJob):
    """This is the trainer for the Naive-Bayes model."""
    
    INPUT_PROTOCOL = JSONProtocol
    
    # this needs to be set to the totals for each category
    totals = {}
    
    # this needs to be set to the total number of distinct words
    distinct = 0
    
    # this is the parameter for the additive smoothing
    alpha = 1

    
    def mapper(self, key, value):
        category = key[0]
        
        yield key, math.log(
            (float(value) + self.alpha) / 
            (self.totals[category] + self.alpha*self.distinct))
        


    def reducer(self, key, values):
        for value in values:
            yield key, value


if __name__ == '__main__':
    #parse the counts of total and distinct words from counter.py (stdin)
    for line in sys.stdin.readlines():
        (key, value) = JSONProtocol().read(line)
        if key[1] == 'total':
            Trainer.totals[key[0]] = value
        elif key[1] == 'distinct':
            Trainer.distinct = value

    Trainer().run()
