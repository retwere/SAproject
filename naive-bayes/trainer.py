""" """


import math

from word_utils import words


def train(review_data, categoryof, textof, alpha = 1):
    """train: Return the training data for the given review data.

    Arguments:
    review_data -- an RDD of the consisting of the training data
    categoryof -- a function that returns the category of a record of
                  review_data
    textof -- a function that returns the review text given a record of
              review_data
    alpha -- the smoothing parameter (defaults to 1)

    Output: an RDD consisting of pairs ((C, W), P), where C is a category
    (string), W is a word (string) and P is the log-likelyhood estimate for the
    word W in category C (float).
    """

    #categorized_reviews = RDD of (C, T) pairs where C = category and T = text
    categorized_reviews = review_data.map(
        lambda x: (categoryof(x), textof(x))
    ).cache()

    #raw "bags of words"
    bags_of_words = categorized_reviews.flatMap(
        lambda (cat, text): [ ((cat, word), 1) for word in words(text) ]
    ).reduceByKey(lambda x, y: x + y)

    #a list of all possible distinct categories
    possible_categories = categorized_reviews.keys().distinct()

    #a list of all distinct words that occur in the corpus
    all_words = categorized_reviews.values().flatMap(words).distinct()

    #perform Laplace smoothing on the bags of words with parameter alpha. This
    #just means that we add "alpha" copies of each word to each bag.
    smoothed_bags_of_words = bags_of_words.union(
        possible_categories.cartesian(all_words).map(lambda x: (x, alpha))
    ).reduceByKey(lambda x, y: x + y).cache()
    
    #the total number of words in each bag
    totals = smoothed_bags_of_words.map(
            lambda ((cat, word), count): (cat, count)
        ).reduceByKey(lambda x, y: x + y).collectAsMap()
    
    #the estimates of the log-likelihood of each (category, word) pair
    log_likelihoods = smoothed_bags_of_words.map(
        lambda ((cat, word), count): ((cat, word), math.log(count/float(totals[cat])))
    ).cache()

    return log_likelihoods
