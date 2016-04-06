import os

testdirectory = './'

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if '.tree' in current_file:
    	os.system("python ClassifierPerParentNode.py "+current_file)