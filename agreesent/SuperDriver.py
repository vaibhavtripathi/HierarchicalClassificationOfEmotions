import os
for i in range(1,6):
	os.system("python Driver-fk.py "+str(i))

for i in range(1,6):
	os.system("python ResultsGen.py "+str(i))

for i in range(1,6):
	os.system("python Hfinder.py "+str(i))
