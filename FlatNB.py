from sets import Set
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from prettytable import PrettyTable
import string, sys
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
exclude = set(string.punctuation)

flatdata = []
flatlabels = []
testdata = []

with open(sys.argv[1],'rb') as f1:
	flatdata = f1.readlines()
with open(sys.argv[2],'rb') as f2:
	flatlabels = f2.readlines()
with open(sys.argv[3],'rb') as f3:
	testdata = f3.readlines()
flatdata = [''.join(ch for ch in i.strip('\n').lower() if ch not in exclude) for i in flatdata]
testdata = [''.join(ch for ch in i.strip('\n').lower() if ch not in exclude) for i in testdata]
flatlabels = [i.strip('\n') for i in flatlabels]

clf = LogisticRegression()
vec = CountVectorizer(stop_words="english")

flatdata = vec.fit_transform(flatdata, flatlabels)	
testdata = vec.transform(testdata)
clf.fit(flatdata, flatlabels)
pred = clf.predict(testdata)

f = open(sys.argv[4],'wb')
for row in pred:
	f.write(row+'\n')