#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:11:14 2019

@author: juanflorez
Bayesian model library
"""
from os import walk

class classification():

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return ("Class {}".format(self.name))

        

def count_word_dict(fileName, word_dict):
    """
    Given a fileName, add the words to word_dict
    TODO: improve resialance, and handle exceptions
    """
    with open(fileName, "r") as fl:
        line_buffer = fl.readlines()
        for l in line_buffer:
            tmp_words = l.split(' ')

            for w in tmp_words:
                if w not in word_dict.keys():
                    word_dict[w] = 1
                else:
                    word_dict[w] += 1

    return len(word_dict)


def build_full_dic(path, word_bag):
    """
    Given a path to a directory, get the set of all words in the directory
    and store them in word_bag dictionary
    """
    # build a list of files
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    word_set = set()
#   print("start the loop")
    for f in files:
        tmp_words = set(open(path+"/"+f).read().split())
        word_set.update(dict.fromkeys(tmp_words))
#       print("{} processed ".format(f))

    word_bag.update(dict.fromkeys(word_set, 0))

    return len(word_bag)


def count_words(path, count_words):
    """
    Given a path and a dictionary of words, count all the ocurrence of the
    words in the directory. if a word is in a file, but not in the directory,
    it gets added.
    """
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break

    for f in files:
        print(f)
        tmp_words = open(path+"/"+f).read().split()

        for w in tmp_words:
            if w not in count_words.keys():
                count_words[w] = 1
            else:
                count_words[w] += 1
        print("finished {}".format(f))

    return len(count_words)  # should'n change... (?)


def prob_of_word(word, w_count: dict):
    """
    Given a word, a classification and a dictionary with the count of words
    in the classification, return the probability that a word in class is the
    that word 
    
    P(w|c) = [count(w in c)] / (total words in c)
    
    """
    return w_count[word]/sum(w_count.values())
    
    return 1