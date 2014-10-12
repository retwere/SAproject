
import simplejson
from trainer import train
from pyspark import SparkContext

input_path = "/home/jake/Dropbox/Projects/Sentiment Analysis/yelp_dataset/yelp_academic_dataset"

sc = SparkContext("local", "NBTrainer")

all_reviews = sc.textFile(input_path).map(simplejson.loads).filter(lambda datum: datum['type']=='review')

total = 330071

sample_size = 100

training_data = all_reviews.sample(False, float(sample_size)/float(total))

def categoryof(datum):
    if datum['stars'] > 3:
        return 'pos'
    else:
        return 'neg'

def textof(datum):
    return datum['text']



output = train(training_data, categoryof, textof).map(
    lambda ((cat, word), p): (word, p if cat=='pos' else -p)
).reduceByKey(lambda x,y: x+y).collectAsMap()

output_text = simplejson.dumps(output)

print output_text
