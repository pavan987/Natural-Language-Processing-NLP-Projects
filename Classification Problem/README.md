The aim of this Project is to do authorship identification on lines of poetry written by Emily Bronte and William Shakespeare. We’ll be using the Naive Bayes classifier provided by nltk.

classify.py : This is an implementation of a Naive Bayes classifier that uses NLTK’s Naive Bayes code. It generates features from training data, evaluates on a small percentage of the training data, then re-trains on the full training data and generates predictions for the test data.

It is implemented with a following feature set to get the best Accuracy

1. Most Frequently Used words

This is a very important deciding factor for identifying the sentence belong to which author. I have collected all the words, sorted by their frequencies and collected 3000 most frequently used words. all these words will be acted as features to check if word is present or not.

2. Punctuations:-

I have observed that the usage of punctuation differs with each author. for example, Author Bronte used significantly higher exclamation marks compared to Shakespeare. Similar observations are done for other punctuations like comma, colon, apostrophes. So the feature set is to check if sentence contain these specific punctuations are not

3. Length of sentences:

It is observed that average length of Shakespeare sentences is higher than of Bronte. this is one of the key feature for classifier algorithm to identify.

4. First word-

The way, author starts his sentence differs. the starting word of each sentence is also a good distinguishing feature.

5. Normalization:-
This is not a feature. But removing all the punctuation marks  and splitting the tokens by space while using the data for unigrams or most frequent words or lemmatization will help the features to work properly.  
