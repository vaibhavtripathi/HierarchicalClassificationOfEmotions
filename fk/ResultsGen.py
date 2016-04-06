import os
import sys

testdirectory = './'

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if 'pred_run'+str(sys.argv[1])+'_' in current_file:
    	os.system("paste test_run"+str(sys.argv[1])+"_labels.txt "+current_file+" > labelfile.txt")
    	resfile = 'res_run'+str(sys.argv[1])+'_'+''.join(ch for ch in current_file.split('_')[-1] if ch in '1234567890')+'.txt'
    	os.system("python ClassificationReport.py labelfile.txt > "+resfile)

