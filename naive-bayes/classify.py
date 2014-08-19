"""A convenience runner for the naive Bayes classifier. (NOT WORKING)"""

import sys
import tempfile
from subprocess import check_output
from mrjob.protocol import JSONProtocol



def classify(review, trained_data):
    #make a temp file to store the review that can be passed to bag-of-words.py
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(JSONProtocol().write("review",review))

    return check_output("printf \"pos\"", shell=True) 
    #check_output("printf \"review\" | python naive-bayes/bag-of-words.py {} | python naive-bayes/nb-classifier.py {}".format(tmp.name,trained_data), shell=True)



if __name__ == '__main__':
    #read the text of the review from stdin
    review_text = "".join(sys.stdin.readlines())
    
    #the path to the training data is the first command line argument
    train_path = sys.argv[1]
    
    print classify(review_text, train_path)
