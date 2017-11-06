#!/usr/bin/env python

import sys, fileinput
import collections
import tree

def preorder(root):
    rule=""
    if root.children:
        rule = root.label+" "
        for i in root.children:
            if len(root.children) == 2:
                rule += i.label+" "
            else:
                rule += i.label+" "
        print rule
        for i in root.children:
            preorder(i)

trees = []
for line in fileinput.input():
    t = tree.Tree.from_str(line)
    preorder(t.root)
