#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:11:14 2019

@author: juanflorez
Bayesian model library
"""
from os import walk
from math import log

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


def single_w_c(word: str, w_count: dict, total_set: int):
    """
    Given a word 'w',  a dictionary with the count of words
    in the classification and the total set of words in the classification,
    return the probability that
    a word in the class is 'w' use total_set as denominator for normalisation
    P(w|c) = [[count(w in c)] + 1 ] / [(total words in c) + total_set]

    :word: the word  to evaluate
    :w_count: directory with the frequencies off all the words in the dictionary
    :total_set: the amount of words, used for normalization
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
    TODO: make it an array of directories to have different number of classes
    :root_path: Root directory, assumes it has one sub-directory per class
    :class_path: sub-directory of root, assumed to have all the documents of one class.
    :return: probability 0 <= p(d) <= 1
    """
    # total files in path
    total_files = sum([len(files) for r, d, files in walk(root_path)])
    
    # total files in target
    total_tg = sum([len(files) for r, d, files in walk(class_path)])
    
    return total_tg/total_files


def make_dic_w_c(dir_p_w_c, full_w_c):
    """
    Load the dictionaty dir_p_w_c, for each word (key) give the 
    ocurrences/total words in the class taken from full_wc[word].
    """
    total_set = sum(full_w_c.values())+len(full_w_c)
    for w in dir_p_w_c:
        dir_p_w_c[w] = (full_w_c[w]+1)/total_set


def prob_class_doc(document: str, dict_p_w_comp, p_c):
    """
    :return probability of the document to be in a class c given the dictionary of frequency probability and
    probability of a doc to be in a class c
    :document: string of words
    :dict_p_w_comp: dictionary with words as keys that store the frequency probability of the word inside the class
    normalized already
    Given a word w, what are the odds that it is in a document of class c?
    P(c|D) =  LOG P(c) + SUM(LOG(P(w|c)))
    """
    sum_of_log = 0
    for w in document.split(' '):
        try:
            sum_of_log += log(dict_p_w_comp[w])
        except KeyError:
            sum_of_log += 0

    return log(p_c) + sum_of_log
