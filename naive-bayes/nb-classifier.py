"""This attempts to classify a review based on the training data. It takes into 
stdin the 'bag of words' of the review, and as the first argument the path to 
the file containing the output of nb-trainer.py.

The output will be the most likely category for the review text. (By not caring
about the actual probability, we make the calculation simpler.)"""

import sys
import math

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.protocol import RawValueProtocol
from mrjob.step import MRStep


class Classifier(MRJob):
    """"""
    
    INPUT_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    input_words = {}

    #The multiplier is irrelevant if we assume each class is equally likely
    #multiplier = 0
    
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper_multiply,
                   reducer=self.reducer_calc_score),
            MRStep(reducer=self.reducer_max)
        ]
    
    def mapper_multiply(self, key, value):
        category = key[0]
        word = key[1]

        if word in self.input_words:
            yield category, self.input_words[word] * value
        
    def reducer_calc_score(self, category, values):  
        yield None, (category, sum(values))

    def reducer_max(self, _, values):
        v = list(values) #make a copy of the iterator as a list so we can loop twice
        transpose = zip(*v)
        i = v.index(max(v)) #find the position of the max score
        yield '', v[i][0] #return the category corresponding to the max score




if __name__ == '__main__':
    #parse the bag of words for the review (stdin)
    for line in sys.stdin.readlines():
        (key, value) = JSONProtocol().read(line)
        Classifier.input_words[key[1]] = value
        

    Classifier().run()
