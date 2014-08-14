"""Process reviews into positive or negative by a simple heuristic."""

from preprocessor import Preprocessor

def categorize(_, data):
    """A review is considered positive if its star rating is 4 or more."""
    if data['stars'] >= 4:
        return 'pos'
    else:
        return 'neg'

if __name__ == '__main__':
    Preprocessor.categorize = categorize
    Preprocessor().run()

