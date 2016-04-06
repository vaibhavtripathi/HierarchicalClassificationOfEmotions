import pickle
import numpy as np
import operator

f1 = open('scores_run1.p','rb')
f2 = open('scores_run2.p','rb')
f3 = open('scores_run3.p','rb')
f4 = open('scores_run4.p','rb')
f5 = open('scores_run5.p','rb')

s1 = pickle.load(f1)
s2 = pickle.load(f2)
s3 = pickle.load(f3)
s4 = pickle.load(f4)
s5 = pickle.load(f5)

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()

scores = {}
for key in s1.keys():
	scorevec = [s1[key],s2[key],s3[key],s4[key],s5[key]]
	scores[key] = np.average(scorevec)

sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
for i in sorted_scores:
	print i[0], '\t', i[1]

