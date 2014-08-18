"""This attempts to classify a review based on the training data. It takes into 
stdin the 'bag of words' of the review, and as the first argument the path to 
the file containing the output of nb-trainer.py.

The output is a list of the possible categories with the probability that the
given review is in the category."""

import sys
import math

#from decimal import Decimal

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.step import MRStep


class Classifier(MRJob):
    """"""
    
    INPUT_PROTOCOL = JSONProtocol

    input_words = {}

    #Note that we will work in log scale to avoid overflow errors
    multiplier = 0
    
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper_multiply,
                   reducer=self.reducer_calc_score),
            MRStep(reducer=self.reducer_calc_prob)
        ]
    
    def mapper_multiply(self, key, value):
        category = key[0]
        word = key[1]

        if word in self.input_words:
            yield category, self.input_words[word] * value
        
    def reducer_calc_score(self, category, values):  
        yield None, (category, math.exp(sum(values) + self.multiplier))

    def reducer_calc_prob(self, _, values):
        v = list(values) #make a copy of the iterator as a list so we can loop twice
        transpose = zip(*v)
        total = sum(transpose[1])
        for value in v:
            yield value[0], value[1]/total





if __name__ == '__main__':
    #parse the bag of words for the review (stdin)
    for line in sys.stdin.readlines():
        (key, value) = JSONProtocol().read(line)
        Classifier.input_words[key[1]] = value
        
    # calculate the multiplier for the probability (for now, assume there are only 2 possible classes) (Also, we work in log scale to avoid overflow errors.)
    num_possible_classes = 2
    numer = math.log(math.factorial(sum(Classifier.input_words.itervalues())))
    denom = sum([math.log(math.factorial(n)) for n in Classifier.input_words.itervalues()])
    Classifier.multiplier = math.log(num_possible_classes) + numer - denom

    

    Classifier().run()
