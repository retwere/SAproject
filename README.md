#SAproject

Sentiment Analysis Project

This is a project for performing sentiment analysis on the Yelp academic data set. 


##Preprocessing

Process the dataset from Yelp into a format that we can easily use. 


##Naive-Bayes

###Training

To train the naive-Bayes classifier, first calculate the "bag of words" using the following command line:
```sh
printf "pos\nneg" | python naive-bayes/bag-of-words.py preprocessed.json > bag.json
```
where `pos` and `neg` are the categories, `preprocessed.json` is the preprocessed dataset, and `bag.json` is the output file.

Then we run the trainer to calculate the "word scores" (these are the log-estimates of the probabilities p_i). Use this command line:
```sh
python naive-bayes/counter.py bag.json | python naive-bayes/trainer.py bag.json > trained.json
```
where `bag.json` is the "bag of words" from the previous command and `trained.json` is the output file.

###Classifying

To use the naive-Bayes classifier, use the following command line:
```sh
printf "review" | python naive-bayes/bag-of-words.py review.txt | python naive-bayes/nb-classifier.py trained.json
```
where `review.txt` is the review to classify, formatted as a single line of the form
```json
"review" <tab> "<text of review>"
```
and `trained.json` is the output of the trainer.
