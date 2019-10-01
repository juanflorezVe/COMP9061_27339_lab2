#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:11:14 2019

@author: juanflorez
Bayesian model library
"""

def read_word_dict(fileName, word_dict):
    """
    given a fileName, add the words to word_dict
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

