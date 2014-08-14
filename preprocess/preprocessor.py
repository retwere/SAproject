"""This is a general preprocessor for transforming the raw academic dataset
into a form that is usable by our various training programs. It needs as
input:
    * the path to the dataset 
    * a function "categorize" which analyzes a review and determines its
      category.

The output will be a list of items of the form (category, text)"""

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


#Note: This doesn't really need to be mapreduce, but I'm doing it this way to use
#      mrjob's JSON protocol.

class Preprocessor(MRJob):
    """This class is the generic preprocessor for the dataset."""

    INPUT_PROTOCOL = JSONValueProtocol
    categorize = lambda x: ''

    def mapper(self, _, data):
        """Walk through every review, and yield its category and text."""
        if data['type'] == 'review':
            yield self.categorize(data), data['text']

    def reducer(self, category, reviews):
        for review in reviews:
            yield category, review
