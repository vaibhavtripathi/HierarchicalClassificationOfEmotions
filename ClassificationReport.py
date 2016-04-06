import sys
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

gold = []
pred = []

with open(sys.argv[1], 'rb') as f:
	for line in f:
		line = line.strip('\n')
		line = line.split('\t')
		gold.append(line[0])
		pred.append(line[1])

print classification_report(gold, pred)
print '\t>>>', f1_score(gold, pred, average="micro")

