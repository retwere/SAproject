SAproject
=========

Sentiment Analysis Project

This is a project for performing sentiment analysis on the Yelp academic data set. 


Naive-Bayes
===========

#Classifying

To use the naive-Bayes classifier, use the following command line:
```sh
printf "review" | python naive-bayes/bag-of-words.py review.txt | python naive-bayes/nb-classifier.py trained.json
```
where `review.txt` is the review to classify, formatted as a single line of the form
```json
"review" <tab> "<text of review>"
```
and `trained.json` is the output of the trainer.
