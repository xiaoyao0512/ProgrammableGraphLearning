# ProgrammableGraphLearning

1. Install required tools mentioned in Document/LLVM 3.8.1 Installation Guide;
2. The following steps are used to remove some cached files;\
  2.1. go to llvm-contech, remove CMakeCache.txt "rm CMakeCache.txt";\
  2.2. Type "cmake .";\
  2.3. Type "make";\
  2.4. Type "cd ..";\
  2.5. Type “make clean”;\
  2.6. Type "make";
3. Set an environment variable. For example, if one places it into the /home/Downloads folder, type "export /home/Downloads/ProgrammableGraphLearning";
4. If you have C code, go to the script folder, and run "perl run.pl <C code>" to obtain the graph representation; 
