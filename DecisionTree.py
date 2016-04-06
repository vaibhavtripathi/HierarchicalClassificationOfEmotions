from sets import Set
import sys
import string
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from prettytable import PrettyTable
from sklearn import tree
from sklearn.externals.six import StringIO 
import pydot

cv = CountVectorizer(stop_words="english")
exclude = set(string.punctuation)

datafile = 'train_data.txt'
labelfile = 'train_labels.txt'
testdatafile = 'test_data.txt'
testlabelsfile = 'test_labels.txt'

traindata = []
testdata = []
trainlabels = []
testlabels = []

with open(datafile) as f:
	for line in f:
		line = ''.join(ch for ch in line if ch not in exclude)
		traindata.append(line.strip('\n'))

with open(testdatafile) as f:
	for line in f:
		line = ''.join(ch for ch in line if ch not in exclude)
		testdata.append(line.strip('\n'))

with open(labelfile) as f:
	for line in f:
		trainlabels.append(line.strip('\n'))

with open(testlabelsfile) as f:
	for line in f:
		testlabels.append(line.strip('\n'))

X = cv.fit_transform(traindata, trainlabels)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, trainlabels) 

'''for key,value in cv.vocabulary_.iteritems():
	print key, value'''

dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data, max_depth=3) 
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
graph.write_pdf("emot.pdf")

pred = clf.predict(cv.transform(testdata))
outfile = open('pred.txt','w')
for label in pred:
	outfile.write(label+'\n')
