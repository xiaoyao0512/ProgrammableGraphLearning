import glob, os
for f in glob.glob("*.c"):
    #y = f.replace('.cl','.c')
    print f    
    #os.system("mv "+f+" "+y)
    #os.system("")
    os.system("gcc "+f)
    os.system("./a.out")
