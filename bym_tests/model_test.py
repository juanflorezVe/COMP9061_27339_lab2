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
"""
Cloud Java Cloud
Comp
2
Cloud Cloud Spring
Comp
3
Cloud Software Java
Comp
4
Referendum Software Election
Politics
Test
5
Java Software Java Election


"""


@pytest.fixture
def doc1():  #Comp
    return "Cloud Java Cloud"

@pytest.fixture
def doc2():  #Comp
    return "Cloud Cloud Spring"

@pytest.fixture
def doc3():  #Comp
    return "Cloud Software Java"

@pytest.fixture
def doc4():  #Politics
    return "Referendum Software Election"

@pytest.fixture
def doc5():
    return "Java Software Java Election"

@pytest.fixture
def dict_univ():
    """
    Universal dictionary, all the words in all the documents of all
    classes
    """
    return {"Cloud": 0, "Spring": 0, "Software": 0, "Referendum": 0,
            "Java": 0, "Election": 0}

@pytest.fixture
def u_dict_w_count_comp():
    """
    Dictionay with all the universal words but having amount in comp class
    """
    return {"Cloud": 5, "Spring": 1, "Software": 1, "Referendum": 0,
            "Java": 2, "Election": 0}

@pytest.fixture
def u_dict_w_count_politics():
    """
    Dictionay with all the universal words but having amount in politics class
    """
    return {"Cloud": 0, "Spring": 0, "Software": 1, "Referendum": 1,
            "Java": 0, "Election": 1}

@pytest.fixture
def dict_w_count_comp():
    """
    Dictionay with the words in comp class
    """
    return {"Cloud": 5, "Spring": 1, "Software": 1,
            "Java": 2}

@pytest.fixture
def dict_w_count_politics():
    """
    Dictionay with all the words in politics class
    """
    return {"Software": 1, "Referendum": 1, "Election": 1}

@pytest.fixture
def total_words_politics(u_dict_w_count_politics):
    return sum(u_dict_w_count_politics.val())

@pytest.fixture
def total_words_comp(u_dict_w_count_comp):
    return sum(u_dict_w_count_comp.val())

# """ These are constant and are easy to keep just like this """"

path = "exmpleTest"
path_comp = path+"/comp"
path_pol = path+"/pol"

fileComp1 = path_comp+"/comp_test1.txt"
fileComp2 = path_comp+"/comp_test2.txt"
fileComp3 = path_comp+"/comp_test3.txt"
filePol1  = path_pol+"/pol_test1.txt"

# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@pytest.fixture
def mk_dat(doc1, doc2, doc3, doc4):
    """
    Make the test data:
    all the folders and files
    """
    try:
        os.mkdir(path)
        os.makedirs(path_comp)
        os.makedirs(path_pol)
    except OSError:
        print("Creation of the directory {} failed ".format(OSError))
    else:
        print("Successfully created the directory %s " % path)

    with open(fileComp1, "w") as fl1:
        fl1.write(doc1)

    with open(fileComp2, "w") as fl2:
        fl2.write(doc2)
        
    with open(fileComp3, "w") as fl3:
        fl3.write(doc3)
 
    with open(filePol1, "w") as fl4:
        fl4.write(doc4)


def test_build_full_dictionary(mk_dat, dict_w_count_comp):
    """
    Given a folder, get all the words in all the docs in the folder and
    make a dictionary initialized to 0
    """
    comp_word_bag = {}
    count = bym.build_full_dic(path_comp, comp_word_bag)
    assert(comp_word_bag == dict.fromkeys(dict_w_count_comp, 0))
    assert(4 == count)


def test_build_read_word_dict(mk_dat, dict_univ):
    """
    Count the words in a document and update the dictionary
    """
    word_dict = dict_univ.copy()
    fileComp1_dict = {"Cloud": 2, "Spring": 0, "Software": 0,
            "Referendum": 0, "Java": 1, "Election": 0}
    count = bym.count_word_dict(fileComp1, word_dict)
    assert(fileComp1_dict == word_dict)
    assert(count == 6)


def test_count_words_in_directory(mk_dat, dict_univ, 
                                  u_dict_w_count_comp):
    """
    given a directory, and a dictionary of words,
    record the occurrence of each word in all the files in the directory.
    """
    counted_words = dict_univ.copy()  #Always create a copy 

    total_words = bym.count_words(path_comp, counted_words)
 
    assert(counted_words == u_dict_w_count_comp)
    assert(total_words == len(counted_words))
    

def test_prob_word_given_class(u_dict_w_count_comp, dict_univ):
    """
    Given a word, and a class, calculate the number p; 0 <= p <= 1
    count of appearences of w in all the docs in c, over the total
    amount of words in c.
    P(w|c) = count_of(w) / total of words in c
    """

    denom_normal = len(dict_univ)
    p = bym.single_w_c("Java", u_dict_w_count_comp, denom_normal)
    manual_calc = ( u_dict_w_count_comp["Java"] + 1) / (sum(u_dict_w_count_comp.values()) + denom_normal)
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
    
    p = bym.prob_class(path, path_comp)
    assert(3/4 == p)
    
    
def test_make_dic_w_c(dict_univ, u_dict_w_count_comp):
    """
    P(w|c) for each word in the dictionary, for the given class
    """
    dir_p_w_c = dict_univ.copy()
    total_w_comp = sum(u_dict_w_count_comp.values())
    total_w_univ = len(dict_univ)
    denom = total_w_univ + total_w_comp
    assert(denom == 15)  # from the lecture's example
    target_prob = {"Cloud": (5+1)/denom, "Spring": (1+1)/denom, 
                   "Software": (1+1)/denom, "Referendum": (0+1)/denom,
                    "Java": (2+1)/denom, "Election": (0+1)/denom}
    
    bym.make_dic_w_c(dir_p_w_c,  u_dict_w_count_comp)  #Refactor
    assert(dir_p_w_c == target_prob)