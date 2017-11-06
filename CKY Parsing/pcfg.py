from __future__ import print_function
import collections
import fileinput
from sets import Set
import math
import time
import argparse
import sys

# import numpy as np
# import matplotlib.pyplot as plt



def preorder(cky, label, i, j):
    print("(", end='')
    print(label+" ", end='')
    node = cky[i][j]
    k = node[label][1]
    sufix1 = node[label][2]
    sufix2 = node[label][3]
    if k != -1:
        # print("(", end='')
        preorder(cky, sufix1, i, k)
        # print(")", end='')
        # print("(", end='')
        preorder(cky, sufix2, k, j)
        print(")", end='')
        # print(")", end='')
    else:
        print(sufix2, end='')
        print(")", end='')

def main():
    parser = argparse.ArgumentParser(description="ignore input; make a demo grammar that is compliant in form",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # addonoffarg(parser, 'debug', help="debug mode", default=False)
    parser.add_argument("--gfile", "-g", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file (ignored)")
    parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="output file (grammar)")

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    reverserules = collections.defaultdict(set)
    # for line in fileinput.input():
    for line in args.gfile.readlines():
        tokens = line.strip().split(" ")
        key = " ".join(tokens[1:])
        value = tokens[0]
        reverserules[key].add(value)
    args.gfile.seek(0)
    rules={}
    for line in args.gfile.readlines():
        tokens = line.strip().split(" ")
        parentkey = tokens[0]
        childkey = " ".join(tokens[1:])
        hm = collections.defaultdict(int)
        if parentkey in rules:
            hm = rules[parentkey]
            hm[childkey]+=1
        else:
            hm[childkey] += 1
        rules[parentkey] = hm
    # print (rules)

    probs = {}
    for key, value in rules.items():
        ruleKey = key+" -> "
        total = 0.0
        for _, count in value.items():
            total += count
        for sufix, count in value.items():
            probs[ruleKey+sufix] = math.log10(count/total)
    # print (probs)
    # graph = open("graph","w")
    # x=[]
    # y=[]
    for sen in fileinput.input("dev.strings"):
        #sen="The flight should be eleven a.m tomorrow ."
        #print sen
        words = sen.strip().split(" ")
        # start_time = time.clock()
        cky=[]
        n = len(words)+1
        for i in range(n):
            temp =[]
            for j in range(n):
                temp.append({})
            cky.append(temp)

        # first the terminals
        for i,j in zip(range(n-1), range(1,n)):
            label=words[i]
            if words[i] not in reverserules:
                words[i] = "<unk>"
            for keyRule in reverserules[words[i]]:
                if keyRule not in cky[i][j]:
                    # print (probs[keyRule+" -> "+words[i]])
                    cky[i][j][keyRule]=(probs[keyRule+" -> "+words[i]], -1, words[i], label)
                else:
                    prob = cky[i][j][keyRule][0]
                    if prob < probs[keyRule+" -> "+words[i]]:
                        cky[i][j][keyRule]=(probs[keyRule+" -> "+words[i]], -1, words[i], label)
        # print cky
        for c in range(1, n):
            for i in range(n-1):
                j=i+c
                if j<n:
                    for k in range(i+1,n):
                        cell1 = cky[i][k]
                        cell2 = cky[k][j]
                        for item1 in cell1:
                            for item2 in cell2:
                                sufix = item1+" "+item2
                                if sufix in reverserules:
                                    for keyRule in reverserules[sufix]:
                                        nprob = probs[keyRule+" -> "+sufix]+cky[i][k][item1][0]+cky[k][j][item2][0]
                                        if keyRule in cky[i][j]:
                                            eprob = cky[i][j][keyRule][0]
                                            if eprob < nprob:
                                                cky[i][j][keyRule]=(nprob,k,item1,item2)
                                        else:
                                            cky[i][j][keyRule]=(nprob,k,item1,item2)
        #Q2 print (cky[0][n-1])
        if len(cky[0][n-1]) != 0:
            preorder(cky,"TOP", 0, n-1)

        #end_time = time.clock()
        # graph.write("{0} {1}".format(x,y))
        # print(x,y)
        # x.append(len(words))
        # y.append(time.clock()-start_time)
        print()
        # # for k in range(1,n):
            # for i,j in zip(range(n-1), range(k,n)):
            #     print cky[i][j]
    # for item1, item2 in zip(x,y):
    #     #graph.write(""+str(item1)+" "+str(item2)+"\n")
    #     # print (item1, item2)
    #     print (math.log(item1), math.log(item2*10000000))
    # plt.loglog(np.array(x),np.array(y), basex=np.e, basey=np.e)
    #plt.show()

if __name__ == '__main__':
  main()
