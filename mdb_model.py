#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:13:52 2019

@author: juanflorez
"""

"""
Using the bayesian library, create a naive Bayesian model for the data
directory
"""

import bymodel as bym
import pickle
import os

path=("mdb_model")
train_path= "data/train"

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

full_dictionary ={}

total_neg = bym.build_full_dic(train_path+"/neg", full_dictionary)

print(total_neg)

total_positive = bym.build_full_dic(train_path+"/pos", full_dictionary)

print(total_positive)

f = open(path+"/dictionary.pkl","wb")
pickle.dump(full_dictionary,f)
f.close()

# Create a copy of full_dict to record the occurrence of each word in
# negative reviews

count_neg = dict(full_dictionary)

bym.count_words(train_path+"/neg", count_neg)

n = open(path+"/neg_count.pkl","wb")
pickle.dump(count_neg,n)
n.close()


# Create a copy of full_dict to record the occurrence of each word in
# positive reviews

count_pos = dict(full_dictionary)

bym.count_words(train_path+"/pos", count_pos)

p = open(path+"/pos_count.pkl","wb")
pickle.dump(count_pos,p)
p.close()

