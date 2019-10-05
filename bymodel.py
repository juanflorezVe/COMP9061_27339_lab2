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


def count_word_document(fileName, word_dict):
    """
    Given a fileName, add the words to word_dict
    TODO: improve resilience, and handle exceptions
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


def load_count_dict(path, count_words):
    """
    Given a path and a dictionary of words, count all the occurrences of the
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


def single_w_c(word, w_count: dict, total_set: int):
    """
    Given a word 'w', a classification  a dictionary with the count of words
    in the classification and the total set of words in the class, 
    return the probability that
    a word in class is 'w' use total_set as denominator for normalisation 
    
    P(w|c) = [[count(w in c)] + 1 ] / [(total words in c) + total_set]
    
    """
    return (w_count[word]+1 )/(sum(w_count.values()) + total_set)

    
def prob_class(root_path, class_path): 
    """
    out off all the documents D, what are the odds that a document d belongs
    to a class c
    P(c) = total(c)/total(D)
    assume the model has directories per class, so the probability is the total
    of files in the class\' directory over total of documents in all
    directories
    """
    #total files in path
    total_files = sum([len(files) for r, d, files in walk(root_path)])
    
    #total files in target
    total_tg = sum([len(files) for r, d, files in walk(class_path)])
    
    return total_tg/total_files



def make_dic_w_c(dir_p_w_c, full_w_c):
    """
    Load the dictionaty dir_p_w_c, for each word (key) give the 
    ocurrences/total words in the class.
    """
    total_set = sum(full_w_c.values())+len(full_w_c)
    for w in dir_p_w_c:
        dir_p_w_c[w] = (full_w_c[w]+1)/total_set



def prob_w_c(word: str, _class: classification):
    """
    Given a word w, what are the odds that it is in a document of class c?
    P(c|w) =  LOG P(c) + SUM(LOG(P(w|c)))
    """
    pass
