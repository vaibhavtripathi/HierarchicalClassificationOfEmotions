import os
import sys

testdirectory = './'

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if '.tree' in current_file:
    	os.system("python CPPN-fk.py "+current_file+" "+sys.argv[1])