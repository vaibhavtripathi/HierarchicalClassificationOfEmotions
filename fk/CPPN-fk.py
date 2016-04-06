from sets import Set
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from prettytable import PrettyTable
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import string, sys
exclude = set(string.punctuation)

class ClassifierPerParentNode:

	#HIERARCHY

	leaves = []
	inodes = []

	#FOR HIERARCHICAL CONSISTENCY 
	parent = dict()
	ancestor_set = dict()

	with open(sys.argv[1],'r') as hfile:
		for line in hfile:
			if '#' not in line:
				line = line.strip('\n')
				if ':' in line or ('IN' in line and len(line.split()) < 2):
					if 'IN' in line:
						inodes = line.split(':')
						for i in inodes:
							parent[i] = ''
					else:
						leaves = line.split(':')
						for l in leaves:
							parent[l] = ''	
				else:
					if len(line.split()) > 1:
						if line.split()[0] != 'root':
							if line.split()[0] not in leaves and line.split()[0] not in inodes:
								print 'Inconsistent hierarchy in '+ sys.argv[1] +'. Uninitialized element '+ line.split()[0] +'. Aborting...'
								sys.exit(0)
						if line.split()[1] != 'root':		
							if line.split()[1] not in leaves and line.split()[1] not in inodes:
								print 'Inconsistent hierarchy in '+ sys.argv[1] +'. Uninitialized element '+ line.split()[1] +'. Aborting...'
								sys.exit(0)
						parent[line.split()[0]] = line.split()[1]
	
	for key, value in parent.iteritems():
		print key, value

	for leaf in leaves:
		ancestor_set[leaf] = [parent[leaf]]
		currnode = parent[leaf]
		if currnode == 'root':
			continue
		while parent[currnode] != 'root':
			ancestor_set[leaf].append(parent[currnode])
			currnode = parent[currnode]
	
	#ALL CLASSIFIERS
	clfclasses = dict()
	for node in inodes+['root']:
		clfclasses[node] = []

	for node in inodes+['root']:
		for key, value in parent.iteritems():
			if value == node:
				clfclasses[node].append(key)

	for key in clfclasses.keys():
		if len(clfclasses[key]) < 2:
			print 'Improper hierarchy in '+ sys.argv[1] +'. Not enough children. Aborting...'
			sys.exit(0)

	#CLASSIFIER
	clfs = {}
	X = {}
	y = {}
	vec = {}

	for label in clfclasses.keys():
		clfs[label] = LinearSVC()
		vec[label] = CountVectorizer(stop_words="english")
		X[label] = []
		y[label] = []

	#TRAIN CLASSIFIER
	def train(self, datafile, labelfile):
		with open(datafile,'rb') as f1:
			flatdata = f1.readlines()
		with open(labelfile,'rb') as f2:
			flatlabels = f2.readlines()
		flatdata = [''.join(ch for ch in i.strip('\n').lower() if (ch.isalpha() or ch==' ')) for i in flatdata]
		flatlabels = [i.strip('\n') for i in flatlabels]

		#DUPLICATE SAMPLES FOR HIERARCHICAL CONSISTENCY
		data = flatdata
		labels = flatlabels
		for i in range(len(flatlabels)):
			for label in self.ancestor_set[flatlabels[i]]:
				data.append(flatdata[i])
				labels.append(label)

		for label in self.clfclasses.keys():		
			for i in range(len(labels)):
				if labels[i] in self.clfclasses[label]:
					self.X[label].append(data[i])
					self.y[label].append(labels[i])

		#TRAINING
		for label in self.clfclasses.keys():
			print 'Training for classifier '+label+' complete.' 
			self.X[label] = self.vec[label].fit_transform(self.X[label], self.y[label])	
			self.clfs[label].fit(self.X[label], self.y[label])

	#TEST CLASSIFIER
	def	predict(self, datafile):
		print 'Predicting labels...'
		predicted = []
		testdata = []
		with open(datafile,'rb') as f1:
			for line in f1:
				line = line.strip('\n').lower()
				line = ''.join(ch for ch in line if (ch.isalpha() or ch==' '))
				testdata.append(line)
		
		for i in range(len(testdata)):
			pred = self.clfs['root'].predict(self.vec['root'].transform([testdata[i]]).toarray())[0]
			while pred not in self.leaves:
				pred = self.clfs[pred].predict(self.vec[pred].transform([testdata[i]]).toarray())[0]	
			predicted.append(pred)		
		print 'Done.'	 
		return predicted

	def NoOfAncestors(self, label):
		return len(self.ancestor_set[label])	

	def publish_labels(self, predicted, datafile):
		f = open(datafile,'wb')
		for row in predicted:
			f.write(row+'\n')

	def classifier_features(self):
		for label in sorted(self.classes.keys()):
			clf = self.clfs[label]
			vec = self.vec[label]
			print 
			print label
			print '='*20
			print 'Class Log Prior: ',clf.class_log_prior_	
			print 'Class Count: ',clf.class_count_

if __name__=='__main__':

	DATAFILE = 'train_run'+str(sys.argv[2])+'_text.txt'
	LABELFILE = 'train_run'+str(sys.argv[2])+'_labels.txt'
	TESTFILE = 'test_run'+str(sys.argv[2])+'_text.txt'
	OUTFILE = 'pred_run'+str(sys.argv[2])+'_'+''.join(ch for ch in sys.argv[1] if ch in '1234567890')+'.txt'

	cpn = ClassifierPerParentNode()
	cpn.train(DATAFILE, LABELFILE)
	predicted = cpn.predict(TESTFILE)
	cpn.publish_labels(predicted, OUTFILE)
				
