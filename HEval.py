from sets import Set
import numpy as np
from prettytable import PrettyTable
from sklearn.metrics import classification_report

class HEval:

	#HIERARCHY
	ancestor_set = {'A':Set(['A','-','E']), 'Sa':Set(['Sa','-','E']), 'D':Set(['D','-','E']), 'F':Set(['F','-','E']), 'Su-':Set(['Su-','-','E']), 'Su+':Set(['Su+','+','E']), 'H':Set(['H','+','E']), 'N':Set(['N']), 'E':Set(['E']), '+':Set(['+','E']), '-':Set(['-','E'])}

	#HEVAL_SAMPLE
	def h_eval_sample(self, alabel, plabel):
		a_ancestors = self.ancestor_set[alabel]
		p_ancestors = self.ancestor_set[plabel]
		i_ancestors = a_ancestors.intersection(p_ancestors)
		hp = len(i_ancestors)/float(len(p_ancestors))
		hr = len(i_ancestors)/float(len(a_ancestors))
		hp = hp*hp
		hr = hr*hr
		return [hp, hr]

	def h_eval_labels(self, alabelfile, plabelfile):
		alabels = []
		plabels = []
		p = []
		r = []
		precision = {}
		recall = {}
		support = {}
		
		with open(alabelfile,'rb') as f1:
			for label in f1:
				alabels.append(label[:-1]) 
		with open(plabelfile,'rb') as f2:
			for label in f2:
				plabels.append(label[:-1])	

		'''for index in range(len(alabels)):
			if alabels[index] not in recall:
				recall[alabels[index]] = []
			recall[alabels[index]].append(self.h_eval_sample(alabels[index], plabels[index])[1])	
			if plabels[index] in alabels:
				if plabels[index] not in precision:
					precision[plabels[index]] = []	
					support[plabels[index]] = []
				precision[plabels[index]].append(self.h_eval_sample(alabels[index], plabels[index])[0])
				support[plabels[index]].append(1)'''

		for index in range(len(alabels)):
			if alabels[index] not in recall:
				recall[alabels[index]] = []
			recall[alabels[index]].append(self.h_eval_sample(alabels[index], plabels[index])[1])
			r.append(self.h_eval_sample(alabels[index], plabels[index])[1])	
			
			if plabels[index] not in precision:
				precision[plabels[index]] = []	
				support[plabels[index]] = []
			precision[plabels[index]].append(self.h_eval_sample(alabels[index], plabels[index])[0])
			p.append(self.h_eval_sample(alabels[index], plabels[index])[0])
			support[plabels[index]].append(1)
		print 
		print "Overall Precision: "+str(np.average(p)) 
		print "Overall Recall: "+str(np.average(r)) 	
		print "Overall F - Score: "+str((2*np.average(r)*np.average(p))/(np.average(p)+np.average(r))) 
		for key in precision.keys():
			if key not in recall:
				recall[key] = 0
		for key in recall.keys():
			if key not in precision:
				precision[key] = 0
				support[key] = 0

		for label in precision.keys():
			precision[label] = np.average(precision[label])
			recall[label] = np.average(recall[label])	
			support[label] = np.sum(support[label])

		return [precision, recall, support]

	def NoOfAncestors(self, label):
		return len(self.ancestor_set[label])	

	def eval_result(self, alabelfile, plabelfile):
		[precision, recall, support] = self.h_eval_labels(alabelfile, plabelfile)
			
		table = PrettyTable(["Label", "HP", "HR", "HF", "Support"])
		table.align["Label"] = "l"
		p = []
		r = []
		f = []
		for label in sorted(precision.keys(), key=self.NoOfAncestors, reverse=True):
			table.add_row([label, precision[label], recall[label], (2*precision[label]*recall[label])/(precision[label]+recall[label]), support[label]])
			p.append(precision[label])
			r.append(recall[label])
			f.append((2*precision[label]*recall[label])/(precision[label]+recall[label]))
		print table	
		print

if __name__=='__main__':

	#ACTUAL AND PREDICTED LABELS
	ACTUAL = 'test_labels.txt'
	PREDICTED = 'pred.txt'

	heval = HEval()
	heval.eval_result(ACTUAL, PREDICTED)	
	

				
