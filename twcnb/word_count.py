"""A simple word count MRJob. Takes as input raw text and returns a list of the
words that occur in the text and their frequencies."""

from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol
from word_utils import words

class WordCount(MRJob):
    
    IMPORT_PROTOCOL = RawValueProtocol
    
    def mapper(self, _, text):
        for word in words(text):
            yield word, 1
            
    def reducer(self, word, occurences):
        yield word, sum(occurences)
        


if __name__ == '__main__':
    WordCount.run()
