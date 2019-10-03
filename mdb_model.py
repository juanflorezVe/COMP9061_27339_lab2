#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bymodel as bym
import pickle
import os

"""
Created on Wed Oct  2 11:13:52 2019

@author: juanflorez
"""

"""
Using the bayesian library, create a naive Bayesian model for the data
directory
"""

path = ("mdb_model")
train_path = "data/train"

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

full_dictionary = {}

total_neg = bym.build_full_dic(train_path+"/neg", full_dictionary)

print(total_neg)

total_positive = bym.build_full_dic(train_path+"/pos", full_dictionary)

print(total_positive)

f = open(path+"/dictionary.pkl", "wb")
pickle.dump(full_dictionary, f)
f.close()

# Create a copy of full_dict to record the occurrence of each word in
# negative reviews

count_neg = dict(full_dictionary)

total_neg = bym.count_words(train_path+"/neg", count_neg)

n = open(path+"/neg_count.pkl", "wb")
pickle.dump(count_neg, n)
n.close()


# Create a copy of full_dict to record the occurrence of each word in
# positive reviews

count_pos = dict(full_dictionary)

total_pos = bym.count_words(train_path+"/pos", count_pos)

p = open(path+"/pos_count.pkl", "wb")
pickle.dump(count_pos, p)
p.close()

# Create a new dictionary with the total of positives and negatives


count_total = {key: count_pos.get(key, 0) + count_neg.get(key, 0)
                for key in set(count_pos) | set(count_pos) | set(full_dictionary)
               }

total_words = len(count_total)

t = open(path+"/tot_count.pkl", "wb")
pickle.dump(count_total, t)
t.close()

all_words_positive = sum(count_pos.values())
all_words_negative = sum(count_neg.values())

print("total set of negative words {}".format(total_neg))
print("total set of positive words {}".format(total_pos))
print("total amount of words in negative docs {}".format(all_words_negative))
print("total amount of words in positive docs {}".format(all_words_positive))
print("total amount of words in all the docs {}".format(all_words_positive + 
      all_words_negative))
