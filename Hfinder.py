import os
import operator

testdirectory = './'

scores = {}

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if 'res' in current_file:
    	with open(current_file) as f:
    		for line in f:
    			if '>>>' in line:
    				line = ''.join([ch for ch in line if (ch.isdigit() or ch=='.')])
    				scores[current_file] = float(line)

sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
for i in sorted_scores:
	print i[0], '\t', i[1]