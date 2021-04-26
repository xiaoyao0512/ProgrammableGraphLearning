import re
import random
import os


def progTrans(fileRead, fileWrite, ite):
	fr = open(fileRead+'.c', 'r')
	fw = open(fileWrite+'.c', "w")
	lines = fr.readlines()
	for line in lines:
		temp = line.strip()
		if re.match(r"for", temp):
			#temp = re.sub(r'for\(.*;\s*\w+\s*<\s*\d+;.*\)', 'for\(.*;\s*\w+\s*<\s*{};.*\)'.format(ite), temp)
			temp = re.sub(r'\d{2}', '{}'.format(ite), temp)
		print(temp)		
		fw.write(temp)
		fw.write('\n')
		#print(temp)
	fr.close()
	fw.close()

file1 = open('c/datasets.csv', 'r') 
lines = file1.readlines() 
fileNames = []
labels = []
f = open("newDatasets.csv", "w")
#f.write("Now the file has more content!")
iteration = [1, 2, 3, 4, 12, 13, 14, 15]
for line in lines:
    temp = line.rstrip().split()
    fileName = temp[0]
    for i in range(8):
    	#label = 0 if temp[1] == 'CPU' else 1 
    	#ite = random.randint(4,20)
    	ite = iteration[i]
    	fileName1 = fileName + '-' + str(ite)
    	print fileName1
    	print fileName
    	fileNames.append(fileName1.replace('-', '_').replace('.', '_'))
    	progTrans(fileName, fileName1, ite)
    	f.write(fileName1)
    	f.write(' ')
    	f.write(temp[1])
    	f.write('\n')
    	os.system('perl ee554-2.pl '+fileName1+'.c')
        count = 0
        label = 0
        with open('graphs/'+fileName1.replace('-', '_').replace('.', '_')+'.py') as fil:
            count = sum(1 for _ in fil)    
        if (count < 5000):
            label = 0
        else:
            label = 1    
        labels.append(label)
    	print('-----END-----')
    	

    
file1.close() 
f.close()

file1.close() 

numFiles = len(labels) #30
kfold = 5
# Once all of the graphs are generated in the graph folder,
# create a dataset.py file containing these graphs.

f = open("dataset.py", "w")
f.write("from torch.utils.data import Dataset, DataLoader\n")
f.write("import torch\n")
f.write("import sys\n")
f.write("sys.path.append('graphs/')\n")
for fh in fileNames:
    f.write("import " + fh + "\n")
f.write("import numpy as np\n")
f.write("class GraphDataset(Dataset):\n")
f.write("\tdef __init__(self):\n") 

filestr = "["
for idx in range(len(fileNames)):
    fh = fileNames[idx]
    if (idx != len(fileNames) - 1):
        filestr += fh + "." + fh + "(), "
    else:
        filestr += fh + "." + fh + "()]"
labelstr = "["
for idx in range(len(labels)):
    l = labels[idx]
    if (idx != len(labels) - 1):
        labelstr += str(l) + ", "
    else:
        labelstr += str(l) + "]"

f.write("\t\tself.graphs = " + filestr + "\n")
f.write("\t\tself.labels = " + labelstr + "\n")
f.write("\tdef __len__(self):\n")
f.write("\t\treturn len(self.graphs)\n")
f.write("\tdef __getitem__(self, idx):\n")

#f.write("\t\tif torch.is_tensor(idx):")
#f.write("\t\t\tidx = idx.tolist()")
#f.write("\t\tgraph = [self.graphs[i] for i in idx]")
#f.write("\t\tlabel = [self.labels[i] for i in idx]")
#f.write("\t\tsample = {'graph': graph, 'label': label}")
f.write("\t\treturn self.graphs[idx], self.labels[idx]\n")
f.close()
