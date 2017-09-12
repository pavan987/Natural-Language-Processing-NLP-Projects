#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

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

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        num_result = 0
        word = word.lower()
        if word in self._pronunciations:
            w_prons = self._pronunciations[word]
            i=0
            for w in w_prons:
                count =0
                for l in w:
                    if l[-1].isdigit():
                        count+=1
                if i==0:
                    num_result = count
                if count < num_result:
                    num_result = count
                i+=1
            return num_result
        else:
            return 1


    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        result = False
        a = a.lower()
        b = b.lower()
        # get the pronunciation from dictionary
        if a in self._pronunciations and b in self._pronunciations:
            a_pron = self._pronunciations[a]
            b_pron = self._pronunciations[b]
            for i in a_pron:
                for j in b_pron:
                    indexi=0
                    indexj=0
                    leni = len(i)
                    lenj = len(j)
                    # check for first occurance of vowels
                    while(indexi < leni and not (i[indexi][-1].isdigit())):
                        indexi += 1
                    while(indexj < lenj and not (j[indexj][-1].isdigit())):
                        indexj += 1
                    l = leni-1
                    k = lenj-1
                    rhyme=True
                    # set i = larger word and j = smaller word
                    while(k >= indexj and l>= indexi):
                        if j[k] != i[l]:
                            rhyme=False
                            break
                        k -= 1
                        l -= 1
                    if rhyme:
                        return True
        return result


    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        lines = text.strip().translate(None, punctuation.replace("'","")).lower().split("\n")
        lines = [s for s in lines if s]
        # check if poem has 5 lines
        if len(lines) == 5:
            words = []
            # split lines in to words
            for i in xrange(0,5):
                words.append(word_tokenize(lines[i]))
            count =[]
            # store count of syllables and check if count < 4
            for sen in words:
                c=0
                for word in sen:
                    c += self.num_syllables(word)
                count.append(c)
                if c < 4:
                    return False
            # check if difference of count of syllables between lines is proper
            if (abs(count[0]-count[1]) > 2) or (abs(count[1]-count[4]) > 2) or (abs(count[0]-count[4]) > 2) or (abs(count[2]-count[3]) > 2):
                return False
            # Find min num of syllables in A lines
            min=0
            if count[0]<count[1]:
                if count[0] < count[4]:
                    min = count[0]
                else:
                    min = count[4]
            else:
                if count[1] < count[4]:
                    min = count[1]
                else:
                    min = count[4]
            # check if b lines syllables less than a lines
            if count[2]>min or count[3]>min :
                return False
            # check if rhymes
            if (self.rhymes(words[0][-1], words[1][-1]) and self.rhymes(words[0][-1], words[4][-1]) and self.rhymes(words[1][-1], words[4][-1])
            and self.rhymes(words[2][-1], words[3][-1]) and (not self.rhymes(words[1][-1], words[2][-1])) and (not self.rhymes(words[0][-1], words[2][-1]))):
                return True
            else:
                return False
        return False

    def apostrophe_tokenize(self, text):
        words=word_tokenize(text)
        i = len(words)-1
        while i >= 0:
            if "'" in words[i]:
                words[i-1]=words[i-1]+words[i]
                words[i]=""
                i-=1
            i-=1
        return words

    def guess_syllables(self, word):
        vowels = ["a","e","i","o","u","y"]
        i=0
        count=0
        vowel =False
        consonant=True
        while i < len(word):
            if word[i] not in vowels:
                consonant = True
                vowel = False
            if word[i] in vowels:
                if consonant == True:
                    count+=1
                vowel = True
                consonant = False
            i+=1
        return count


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
