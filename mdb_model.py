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

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

full_dictionary ={}

total_neg = bym.build_full_dic("data/trainSmall/neg", full_dictionary)

print(total_neg)

total_positive = bym.build_full_dic("data/trainSmall/pos", full_dictionary)

print(total_positive)

f = open(path+"/dictionary.pkl","wb")
pickle.dump(full_dictionary,f)
f.close()

# Create a copy of full_dict to record the occurrence of each word in
# negative reviews

count_neg = dict(full_dictionary)



