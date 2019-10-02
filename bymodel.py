#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:11:14 2019

@author: juanflorez
Bayesian model library
"""
from os import walk


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

            print(tmp_words)
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
    print("start the loop")
    for f in files:
        tmp_words = set(open(path+"/"+f).read().split())
        word_set = word_set.union(word_set, tmp_words)
        print(word_set)

    word_bag.update(dict.fromkeys(word_set, 0))

    return len(word_bag)
