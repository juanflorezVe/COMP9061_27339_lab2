This is my "not perfect" lab 2.
It has three basic files:

bym_tests/model_test.py --> Tests the methods in bymodel.py model (TDD)
bymodel.py --> A generic set of methods to explore directories and calculate p(w|c) and p(c|W) assuming the docs are
               classified by directories.
mdb_model.py --> Using the utilities from bymodel.py, it generates the model using the data set, and then classifies the docs in test subdirectory.


Invoking it by time python3 mdb_model.py
======================================
total set of negative words 280617
total set of positive words 280617
total set of words 280617
total amount of words in negative docs 2885848
total amount of words in positive docs 2958832
total amount of words in all the docs 5844680
Probability of negative 0.499980000799968
Probability of positive 0.499980000799968
times it classified as negative 1898
times it classified as positive 104
accuracy of negatives 0.948051948051948
times it classified as positive 1240
times it classified as negative 760
accuracy of positives 0.62

real	0m34.431s
user	0m15.119s
sys	0m6.656s
======================================

