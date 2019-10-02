#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 13:41:41 2019

@author: juanflorez
"""
import bymodel as bym
import os

# Create a adictionary of words key = word and amount

testPhrase = "the the a a a is a word words no"
testPhrase2 = "some words are common others are not"

targetDictionary = {"the": 2, "a": 4, "is": 1, "word": 1, "no": 1, "words": 1}
targetWordBag = {"the": 0, "a": 0, "is": 0, "word": 0, "words": 0, "no": 0,
                 "some": 0, "are": 0, "common": 0, "others": 0, "not": 0}

path = "tmptestdir"
fileName1 = path+"/input_test1.txt"
fileName2 = path+"/input_test2.txt"


def create_test_data_directory():

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    with open(fileName1, "w") as fl1:
        fl1.write(testPhrase)

    with open(fileName2, "w") as fl2:
        fl2.write(testPhrase2)


def test_build_full_dictionary():
    """
    Given a folder, get all the words in the folder and
    make a dictionary initialized to 0
    """
    create_test_data_directory()

    word_bag = {}
    count = bym.build_full_dic(path, word_bag)
    assert(word_bag == targetWordBag)
    assert(11 == count)


def test_build_read_word_dict():
    """
    Create a file, build a dictionay
    """
    create_test_data_directory()
    word_dict = {}
    count = bym.count_word_dict(fileName1, word_dict)
    assert(targetDictionary == word_dict)
    assert(count == 6)


def test_count_words_in_directory():
    """
    given a directory, and a dictionary of words,
    record the occurrence of each word in all the files in the directory.
    """
    create_test_data_directory()
    counted_words = targetWordBag.copy()

    bym.count_words(path, counted_words)
    targetWordCount = {"the": 2, "a": 4, "is": 1, "word": 1, "words": 2,
                       "no": 1, "some": 1, "are": 2, "common": 1, "others": 1,
                       "not": 1}
    assert(counted_words == targetWordCount)
