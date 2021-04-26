import glob
import os


file1 = open('c/datasets.csv', 'r') 
lines = file1.readlines() 
fileNames = []
labels = []
for line in lines:
    temp = line.rstrip().split()
    fileName = temp[0]
    fileNames.append(fileName.replace('-', '_').replace('.', '_'))
    label = 0 if temp[1] == 'CPU' else 1 
    labels.append(label)
    os.system('perl run.pl '+fileName+'.c')
    
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
