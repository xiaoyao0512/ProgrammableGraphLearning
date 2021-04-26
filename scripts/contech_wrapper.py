#!/usr/bin/env python

# Wrapper compiler for contech front end

import os
import sys
import subprocess
import shutil
from util import pcall
import glob
import tempfile
import subprocess

def main(isCpp = False, markOnly = False, minimal = False, hammer = False):
    
    # Hack to detect on ARM
    ARM = False
    if os.environ.has_key("USER"):
        uname = os.environ["USER"]
        if uname == "ubuntu":
            ARM = True
    
    # Set locations of clang, opt, and the contech pass
    if os.environ.has_key("CONTECH_HOME"):
        CONTECH_HOME = os.environ["CONTECH_HOME"]
        if os.environ.has_key("CONTECH_LLVM_HOME"):
            CONTECH_LLVM_HOME = os.environ["CONTECH_LLVM_HOME"]
            LLVMCONTECH = CONTECH_LLVM_HOME + "/lib/LLVMContech.so"
            CLANG = CONTECH_LLVM_HOME + "/bin/clang"
            CLANGPP = CLANG + "++"
            OPT = CONTECH_LLVM_HOME + "/bin/opt"
        else:
            ""
        #LLVMHAMMER = CONTECH_HOME + "/llvm_fe_3.2/build/Release+Asserts/lib/LLVMHammer.so"
        #RUNTIME = CONTECH_HOME + "/common/runtime/libct_runtime.a"
        if markOnly:
            # Use the .o file so that LLVM does not optimize away the marker calls
            RUNTIME = CONTECH_HOME + "/common/runtime/ct_runtime.o"
        else:
            if ARM == True:
                RUNTIME = CONTECH_HOME + "/common/runtime/ct_runtime.bc " + CONTECH_HOME + "/common/runtime/ct_main.bc "
            else:
                RUNTIME = CONTECH_HOME + "/common/runtime/ct_runtime.bc " + CONTECH_HOME + "/common/runtime/ct_main.bc "
        
        if os.environ.has_key("CONTECH_STATE_FILE"):
            stateFile = os.environ["CONTECH_STATE_FILE"]
        else:
            stateFile = CONTECH_HOME + "/scripts/output/contechStateFile.temp"

    else:        
        print ">Error: Could not find contech installation. Set CONTECH_HOME to the root of your contech directory."
        exit(1)
    
    #LOCAL = "/net/tinker/local"
    #LLVMCONTECH = LOCAL + "/lib/LLVMContech.so"
    #RUNTIME = LOCAL + "/lib/libct_runtime.a"
    
    
    # Name of the .c file to be processed
    cfile="" 
    # Names of the .o files to be linked
    ofiles=""
    # .o files hiding in .a files to be linked
    oFromAFiles=""
    # Name of the output file
    out=""
    # All remaining flags to be passed on to clang
    if ARM == True:
        CFLAGS="--verbose -pthread"
    else:
        CFLAGS="-flto --verbose -pthread"

    # Choose correct compiler
    if isCpp:
        CC = CLANGPP
    else:
        CC = CLANG
    
    outFileComingNext = False;
    compileOnly = False;
    depsOnly = False;
    dragon = False;
    MPI = False;
    
    for arg in sys.argv[1:]:

        # This compile step is just generating dependencies, don't compile or link unless instructed to
        if "-M" in arg:
            depsOnly = True
    
        # -o, look for filename next
        elif "-o" == arg:
            outFileComingNext = True
        
        # -o attached to other options
        elif "-o," in arg and out == "":
            
            # Option might have been passed to the linker with something like -Wl,-o,out
            if "," in arg:
                for token in arg.split(","):
                    if outFileComingNext == True:
                        out = token
                        outFileComingNext = False
                    elif token == "-o":
                        outFileComingNext = True
                # Make sure the whole option makes it to the CFLAGS, just in case
                CFLAGS = CFLAGS + " " + arg
                
            # -o attached to the front of the name
            else:
                out = arg
                out = out.replace("-o","",1)
            # TODO What other horrible ways are there to pass the name of the output file???
        
        # Saw -o at last arg
        elif outFileComingNext:
            out = arg
            outFileComingNext = False
            
        # C++ file
        elif ".cxx" == arg[-4:]:
            cfile = arg
            isCpp = True
        elif ".cpp" == arg[-4:]:
            cfile = arg
            isCpp = True
        elif ".cc" == arg[-3:]:
            cfile = arg
            isCpp = True
        # C file
        elif ".c" == arg[-2:]:
            cfile = arg
            isCpp = False
        elif ".f" == arg[-2:]:
            # Fortran only supported through dragonEgg and not clang
            cfile = arg
            dragon = True
        # Object file
        elif ".o" == arg[-2:]:
            ofiles = ofiles + " " + arg
        
        # Compile only
        elif "-c" == arg:
            compileOnly = True
        elif "-lmpi" == arg[0:5]:
            MPI = True
            CFLAGS = CFLAGS + " " + arg
        elif "-fcilkplus" == arg:
            CFLAGS = CFLAGS + " " + arg + " "
            CC = CC + "-cilk"
        # Combine other args into CFLAGS
        else:
            CFLAGS = CFLAGS + " " + arg


            
    # Debug
    #print ""
    #print "Contech wrapper: "
    #print "cfile=" + cfile
    #print "ofiles=" + ofiles
    #print "CFLAGS=" + CFLAGS
    #print "out=" + outdo

    # Found some flag that we don't handle, just pass through the compiler and exit
    if depsOnly and not compileOnly:
        passThrough(CC)
    
    # Compile requested but no input found, let the compiler throw an error
    if cfile == "" and compileOnly:
        passThrough(CC)
    
    # Requires dragon egg
    elif dragon == True:
        name=cfile[0: len(cfile) - 2]
        
        # Define names of intermediate files
        A= name + ".ll"
        B= name + "_ct.bc"
        
        # Define name of compiled file
        newobj = ""
        if out != "" :
            newobj = out
        else:
            newobj = name + ".o"
        
        # Make sure the output ends in .o
        if newobj[-2:] != ".o":
            newobj = newobj + ".o"
        
        # -fplugin=$CONTECH_LLVM_HOME/lib64/dragonegg.so -S -fplugin-arg-dragonegg-emit-ir
        pcall(["gcc", CFLAGS, "-S", "-fplugin=" + CONTECH_LLVM_HOME + "/lib/dragonegg.so" , "-fplugin-arg-dragonegg-emit-ir", cfile, "-o", A])
        
        pcall([OPT, "-load=" + LLVMCONTECH, "-Contech", A, "-o", B, "-ContechState", stateFile])
        # Compile bitcode back to a .o file
        pcall([CC, CFLAGS, "-c", "-o", newobj, B])
        # Add the generated object file to the list of things to link
        ofiles = ofiles + " " + newobj
        
    # Input file found, assuming compile requested.
    # Compile with contech   
    elif cfile != "":
        
        # Get the name of cfile without an extension
        if isCpp:
            name=cfile.replace(".cpp","",1);
            name=name.replace(".cc","",1);
        else:
        #linux.contech ... 
            name=cfile[0: len(cfile) - 2]
        
        # Define names of intermediate files
        A= name + ".bc"
        B= name + "_ct.bc"

        # Define name of compiled file
        newobj = ""
        if out != "" :
            newobj = out
        else:
            newobj = name + ".o"
        
        # Make sure the output ends in .o
        if newobj[-2:] != ".o":
            newobj = newobj + ".o"

        # Compile with clang to emit LLVM bitcode
        pcall([CC, CFLAGS, cfile, "-emit-llvm", "-c", "-o", A])
        # Run the Contech pass to add instrumentation
        
        if markOnly:
            pcall([OPT, "-load=" + LLVMCONTECH, "-Contech", A, "-o", B, "-ContechState", stateFile, "-ContechMarkFE"])
        elif minimal:
            pcall([OPT, "-load=" + LLVMCONTECH, "-Contech", A, "-o", B, "-ContechState", stateFile, "-ContechMinimal"])
        elif hammer:
            hammerNailFile = os.environ["HAMMER_NAIL_FILE"]
            hammerOptLevel = os.environ["HAMMER_OPT_LEVEL"]
            pcall([OPT, "-load=" + LLVMHAMMER, "-Hammer", A, "-o", B, "-HammerState", stateFile, "-HammerNailFile", hammerNailFile, "-HammerOptLevel", hammerOptLevel])
        else:
            if ARM == True:
                pcall([OPT, "-load=" + LLVMCONTECH, "-Contech", A, "-o", newobj, "-ContechState", stateFile])
            else:
                pcall([OPT, "-load=" + LLVMCONTECH, "-Contech", A, "-o", B, "-ContechState", stateFile])
        # Compile bitcode back to a .o file
        if ARM == True:
            print ""
        else:
            pcall([CC, CFLAGS, "-c", "-o", newobj, B])
        # Add the generated object file to the list of things to link
        ofiles = ofiles + " " + newobj
        
    # Link 
    if not compileOnly:
        if ofiles != "":
            
            # Define name of final executable
            if out == "":
                out = "a.out"
                
            if hammer:
                # Compile final executable
                pcall([CC, ofiles, CFLAGS, "-o", out, "-flto", "-lpthread", "-lz"])
            else:
                # Link in basic block table
                shutil.copyfile(stateFile, "contech.bin")
                # Note that we may have to create two .o, one for 32bit and one for 64bit
                OBJCOPY = "objcopy"
                
                if ARM == True:
                    pcall([OBJCOPY, "--input binary", "--output elf32-littlearm", "--binary-architecture arm", "contech.bin", "contech_state.o"])
                else:
                    pcall([OBJCOPY, "--input binary", "--output elf64-x86-64", "--binary-architecture i386", "contech.bin", "contech_state.o"])
                    #pcall([OBJCOPY, "--input binary", "--output elf32-i386", "--binary-architecture i386", "contech.bin", "contech_state.o"])

                # Does the binary use MPI?
                if MPI == True:
                    RUNTIME = RUNTIME + CONTECH_HOME + "/common/runtime/ct_mpi.bc "
                else:
                    RUNTIME = RUNTIME + CONTECH_HOME + "/common/runtime/ct_nompi.bc "
                    
                # Compile final executable

                # But first extract .o files hiding in .a libraries
                TMPARDIR = tempfile.mkdtemp()
                if os.path.isdir(TMPARDIR):
                    pcall(["mkdir",  "-p", TMPARDIR])

                    for flag in CFLAGS.split():
                        if ".a" == flag[-2:]:
                            aFilename = flag
                            if not flag.find("/") == -1:
                                aFilename = flag.split("/")[-1]
                            pcall(["cp", flag, TMPARDIR])
                            pcall(["cd", TMPARDIR, ";", CONTECH_HOME + "/scripts/uniq_ar_x.sh", aFilename])
                    oFromA = glob.glob(TMPARDIR + "/*.o")
                    for f in oFromA:
                        head = subprocess.Popen(["head", "-c", "3", f], stdout=subprocess.PIPE)
                        oFromAType = head.stdout.read()
                        if oFromAType.startswith("BC"):
                            oFromAFiles = oFromAFiles + " " + f 

                    pcall(["llvm-link", ofiles, RUNTIME, oFromAFiles, "-o", out + "_ct.link.bc"])
                    pcall(["rm",  "-rf", TMPARDIR])

                if ARM == True:
                    pcall([OPT, "-always-inline", out + "_ct.link.bc", "-o", out + "_ct_inline.bc"])
                    pcall([CC, CFLAGS, "-c -o", out + "_ct.o", out + "_ct_inline.bc"])
                    pcall([CC, out + "_ct.o", CFLAGS, "-o", out, "-lpthread", "contech_state.o"])
                else:
                    #Cilk runtime requires -ldl?
                    #Contech runtime requires -lrt and -lpthread
                    pcall([CC, RUNTIME, ofiles, CFLAGS, "-o", out, "-lrt", "-ldl", "-flto", "-lpthread", "contech_state.o"])
        else:
            passThrough(CC)


# Pass all args through to the compiler and don't do anything else
def passThrough(CC):
    command = [CC] + sys.argv[1:] 
    pcall(command, silent=True)
    exit(0)
    
if __name__ == "__main__":
    main(False)

    

