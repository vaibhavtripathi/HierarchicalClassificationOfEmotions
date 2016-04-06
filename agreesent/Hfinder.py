import os
import pickle
import sys
import operator

testdirectory = './'

scores = {}

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if 'res_run'+str(sys.argv[1])+'_' in current_file:
    	with open(current_file) as f:
    		for line in f:
    			if '>>>' in line:
    				line = ''.join([ch for ch in line if (ch.isdigit() or ch=='.')])
    				scores[current_file.replace('run'+str(sys.argv[1]),'')] = float(line)

sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
for i in sorted_scores:
	print i[0], '\t', i[1]

pickle.dump(scores,open('scores_run'+str(sys.argv[1])+'.p','wb'))