import simplejson
from classifier import classify
from pyspark import SparkContext

input_path = "/home/jake/Dropbox/Projects/Sentiment Analysis/yelp_dataset/yelp_academic_dataset"
training_path = "/home/jake/Dropbox/Projects/Sentiment Analysis/my_data/training_test/part-00000"

sc = SparkContext("local","NBClassifier")

training_data = sc.textFile(training_path).map(simplejson.loads)

all_reviews = sc.textFile(input_path).map(simplejson.loads).filter(lambda datum: datum['type']=='review')

total = 330071
sample_size = 100

reviews = all_reviews.sample(False, float(sample_size)/float(total)).cache()


def categoryof(datum):
    if datum['stars'] > 3:
        return 'pos'
    else:
        return 'neg'

def textof(datum):
    return datum['text']



#reviews = sc.textFile(input_path)

def maxkey(item):
    return max(item.iterkeys(), key=lambda x: item[x])

guesses = map(maxkey, classify(reviews, training_data, textof))

actual = reviews.map(categoryof).collect()

testset = map(lambda x: 1 if x[0]==x[1] else 0 , zip(guesses, actual))

print float(sum(testset))/float(len(testset))
