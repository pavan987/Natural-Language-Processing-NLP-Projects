from __future__ import division
from collections import defaultdict
from sets import Set
import sys,json,math
import os
import numpy as np

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.

    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1
    numerator=0.0
    den1=0.0
    den2=0.0
    for key,value in v1.items():
        if key in v2:
            numerator += value*v2[key]

    for key,value in v1.items():
        den1 += value*value
    for key,value in v2.items():
        den2 += value*value
    den = math.sqrt(den1) * math.sqrt(den2)
    if numerator ==0:
        return 0
    return numerator/den

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1
    # return np.sum(v1*v2)/math.sqrt(np.sum(v1**2)*np.sum(v2**2))
    return v1.dot(v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]
    result = []
    filterdict = {k:v for k,v in word_2_vec.items() if k not in exclude_w }
    for key, value in sorted(filterdict.items(), key=lambda (k,v): sim_metric(v,w_vec), reverse=True):
        result.append((key, sim_metric(value,w_vec)))
    #return [item for item in result if item[0] == "cake"]
    return result[:10]
