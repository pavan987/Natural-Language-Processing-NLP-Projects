#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter
from nltk.corpus import stopwords
from nltk.util import ngrams
import nltk
import string
import codecs
import sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

all_words = []
kTOKENIZER = TreebankWordTokenizer()

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

class FeatureExtractor:
    def __init__(self,fh):
        self.punc = "!,':"
        all_words=[]
        datafile = reader(fh)
        datadict = DictReader(datafile, delimiter='\t')
        for ii in datadict:
            text = ii['text'].translate(None, string.punctuation)
            words = ii['text'].split(" ")
            # words = [w for w in words if not w in stopwords.words('english')]
            for word in words:
                all_words.append(morphy_stem(word))
        all_words = nltk.FreqDist(all_words)
        #print len(all_words)
        self.word_features = list(all_words.keys())[:3000]
        #print self.word_features
        fh.seek(0)
        """
        You may want to add code here
        """

    def features(self, text):
        d = defaultdict(int)

        # check punctuation
        for p in self.punc:
            d['punc'+p] = (p in text)

        # remove punctuation
        text = text.translate(None, string.punctuation)
        tokens = text.split(" ")

        m=[]
        for ii in tokens:
            m.append(morphy_stem(ii))

        # pos
        # pos = nltk.pos_tag(m)
        # d['pos'] = ""
        # for i in pos:
        #     d['pos'] += i[1]+" "

        #len
        d['length']=len(text)

        # most frequently used words
        for word in self.word_features:
            d[word]= (word in m)

        #filtered_words = [w for w in m if not w in stopwords.words('english')]

        #unigrams
        for ii in m:
            d[ii] += 1
        #
        # bigrams=ngrams(m,2)
        # for ii in bigrams:
        #     d[ii] += 1
        #
        # trigrams =ngrams(m,3)
        # for ii in trigrams:
        #     d[ii] += 1
        #
        # first word
        d['first']=m[0]
        #d['last']=tokens[len(tokens)-1]

        #print d
        return d
reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
    parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this fraction of total')
    args = parser.parse_args()
    trainfile = prepfile(args.trainfile, 'r')
    if args.testfile is not None:
        testfile = prepfile(args.testfile, 'r')
    else:
        testfile = None
    outfile = prepfile(args.outfile, 'w')

    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor(args.trainfile)

    # Read in training data
    train = DictReader(trainfile, delimiter='\t')
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['text'])
        #print feat
        if int(ii['id']) % 5 == 0:
            dev_test.append((feat, ii['cat']))
        else:
            dev_train.append((feat, ii['cat']))
        full_train.append((feat, ii['cat']))

    # Train a classifier
    sys.stderr.write("Training classifier ...\n")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))
    if testfile is None:
        sys.stderr.write("No test file passed; stopping.\n")
    else:
        # Retrain on all data
        classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

        # Read in test section
        test = {}
        for ii in DictReader(testfile, delimiter='\t'):
            test[ii['id']] = classifier.classify(fe.features(ii['text']))

        # Write predictions
        o = DictWriter(outfile, ['id', 'pred'])
        o.writeheader()
        for ii in sorted(test):
            o.writerow({'id': ii, 'pred': test[ii]})
