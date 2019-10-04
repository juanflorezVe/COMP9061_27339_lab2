#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 13:41:41 2019

@author: juanflorez
"""
import bymodel as bym
import os
import pytest

# Create a adictionary of words key = word and amount


@pytest.fixture
def docClass1():
    return "the the a a a is a word words no"

@pytest.fixture
def docClass2():
    return "some words are common others are not"

w_count_c1 = {"the": 2, "a": 4, "is": 1, "word": 1, "no": 1, "words": 1}

@pytest.fixture
def w_count_c2():
    return {"some": 1, "words": 1, "are": 2, "common": 1, "others":1, "not":1,
            "the": 0, "a": 0, "is": 0, "word": 0, "no": 0 }

@pytest.fixture
def fullNegDictionary():
    return {"some": 0, "words": 0, "are": 0, "common": 0,
              "others":0, "not":0 }
    
@pytest.fixture
def fullDictionary():
    return {"the": 0, "a": 0, "is": 0, "word": 0, "words": 0, "no": 0,
                 "some": 0, "are": 0, "common": 0, "others": 0, "not": 0}

@pytest.fixture
def total_w():
    return 11

# """ These are constant and are easy to keep just like this """"

path = "temptest"
path_pos = path+"/pos"
path_neg = path+"/neg"

filePos1 = path_pos+"/input_test1.txt"
fileNeg1 = path_neg+"/input_test2.txt"
filePos2 = path_pos+"/input_test3.txt"

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def create_test_data_directory(docClass1, docClass2):

    try:
        os.mkdir(path)
        os.makedirs(path_pos)
        os.makedirs(path_neg)
    except OSError:
        print("Creation of the directory {} failed ".format(OSError))
    else:
        print("Successfully created the directory %s " % path)

    with open(filePos1, "w") as fl1:
        fl1.write(docClass1)

    with open(fileNeg1, "w") as fl2:
        fl2.write(docClass2)
    
    with open(filePos2, "w") as fl3:
        fl3.write("")


def test_build_full_dictionary(docClass1, fullNegDictionary, docClass2):
    """
    Given a folder, get all the words in the folder and
    make a dictionary initialized to 0
    """
    create_test_data_directory(docClass1, docClass2)

    neg_word_bag = {}
    count = bym.build_full_dic(path_neg, neg_word_bag)
    assert(neg_word_bag == fullNegDictionary)
    assert(6 == count)


def test_build_read_word_dict(docClass1, docClass2):
    """
    Count the words in a document and update the dictionary
    """
    create_test_data_directory(docClass1, docClass2)
    word_dict = {}
    count = bym.count_word_dict(filePos1, word_dict)
    assert(w_count_c1 == word_dict)
    assert(count == 6)


def test_count_words_in_directory(docClass1, fullDictionary, docClass2):
    """
    given a directory, and a dictionary of words,
    record the occurrence of each word in all the files in the directory.
    """
    create_test_data_directory(docClass1, docClass2)
    counted_words = fullDictionary.copy()  #Always create a copy 

    total_words = bym.count_words(path_neg, counted_words)
    targetWordCount = {"the": 0, "a": 0, "is": 0, "word": 0, "words": 1,
                       "no": 0, "some": 1, "are": 2, "common": 1, "others": 1,
                       "not": 1}
    assert(counted_words == targetWordCount)
    assert(total_words == 11)


def test_prob_word_given_class(docClass1, w_count_c2, total_w):
    """
    Given a word, and a class, calculate the number p; 0 <= p <= 1
    count of appearences of w in all the docs in c, over the total
    amount of words in c.
    
    """

    class2 = bym.classification("class2")
    assert(class2.name == "class2")
    
    p = bym.single_w_c("common", w_count_c2, total_w)
    manual_calc = ( w_count_c2["common"] + 1) / (sum(w_count_c2.values()) + total_w)
                 
                 
    assert(manual_calc == p)

def test_prob_c():
    """
    out off all the documents D, what are the odds that a document d belongs
    to a class c
    P(c) = total(c)/total(D)
    assume the model has directories per class, so the probability is the total
    of files in the class\' directory over total of documents in all
    directories
    
    """
    
    p = bym.prob_class(path, path_pos)
    assert(2/3 == p)


def test_make_dic_w_c(fullDictionary, w_count_c2):
    """
    P(w|c) for each word in the dictionary, for the given class
    """
    neg_prob = fullDictionary.copy()
    target_prob = {"the": 0, "a": 0, "is": 0, "word": 0, "no": 0,
                   "some": 1/7, "words": 1/7, "are": 2/7, "common": 1/7,
                   "others":1/7, "not":1/7 }
    
    bym.make_dic_w_c(neg_prob,  w_count_c2, 7)
    assert(neg_prob == target_prob)

def test_prob_w_c():
    """
    Given a word w, what are the odds that it is in a document of class c?
    """
    negative = bym.classification("negative doc")
    pwn = bym.prob_w_c("common", negative)
    
    assert(1 == pwn)