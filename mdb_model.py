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

path = "mdb_model"
train_path = "data/train"
test_path = "data/test"

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

neg_dictionary = {}
pos_dictionary = {}

total_neg = bym.load_count_dict(train_path+"/neg", neg_dictionary)

print(total_neg)

total_positive = bym.load_count_dict(train_path+"/pos", pos_dictionary)

print(total_positive)

univ_dict = {**neg_dictionary, **pos_dictionary}

print(len (univ_dict))

f = open(path+"/dictionary.pkl", "wb")
pickle.dump(univ_dict, f)
f.close()

# Create a copy of the universal dictionary  to record the occurrence of each word in
# negative reviews

count_neg_dict = dict(univ_dict)

total_neg = bym.load_count_dict(train_path + "/neg", count_neg_dict)

n = open(path+"/neg_count.pkl", "wb")
pickle.dump(count_neg_dict, n)
n.close()


# Create a copy of full_dict to record the occurrence of each word in
# positive reviews

count_pos_dict = dict(univ_dict)

total_pos = bym.load_count_dict(train_path + "/pos", count_pos_dict)

p = open(path+"/pos_count.pkl", "wb")
pickle.dump(count_pos_dict, p)
p.close()

# Create a new dictionary with the total of positives and negatives


count_total = {key: pos_dictionary.get(key, 0) + neg_dictionary.get(key, 0)
                for key in set(pos_dictionary) | set(neg_dictionary) | set(univ_dict)
               }

total_words = len(count_total)

t = open(path+"/tot_count.pkl", "wb")
pickle.dump(count_total, t)
t.close()

all_words_positive = sum(pos_dictionary.values())
all_words_negative = sum(neg_dictionary.values())

print("total set of negative words {}".format(total_neg))
print("total set of positive words {}".format(total_pos))
print("total set of words {}".format(len(univ_dict)))
print("total amount of words in negative docs {}".format(all_words_negative))
print("total amount of words in positive docs {}".format(all_words_positive))
print("total amount of words in all the docs {}".format(all_words_positive + 
      all_words_negative))


# ===============================================================
#
# ===============================================================

neg_prob = bym.prob_class(train_path, train_path+"/neg")
print("Probability of negative {}".format(neg_prob))

pos_prob = bym.prob_class(train_path, train_path+"/pos")
print("Probability of positive {}".format(neg_prob))

dict_w_prob_pos = univ_dict.copy()
dict_w_prob_neg = univ_dict.copy()

# build the directory with the probability for each word given positive doc
bym.make_dic_w_c(dict_w_prob_pos, count_pos_dict)
# build the directory with the probability for each word given negative doc
bym.make_dic_w_c(dict_w_prob_neg, count_neg_dict)

# =================================================================
# go through all the test/neg and check if it was assert as negative or not.

neg_test_files = []
for (dirpath, dirnames, filenames) in os.walk(test_path+"/neg"):
    neg_test_files.extend(filenames)
    break
good_class = 1
bad_class= 1

for fl in neg_test_files:
    with open(test_path+"/neg/"+fl, "r") as f:
        docum = f.read()

    prob_neg = bym.prob_class_doc(docum, dict_w_prob_neg, 0.5)
    prob_pos = bym.prob_class_doc(docum, dict_w_prob_pos, 0.5)
    if prob_neg > prob_pos:
        good_class += 1
    else:
        bad_class += 1
print("times it classified as negative {}".format(good_class))
print("times it classified as positive {}".format(bad_class))

print("accuracy of negatives {}".format(good_class/(good_class + bad_class)))

