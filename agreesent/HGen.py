from random import randint
import sys

#leaves = ['A','Sa','D','F','Su+','Su-','H','N']
#leaves = ['SAD','REQ','COM','ANG']
leaves = ['A','Sa','F','Su','H']

seq_no = 1
#Add code to handle when root has only one child

while seq_no < 100:
	f = open('h'+str(seq_no)+'.tree','w')
	f.write('#Leaves\n')
	f.write(':'.join(leaves)+'\n')
	f.write('#INodes\n')
	num_inodes = randint(1,len(leaves)-2) #AT LEAST ONE INTERNAL NODE

	inodes = []
	parent = {}
	subtree = dict()
	for i in range(num_inodes):
		inodes.append('IN'+str(i+1))
	f.write(':'.join(inodes)+'\n')
	print ':'.join(inodes)

	for node in inodes+['root']:
		subtree[node] = []

	for leaf in leaves:
		index = randint(0, num_inodes)
		if index == num_inodes:
			parent[leaf] = 'root'
			subtree['root'].append(leaf)
		else:
			parent[leaf] = inodes[index]
			subtree[inodes[index]].append(leaf)

	for node in inodes:
		index = randint(0, num_inodes)
		while index < num_inodes and (inodes[index] == node or inodes[index] in subtree[node]):
			index = randint(0, num_inodes)
		if index == num_inodes:
			parent[node] = 'root'
			subtree['root'].append(node)
			subtree['root'].extend(subtree[node])
		else:		
			parent[node] = inodes[index]
			subtree[inodes[index]].append(node)
			subtree[inodes[index]].extend(subtree[node])

	for key, value in parent.iteritems():
		print key, value

	#CONSISTENCY CHECKS
	inc_hier = False

	for key, value in subtree.iteritems():
		if len(value) < 2:
			inc_hier = True
			break

	for key in inodes+['root']:
		countleaves = len([leaf for leaf in subtree[key] if leaf in leaves])
		if countleaves == 0:
			inc_hier = True
			break

	rootkids = 0
	totchild = 0
	#Root must have atleast one internal node
	for key, value in parent.iteritems():
		if value == 'root':
			totchild = totchild + 1
			if key in inodes:
				rootkids = rootkids + 1

	if rootkids == 0:
		inc_hier = True

	if totchild < 2:
		inc_hier = True

	for node in inodes:
		par = parent[node]
		pathlen = 0
		while par!='root' and par!=node:
			if par==node:
				inc_hier = True
				break
			par = parent[par]
			pathlen = pathlen + 1
			if pathlen > num_inodes+1:
				inc_hier = True
				break	

	if inc_hier == True:
		f.close()
		continue
				
	for key, value in parent.iteritems():
		f.write(key+' '+value+'\n')	
	print 'H-File h'+ str(seq_no) +'.tree created'

	seq_no = seq_no + 1
	f.close()

