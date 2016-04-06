import os

testdirectory = './'

for file in os.listdir(testdirectory):
    current_file = os.path.join(testdirectory, file)
    if 'pred' in current_file:
    	os.system("paste fk-test-label.txt "+current_file+" > labelfile.txt")
    	resfile = 'res'+''.join(ch for ch in current_file if ch in '1234567890')+'.txt'
    	os.system("python ClassificationReport.py labelfile.txt > "+resfile)

