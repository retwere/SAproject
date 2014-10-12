

#note: I would like to do word_count in a parallelized way, but that doesn't seem
#      to be possible in this version of pyspark. It's no big loss---each 
#      individual review shouldn't be very long.
from word_utils import word_count


def classify(reviews, training_data, textof = lambda x: x):
    """Give an estimated classification of the given reviews, according to the 
    provided training data.
    
    Arguments:
    reviews -- an RDD consisting of the reviews to be classified
    training_data -- the output of the train() function
    textof -- a function that returns the review text given a record of reviews

    Output: a list of dictionaries of the form {'cat1': score1, 'cat2': 
    score2, ...} indicating the scores for the various categories. The max score
    is the estimated category.
    """
    
    bags_of_words = reviews.map(textof).map(word_count).collect()

    output = []
    
    for bag in bags_of_words:
        output.append(
            training_data.map(
                lambda ((cat, wd), p): (cat, bag[wd]*p) if wd in bag else (cat, 0)
            ).reduceByKey(lambda x, y: x + y).collectAsMap()
        )
    
    return output
    
