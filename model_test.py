#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 13:41:41 2019

@author: juanflorez
"""
import bymodel as bym

# Create a adictionary of words key = word and amount

testPhrase = "the the a a a is a word words no"
targetDirectory = {"the":2, "a":4, "is":1, "word":1, "no":1, "words":1}

def test_build_read_word_dict():
    fileName = "input_test.txt"
    with open(fileName,"w") as outp:
        outp.write(testPhrase)
    word_dict = {}
    count = bym.read_word_dict(fileName, word_dict)
    assert(targetDirectory == word_dict)
    assert(count == 6)


test_build_read_word_dict()

