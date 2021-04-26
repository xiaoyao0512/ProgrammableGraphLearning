#ifndef CONTECH_H
#define CONTECH_H

// These are included in contech.cpp, which creates the appropriate path
//  given that llvm decided to put the headers in different directories
//#include "llvm/Pass.h"
//#include "llvm/Module.h"

#include <string>
#include "ct_event_st.h"

//#define DEBUG_PRINT_CALLINST
#ifdef DEBUG_PRINT_CALLINST
    #define debugLog(s) errs() << s << "\n"
#else
    #define debugLog(s)
#endif
//#define SPLIT_DEBUG

#define __ctStrCmp(x, y) strncmp(x, y, sizeof(y) - 1)

namespace llvm {
    class Contech;
    ModulePass* createContechPass();
    
    
    typedef struct _llvm_mem_op {
        bool isWrite;
        bool isGlobal;
        bool isDep;
        char size;
        unsigned short depMemOp;
        int depMemOpDelta;
        Value* addr;
        struct _llvm_mem_op* next;
    } llvm_mem_op, *pllvm_mem_op;

    typedef struct _llvm_basic_block {
        unsigned int id, len, lineNum, numIROps, critPathLen;
        bool containCall;
        bool containGlobalAccess;
        pllvm_mem_op first_op;
        std::string fnName;
        std::string callFnName;
        //const char* fnName;
        const char* fileName;
    } llvm_basic_block, *pllvm_basic_block;
    
    typedef enum _CONTECH_FUNCTION_TYPE {
        NONE,
        MAIN,
        MALLOC,
        MALLOC2, // Calls like memalign(align, size)
        REALLOC,
        FREE,
        THREAD_CREATE,
        THREAD_JOIN,
        SYNC_ACQUIRE,
        SYNC_RELEASE,
        BARRIER,
        BARRIER_WAIT,
        EXIT,
        COND_WAIT,
        COND_SIGNAL,
        OMP_CALL,
        OMP_FORK,
        OMP_FOR_ITER,
        OMP_BARRIER,
        OMP_TASK_CALL,
        OMP_END,
        GLOBAL_SYNC_ACQUIRE, // Syncs that have no explicit address
        GLOBAL_SYNC_RELEASE,
        MPI_SEND_BLOCKING,
        MPI_RECV_BLOCKING,
        MPI_SEND_NONBLOCKING,
        MPI_RECV_NONBLOCKING,
        MPI_TRANSFER_WAIT,
        CILK_FRAME_CREATE,
        CILK_FRAME_DESTROY,
        CILK_SYNC,
        NUM_CONTECH_FUNCTION_TYPES
    } CONTECH_FUNCTION_TYPE;
    
    typedef struct _llvm_function_map {
        const char* func_name;
        size_t str_len;
        CONTECH_FUNCTION_TYPE typeID;
    } llvm_function_map, *pllvm_function_map;
    
    extern llvm_function_map functionsInstrument[];
    
    typedef struct _ConstantsCT {
        Constant* storeBasicBlockFunction;
        Constant* storeBasicBlockCompFunction;
        Constant* storeMemOpFunction;
        Constant* allocateBufferFunction;
        Constant* checkBufferFunction;
        Constant* storeThreadCreateFunction;
        Constant* storeSyncFunction;
        Constant* storeMemoryEventFunction;
        Constant* queueBufferFunction;
        Constant* storeBarrierFunction;
        Constant* allocateCTidFunction;
        Constant* getThreadNumFunction;
        Constant* storeThreadJoinFunction;
        Constant* storeThreadInfoFunction;
        Constant* storeBulkMemoryOpFunction;
        Constant* getCurrentTickFunction;
        Constant* createThreadActualFunction;
        Constant* checkBufferLargeFunction;
        Constant* getBufPosFunction;
        Constant* getBufFunction;
        
        Constant* storeBasicBlockMarkFunction;
        Constant* storeMemReadMarkFunction;
        Constant* storeMemWriteMarkFunction;

        Constant* storeMPITransferFunction;
        Constant* storeMPIWaitFunction;
        
        Constant* ompThreadCreateFunction;
        Constant* ompThreadJoinFunction;
        Constant* ompTaskCreateFunction;
        Constant* ompTaskJoinFunction;
        Constant* ompPushParentFunction;
        Constant* ompPopParentFunction;
        Constant* ctPeekParentIdFunction;
        Constant* ompProcessJoinFunction;
        Constant* ompGetNestLevelFunction;
        
        Constant* ompGetParentFunction;
        Constant* ompPrepareTaskFunction;
        Constant* ompStoreInOutDepsFunction;
        
        Constant* cilkInitFunction;
        Constant* cilkCreateFunction;
        Constant* cilkSyncFunction;
        Constant* cilkRestoreFunction;
        Constant* cilkParentFunction;
        
        Constant* pthreadExitFunction;
        
        Type* int8Ty;
        Type* int32Ty;
        Type* voidTy;
        PointerType* voidPtrTy;
        Type* int64Ty;
        Type* pthreadTy;
        int pthreadSize;
        
        unsigned ContechMDID;
    } ConstantsCT, *pConstantsCT;
    
    //
    // Contech - First record every load or store in a program
    //
    class Contech : public ModulePass {
    public:
        static char ID; // Pass identification, replacement for typeid
        ConstantsCT cct;
        const DataLayout* currentDataLayout;
        
        std::set<Function*> contechAddedFunctions;
        std::set<Function*> ompMicroTaskFunctions;
        
        Contech() : ModulePass(ID) {
        }
        
        virtual bool doInitialization(Module &M);
        virtual bool runOnModule(Module &M);
        virtual bool internalRunOnBasicBlock(BasicBlock &B,  Module &M, int bbid, bool markOnly, const char* fnName);
        virtual bool internalSplitOnCall(BasicBlock &B, CallInst**, int*);
        void addCheckAfterPhi(BasicBlock* B);
        void internalAddAllocate(BasicBlock& B);
        pllvm_mem_op insertMemOp(Instruction* li, Value* addr, bool isWrite, unsigned int memOpPos, Value*);
        unsigned int getSizeofType(Type*);
        unsigned int getSimpleLog(unsigned int);
        unsigned int getCriticalPathLen(BasicBlock& B);
        int getLineNum(Instruction* I);
        GetElementPtrInst* createGEPI(Type* t, Value* v, ArrayRef<Value*> ar, const Twine& tw, BasicBlock* B);
        GetElementPtrInst* createGEPI(Type* t, Value* v, ArrayRef<Value*> ar, const Twine& tw, Instruction* I);
        Function* createMicroTaskWrapStruct(Function* ompMicroTask, Type* arg, Module &M);
        Function* createMicroTaskWrap(Function* ompMicroTask, Module &M);
        Function* createMicroDependTaskWrap(Function* ompMicroTask, Module &M, size_t taskOffset, size_t numDep);
        Value* castSupport(Type*, Value*, Instruction*);
        Value* findCilkStructInBlock(BasicBlock& B, bool insert);
        bool blockContainsFunctionName(BasicBlock* B, _CONTECH_FUNCTION_TYPE cft);
        
        Value* findSimilarMemoryInst(Instruction*, Value*, int*);
        _CONTECH_FUNCTION_TYPE classifyFunctionName(const char* fn);
        
        virtual void getAnalysisUsage(AnalysisUsage &AU) const {
        
        }
    };
    
    //
    // Add Debug info to an instruction to indicate that it has been added by Contech
    //
    void MarkInstAsContechInst(Instruction* ii)
    {
        unsigned ctmd = ii->getParent()->getContext().getMDKindID("ContechInst");
        ii->setMetadata(ctmd, MDNode::get(ii->getParent()->getContext(), MDString::get(ii->getParent()->getContext(),"Contech")));
    }
    
    template<typename T>
    void insertMPITransfer(bool isSend, bool isBlocking, Value* startTime, T* ci, ConstantsCT* cct, Contech* ctPass)
    {
        Constant* cSend = ConstantInt::get(cct->int8Ty, isSend);
        Constant* cBlock = ConstantInt::get(cct->int8Ty, isBlocking);
        Value* reqArg = NULL;
        
        if (isBlocking == true)
        {
            reqArg = ConstantPointerNull::get(cct->voidPtrTy);
        }
        else
        {
            reqArg = ctPass->castSupport(cct->voidPtrTy, ci->getArgOperand(6), ci);
        }
        
        // Fortran sometimes passes with pointers instead of values
        Value* countArg = NULL;
        Value* destArg = NULL;
        Value* tagArg = NULL;
        if (ci->getArgOperand(1)->getType()->isPointerTy())
        {
            countArg = new LoadInst(ci->getArgOperand(1), "", ci);
            //MarkInstAsContechInst(countArg);
            
            destArg = new LoadInst(ci->getArgOperand(3), "", ci);
            //MarkInstAsContechInst(destArg);
            
            tagArg = new LoadInst(ci->getArgOperand(4), "", ci);
            //MarkInstAsContechInst(tagArg);
        }
        else
        {
            countArg = ci->getArgOperand(1);
            destArg = ci->getArgOperand(3);
            tagArg = ci->getArgOperand(4);
        }
        
        Value* argsMPIXF[] = {cSend, 
                              cBlock, 
                              countArg,  
                              ctPass->castSupport(cct->int32Ty, ci->getArgOperand(2), ci), // datatype, constant
                              destArg, 
                              tagArg, 
                              ctPass->castSupport(cct->voidPtrTy, ci->getArgOperand(0), ci), 
                              startTime,
                              reqArg};
        
        errs() << "Adding MPI Transfer call\n";
        
        // Need to insert after ci...
        CallInst* ciStore;
        if (isa<CallInst>(ci))
        {
            ciStore = CallInst::Create(cct->storeMPITransferFunction, 
                                                 ArrayRef<Value*>(argsMPIXF, 9), 
                                                 "", ci);
            ci->moveBefore(ciStore);
        }
        else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
        {
            ciStore = CallInst::Create(cct->storeMPITransferFunction, 
                                                 ArrayRef<Value*>(argsMPIXF, 9), 
                                                 "", ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime());
        }
        MarkInstAsContechInst(ciStore);
    }
    
    template<typename T>
    void InsertSyncEvent(T* ci, BasicBlock::iterator &I, ConstantsCT* cct, Instruction* &iPt, bool isAcquire, Value* synAddr)
    {
        Instruction* initialPt = NULL;
        debugLog("getCurrentTickFunction @" << __LINE__);
        CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
        MarkInstAsContechInst(nGetTick);
        
        Value* con1 = ConstantInt::get(cct->int32Ty, isAcquire);
        // If sync returns int, pass it, else pass 0 - success
        Value* retV;
        if (ci->getType() == cct->int32Ty)
            retV = ci;
        else 
            retV = ConstantInt::get(cct->int32Ty, 0);
        Value* cArg[] = {synAddr, con1, retV, nGetTick};
        
        if (isa<CallInst>(ci))
        {
            ++I;
            initialPt = I;
        }
        else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
        {
            initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
        }
        
        debugLog("storeSyncFunction @" << __LINE__);
        CallInst* nStoreSync = CallInst::Create(cct->storeSyncFunction, ArrayRef<Value*>(cArg,4),
                                            "", initialPt);  
        MarkInstAsContechInst(nStoreSync);
        
        if (isa<CallInst>(ci))
        {
            I = nStoreSync;
            iPt = ++I;
            I = nStoreSync;
        }
    }
    
    template<typename T> 
    BasicBlock::iterator InstrumentFunctionCall(T* ci,
                                                 bool &hasUninstCall, 
                                                 bool &containQueueBuf,
                                                 bool hasInstAllMemOps,
                                                 bool ContechMinimal,
                                                 BasicBlock::iterator I,
                                                 Instruction* &iPt,
                                                 llvm_basic_block* bi,
                                                 ConstantsCT* cct,
                                                 Contech* ctPass,
                                                 Module &M)
    {
        Function *f = ci->getCalledFunction();
        hasUninstCall = true;
        
        // call is indirect
        // TODO: add dynamic check on function called
        if (f == NULL) 
        { 
            Value* v = ci->getCalledValue();
            f = dyn_cast<Function>(v->stripPointerCasts());
            if (f == NULL)
            {
                return I; 
            }
        }

        int status;
        const char* fmn = f->getName().data();
        char* fdn = abi::__cxa_demangle(fmn, 0, 0, &status);
        const char* fn = fdn;
        if (status != 0) 
        {
            fn = fmn;
        }
        if (ci->doesNotReturn())
        {
            iPt = ci;
        }
        
        bi->callFnName.assign(fn);
        CONTECH_FUNCTION_TYPE funTy = ctPass->classifyFunctionName(fn);
        //errs() << funTy << "\n";
        switch(funTy)
        {
        
            // Check for call to exit(n), replace with pthread_exit(n)
            //  Splash benchmarks like to exit on us which pthread_cleanup doesn't catch
            //  Also check that this "...exit..." is at least a do not return function
            case(EXIT):
            {
                if (ci->getCalledFunction()->doesNotReturn())
                {
                    ci->setCalledFunction(cct->pthreadExitFunction);
                }
            }
            break;
            case(MALLOC):
            {
                if (!(ci->getCalledFunction()->getReturnType()->isVoidTy()))
                {
                    Value* cArg[] = {ConstantInt::get(cct->int8Ty, 1), ci->getArgOperand(0), ci};
                    debugLog("storeMemoryEventFunction @" << __LINE__);
                    CallInst* nStoreME;
                    if (isa<CallInst>(ci))
                    {
                        nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3),
                                                        "", ++I);   
                        I = nStoreME;                  
                    }
                    else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                    {
                        nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3),
                                                        "", ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime());  
                    }
                    MarkInstAsContechInst(nStoreME);
                }
            }
            break;
            case(MALLOC2):
            {
                if (!(ci->getCalledFunction()->getReturnType()->isVoidTy()))
                {
                    Value* cArg[] = {ConstantInt::get(cct->int8Ty, 1), ci->getArgOperand(1), ci};
                    debugLog("storeMemoryEventFunction @" << __LINE__);
                    CallInst* nStoreME;
                    if (isa<CallInst>(ci))
                    {
                        nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3),
                                                        "", ++I);   
                        I = nStoreME;                       
                    }
                    else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                    {
                        nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3),
                                                        "", ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime());  
                    }
                    MarkInstAsContechInst(nStoreME);
                }
            }
            break;
            case (REALLOC):
            {
                if (!(ci->getCalledFunction()->getReturnType()->isVoidTy()))
                {
                    // Malloc new space
                    // Memcpy old -> new
                    // Free old
                    Instruction* initialPt = NULL;
                    
                    if (isa<CallInst>(ci))
                    {
                        ++I;
                        initialPt = I;
                    }
                    else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                    {
                        initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                    }
                
                    Value* cArg[] = {ConstantInt::get(cct->int8Ty, 1), ci->getArgOperand(1), ci};
                    debugLog("storeMemoryEventFunction @" << __LINE__);
                    CallInst* nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3), "", initialPt);
                    MarkInstAsContechInst(nStoreME);
                   
                    // TODO: copy min of ci and ci->get(0), btw sizeof(ci get(0)) is unknown
                    Value* cArgS[] = {ci->getArgOperand(1), ci, ci->getArgOperand(0)};
                    debugLog("storeBulkMemoryOpFunction @" << __LINE__);
                    CallInst* nStoreCpy = CallInst::Create(cct->storeBulkMemoryOpFunction, ArrayRef<Value*>(cArgS, 3), "", initialPt);
                    MarkInstAsContechInst(nStoreCpy);
                 
                    // TOOD: Only free if ci and ci->get(0) are non-equal
                    Value* cz = ConstantInt::get(cct->int8Ty, 0);
                    Value* cz32 = ConstantInt::get(cct->pthreadTy, 0);
                    cArg[0] = cz;
                    cArg[1] = cz32;
                    cArg[2] = ci->getArgOperand(0);
                    CallInst* nStoreFree = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3), "", initialPt);
                    MarkInstAsContechInst(nStoreFree);
                }
            }
            break;
            case (FREE):
            {
                Value* cz = ConstantInt::get(cct->int8Ty, 0);
                Value* cz32 = ConstantInt::get(cct->pthreadTy, 0);
                Value* cArg[] = {cz, cz32, ci->getArgOperand(0)};
                debugLog("storeMemoryEventFunction @" << __LINE__);
                CallInst* nStoreME;
                if (isa<CallInst>(ci))
                {
                    nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3),
                                                    "", ++I);   
                    I = nStoreME;                     
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    nStoreME = CallInst::Create(cct->storeMemoryEventFunction, ArrayRef<Value*>(cArg, 3),
                                                    "", ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime());  
                }
                MarkInstAsContechInst(nStoreME);
            }
            break;
            case (SYNC_ACQUIRE):
            {
                Instruction* cast0 = new BitCastInst(ci->getArgOperand(0), cct->voidPtrTy, "locktovoid", ci);
                MarkInstAsContechInst(cast0);
                InsertSyncEvent(ci, I, cct, iPt, true, cast0);
            }
            break;
            case (SYNC_RELEASE):
            {
                Instruction* cast0 = new BitCastInst(ci->getArgOperand(0), cct->voidPtrTy, "locktovoid", ci);
                MarkInstAsContechInst(cast0);
                InsertSyncEvent(ci, I, cct, iPt, false, cast0);
            }
            break;
            case (GLOBAL_SYNC_ACQUIRE):
            {
                Value* cinst = ctPass->castSupport(cct->voidPtrTy, ConstantInt::get(cct->int64Ty, 0), I);
                InsertSyncEvent(ci, I, cct, iPt, true, cinst);
            }
            break;
            case (GLOBAL_SYNC_RELEASE):
            {
                Value* cinst = ctPass->castSupport(cct->voidPtrTy, ConstantInt::get(cct->int64Ty, 0), I);
                InsertSyncEvent(ci, I, cct, iPt, false, cinst);
            }
            break;
            case (COND_WAIT):
            {
                Instruction* initialPt = NULL;
                
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                BitCastInst* bciCV = new BitCastInst(ci->getArgOperand(0), cct->voidPtrTy, "locktovoid", ci);
                MarkInstAsContechInst(bciCV);
                
                BitCastInst* bciMut = new BitCastInst(ci->getArgOperand(1), cct->voidPtrTy, "locktovoid", ci);
                MarkInstAsContechInst(bciMut);
                
                Value* cArg[] = {bciMut, ConstantInt::get(cct->int32Ty, 0), ConstantInt::get(cct->int32Ty, 0), nGetTick};
                
                // Store the mutex unlock
                debugLog("storeSyncFunction @" << __LINE__);
                Instruction* callSF = CallInst::Create(cct->storeSyncFunction, ArrayRef<Value*>(cArg,4), "", ci);
                MarkInstAsContechInst(callSF);
                
                // ISSUE #63
                // TODO: By strict semantics, this queue buffer is not required.
                //   However, processing a trace may require excessive memory if the
                //   cond wait takes a long time.
                Value* c1 = ConstantInt::get(cct->int8Ty, 1);
                Value* cArgQB[] = {c1};
                debugLog("queueBufferFunction @" << __LINE__);
                CallInst* nQueueBuf = CallInst::Create(cct->queueBufferFunction, ArrayRef<Value*>(cArgQB, 1),
                                                    "", ci);
                MarkInstAsContechInst(nQueueBuf);
                
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick2 = CallInst::Create(cct->getCurrentTickFunction, "tick2", initialPt);
                MarkInstAsContechInst(nGetTick2);              
                
                Value* retV;
                if (ci->getType() == cct->int32Ty)
                    retV = ci;
                else 
                    retV = ConstantInt::get(cct->int32Ty, 0);                    
                Value* cArgCV[] = {bciCV, ConstantInt::get(cct->int32Ty, 2), retV, nGetTick2};
                debugLog("storeSyncFunction @" << __LINE__);
                CallInst* nStoreCV = CallInst::Create(cct->storeSyncFunction, ArrayRef<Value*>(cArgCV, 4), "", initialPt);
                MarkInstAsContechInst(nStoreCV);
                
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick3 = CallInst::Create(cct->getCurrentTickFunction, "tick3", initialPt);
                MarkInstAsContechInst(nGetTick3);
                
                Value* cArgMut[] = {bciMut, ConstantInt::get(cct->int32Ty, 1), ConstantInt::get(cct->int32Ty, 0), nGetTick3};
                debugLog("storeSyncFunction @" << __LINE__);
                CallInst* nStoreMut = CallInst::Create(cct->storeSyncFunction, ArrayRef<Value*>(cArgMut, 4), "", initialPt);
                MarkInstAsContechInst(nStoreMut);

                if (isa<CallInst>(ci))
                {
                    I = nStoreMut;
                    iPt = ++I;
                    I = nStoreMut;
                }
            }
            break;
            case (COND_SIGNAL):
            {
                Instruction* initialPt = NULL;
                
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                BitCastInst* bciCV = new BitCastInst(ci->getArgOperand(0), cct->voidPtrTy, "locktovoid", ci);
                MarkInstAsContechInst(bciCV);
                
                Value* retV;
                if (ci->getType() == cct->int32Ty)
                    retV = ci;
                else 
                    retV = ConstantInt::get(cct->int32Ty, 0);
                Value* cArgCV[] = {bciCV, ConstantInt::get(cct->int32Ty, 3), retV, nGetTick};
                
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                debugLog("storeSyncFunction @" << __LINE__);
                CallInst* nStoreCV = CallInst::Create(cct->storeSyncFunction, ArrayRef<Value*>(cArgCV, 4), "", 
                                                      initialPt);
                MarkInstAsContechInst(nStoreCV);
                
                if (isa<CallInst>(ci))
                {
                    I = nStoreCV;
                    iPt = ++I;
                    I = nStoreCV;
                }
            }
            break;
            case (BARRIER_WAIT):
            {
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                BitCastInst* bci = new BitCastInst(ci->getArgOperand(0), cct->voidPtrTy, "locktovoid", I);
                MarkInstAsContechInst(bci);
                
                Value* c1 = ConstantInt::get(cct->int8Ty, 1);
                Value* cArgs[] = {c1, bci, nGetTick};
                // Record the barrier entry
                debugLog("storeBarrierFunction @" << __LINE__);
                CallInst* nStoreBarEn = CallInst::Create(cct->storeBarrierFunction, ArrayRef<Value*>(cArgs,3),
                                                    "", I);
                MarkInstAsContechInst(nStoreBarEn);

                CallInst* nStoreBarEx;
                debugLog("storeBarrierFunction @" << __LINE__);
                cArgs[0] = ConstantInt::get(cct->int8Ty, 0);
                if (isa<CallInst>(ci))
                {
                    ++I;
                    nStoreBarEx = CallInst::Create(cct->storeBarrierFunction, ArrayRef<Value*>(cArgs,3),
                                                        "", I);
                    I = nStoreBarEx;
                    iPt = nStoreBarEn;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    nStoreBarEx = CallInst::Create(cct->storeBarrierFunction, ArrayRef<Value*>(cArgs,3),
                                                        "", ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime());
                }
                MarkInstAsContechInst(nStoreBarEx);
            }
            break;
            case (THREAD_JOIN):
            {
                //Value* vPtr = new BitCastInst(ci->getOperand(0), voidPtrTy, "hideInPtr", ci);
                //errs() << *ci->getOperand(0) << "\t" << *ci->getOperand(0)->getType() << "\n";
                //errs() << *storeThreadJoinFunction->getType() << "\n";
                Value* c1 = ConstantInt::get(cct->int8Ty, 1);
                Value* cArgQB[] = {c1};
                
                // NB This queue buffer call is important, as a join event is often long waiting.
                //   By queuing, the events before the join are processed, especially ticketed events
                debugLog("queueBufferFunction @" << __LINE__);
                CallInst* nQueueBuf = CallInst::Create(cct->queueBufferFunction, ArrayRef<Value*>(cArgQB, 1),
                                                    "", ci);
                MarkInstAsContechInst(nQueueBuf);
                
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                Value* cArg[] = {ci->getOperand(0), nGetTick};
                CallInst* nStoreJ;
                debugLog("storeThreadJoinFunction @" << __LINE__);
                if (isa<CallInst>(ci))
                {
                    ++I;
                    nStoreJ = CallInst::Create(cct->storeThreadJoinFunction, ArrayRef<Value*>(cArg, 2), 
                                                         Twine(""), I);
                    I = nStoreJ;
                    iPt = nGetTick;
                    containQueueBuf = true;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    nStoreJ = CallInst::Create(cct->storeThreadJoinFunction, ArrayRef<Value*>(cArg, 2), 
                                                     Twine(""), ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime());
                }
                MarkInstAsContechInst(nStoreJ);
            }
            break;
            //int pthread_create(pthread_t * thread, const pthread_attr_t * attr,
            //                   void * (*start_routine)(void *), void * arg);
            //
            case (THREAD_CREATE):
            {
                Instruction* cast1 = new BitCastInst(ci->getArgOperand(1), cct->voidPtrTy, "", ci);
                Value* cTcArg[] = {ci->getArgOperand(0), 
                                   cast1, 
                                   ci->getArgOperand(2), 
                                   ci->getArgOperand(3)};
                MarkInstAsContechInst(cast1);
                                   
                if (/*InvokeInst* ii = */NULL != dyn_cast<InvokeInst>(ci))
                {
                    assert("WILL REPLACE INVOKE with CALL INST" && 0);
                }
                                   
                debugLog("createThreadActualFunction @" << __LINE__);
                CallInst* nThreadCreate = CallInst::Create(cct->createThreadActualFunction,
                                                           ArrayRef<Value*>(cTcArg, 4), "", ci);
                MarkInstAsContechInst(nThreadCreate);
                ci->replaceAllUsesWith(nThreadCreate);
                ci->eraseFromParent();
                I = nThreadCreate;
                //ci->setCalledFunction(createThreadActualFunction);
            }
            break;
            case (OMP_END):
            {
                Instruction* initialPt = NULL;
                
                // End of a parallel region, restore parent stack
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                debugLog("ompPopParentFunction @" << __LINE__);
                // Also __ctOMPThreadJoin
                CallInst* parentId = CallInst::Create(cct->ctPeekParentIdFunction, "", initialPt);
                MarkInstAsContechInst(parentId); 
                
                Value* cArg[] = {parentId};
                Instruction* oTJF = CallInst::Create(cct->ompThreadJoinFunction, ArrayRef<Value*>(cArg, 1), "", initialPt);
                MarkInstAsContechInst(oTJF); 
                
                CallInst* nPopParent = CallInst::Create(cct->ompPopParentFunction, "", initialPt);
                MarkInstAsContechInst(nPopParent); 
                
                if (isa<CallInst>(ci))
                {
                    I = nPopParent;
                }
            }
            break;
            case (OMP_CALL):
            {
                Instruction* initialPt = NULL;
                
                // Simple case, push and pop the parent id
                // And Transform the arguments to the function call
                // The GOMP_parallel_start has a parallel_end routine, so the master thread
                //   returns immediately
                // Thus the pop parent should be delayed until the end routine executes
                Value* c1 = ConstantInt::get(cct->int8Ty, 1);
                Value* cArgQB[] = {c1};
                debugLog("queueBufferFunction @" << __LINE__);
                CallInst* nQueueBuf = CallInst::Create(cct->queueBufferFunction, ArrayRef<Value*>(cArgQB, 1),
                                                    "", ci);
                MarkInstAsContechInst(nQueueBuf); 
                
                debugLog("ompPushParentFunction @" << __LINE__);                                    
                CallInst* nPushPar = CallInst::Create(cct->ompPushParentFunction, "", ci);
                MarkInstAsContechInst(nPushPar); 
                
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                // __ctOMPThreadCreate after entering the parallel region
                CallInst* parentId = CallInst::Create(cct->ctPeekParentIdFunction, "", initialPt);
                MarkInstAsContechInst(parentId); 
                
                Value* cArg[] = {parentId};
                CallInst* oTCF = CallInst::Create(cct->ompThreadCreateFunction, ArrayRef<Value*>(cArg, 1), "", initialPt);
                MarkInstAsContechInst(oTCF); 
                
                if (isa<CallInst>(ci))
                {
                    I = oTCF;
                }
                
                // Change the function called to a wrapper routine
                Value* arg0 = ci->getArgOperand(0);
                Function* ompMicroTask = NULL;
                ConstantExpr* bci = NULL;
                if ((bci = dyn_cast<ConstantExpr>(arg0)) != NULL)
                {
                    if (bci->isCast())
                    {
                        ompMicroTask = dyn_cast<Function>(bci->getOperand(0));
                    }
                }
                else if ((ompMicroTask = dyn_cast<Function>(arg0)) != NULL)
                {
                    // Cast success
                    errs() << "OmpMicroTask - " << ompMicroTask;
                }
                else
                {
                    errs() << *(arg0->getType());
                    errs() << "Need new casting route for GOMP Parallel call\n";
                }
                ctPass->ompMicroTaskFunctions.insert(ompMicroTask);
                // Alloca Type and store pid and arg into alloc'd space
                Type* strTy[] = {cct->int32Ty, cct->voidPtrTy};
                Type* t = StructType::create(strTy);
                Instruction* nArg = new AllocaInst(t, "Wrapper Struct", ci);
                MarkInstAsContechInst(nArg);
                
                // Add Store insts here
                Value* gepArgs[2] = {ConstantInt::get(cct->int32Ty, 0), ConstantInt::get(cct->int32Ty, 0)};
                Instruction* ppid = ctPass->createGEPI(NULL, nArg, ArrayRef<Value*>(gepArgs, 2), "ParentIdPtr", ci);
                MarkInstAsContechInst(ppid);
                
                debugLog("getThreadNumFunction @" << __LINE__);
                Instruction* tNum = CallInst::Create(cct->getThreadNumFunction, "", ci);
                MarkInstAsContechInst(tNum);
                
                Instruction* stPPID = new StoreInst(tNum, ppid, ci);
                MarkInstAsContechInst(stPPID);
                
                gepArgs[1] = ConstantInt::get(cct->int32Ty, 1);
                Instruction* parg = ctPass->createGEPI(NULL, nArg, ArrayRef<Value*>(gepArgs, 2), "ArgPtr", ci);
                MarkInstAsContechInst(parg);
                
                Instruction* stPARG = new StoreInst(ci->getArgOperand(1), parg, ci);
                MarkInstAsContechInst(stPARG);
                
                Function* wrapMicroTask = ctPass->createMicroTaskWrapStruct(ompMicroTask, t, M);
                ctPass->contechAddedFunctions.insert(wrapMicroTask);
                Instruction* cast0 = new BitCastInst(wrapMicroTask, arg0->getType(), "", ci);
                ci->setArgOperand(0, cast0);
                MarkInstAsContechInst(cast0);
                
                Instruction* cast1 = new BitCastInst(nArg, cct->voidPtrTy, "", ci);
                ci->setArgOperand(1, cast1);
                MarkInstAsContechInst(cast1);                               
                //ci->setArgOperand(2, bci->getWithOperandReplaced(0,wrapMicroTask));
            }
            break;
            case (OMP_FORK):
            {
                Instruction* initialPt = NULL;
                // Simple case, push and pop the parent id
                // And Transform the arguments to the function call
                debugLog("ompPushParentFunction @" << __LINE__);
                CallInst* nPushParent = CallInst::Create(cct->ompPushParentFunction, "", ci);
                MarkInstAsContechInst(nPushParent);
                
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                    assert("WILL REPLACE INVOKE with CALL" && 0);
                }
                
                debugLog("ompPopParentFunction @" << __LINE__);
                CallInst* nPopParent = CallInst::Create(cct->ompPopParentFunction, "", initialPt);
                MarkInstAsContechInst(nPopParent);
                if (isa<CallInst>(ci))
                {
                    I = nPopParent;
                }
                
                // Add one to the number of arguments
                //   TODO: Make this a ConstantExpr
                ci->setArgOperand(1, BinaryOperator::Create(Instruction::Add,
                                            ci->getArgOperand(1),
                                            ConstantInt::get(cct->int32Ty, 1),
                                            "", ci));
                
                // Change the function called to a wrapper routine
                Value* arg2 = ci->getArgOperand(2);
                Function* ompMicroTask = NULL;
                ConstantExpr* bci = NULL;
                if ((bci = dyn_cast<ConstantExpr>(arg2)) != NULL)
                {
                    if (bci->isCast())
                    {
                        ompMicroTask = dyn_cast<Function>(bci->getOperand(0));
                    }
                }
                else
                {
                    errs() << "Need new casting route for omp fork call\n";
                }
                ctPass->ompMicroTaskFunctions.insert(ompMicroTask);
                Function* wrapMicroTask = ctPass->createMicroTaskWrap(ompMicroTask, M);
                ctPass->contechAddedFunctions.insert(wrapMicroTask);
                ci->setArgOperand(2, ConstantExpr::getBitCast(wrapMicroTask, bci->getType()));
                                                          
                // One cannot simply add an argument to an instruction
                // Instead we have to copy the arguments over and create a new instruction
                Value** cArg = new Value*[ci->getNumArgOperands() + 1];
                for (unsigned int i = 0; i < ci->getNumArgOperands(); i++)
                {
                    cArg[i] = ci->getArgOperand(i);
                }
                
                // Now add a new argument
                debugLog("getThreadNumFunction @" << __LINE__);
                Instruction* callTNF = CallInst::Create(cct->getThreadNumFunction, "", ci);
                cArg[ci->getNumArgOperands()] = callTNF;
                MarkInstAsContechInst(callTNF);
                
                // Can this queue buffer be removed?
                Value* cArgQB[] = {ConstantInt::get(cct->int8Ty, 1)};
                debugLog("queueBufferFunction @" << __LINE__);
                Instruction* callQBF = CallInst::Create(cct->queueBufferFunction, ArrayRef<Value*>(cArgQB, 1),
                                                        "", ci);
                MarkInstAsContechInst(callQBF);
                                                        
                debugLog("kmpc_fork_call @" << __LINE__);
                CallInst* nForkCall = CallInst::Create(ci->getCalledFunction(),
                                                       ArrayRef<Value*>(cArg, 1 + ci->getNumArgOperands()),
                                                       ci->getName(), ci);
                MarkInstAsContechInst(nForkCall);
                
                ci->replaceAllUsesWith(nForkCall);
                // Erase is dangerous, e.g. iPt could point to ci
                if (iPt == ci)
                    iPt = nPushParent;
                ci->eraseFromParent();
                delete [] cArg;
            }
            break;
            case (OMP_FOR_ITER):
            {
                Instruction* initialPt = NULL;
                debugLog("ompTaskJoinFunction @" << __LINE__);
                Instruction* callTJF = CallInst::Create(cct->ompTaskJoinFunction, "", ci);
                MarkInstAsContechInst(callTJF);
                
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                Value* cArg[] = {ci};
                debugLog("ompTaskCreateFunction @" << __LINE__);
                CallInst* nCreate = CallInst::Create(cct->ompTaskCreateFunction, ArrayRef<Value*>(cArg, 1), "", initialPt);
                MarkInstAsContechInst(nCreate);
                
                if (isa<CallInst>(ci))
                {
                    I = nCreate;
                }
            }
            break;
            case (OMP_BARRIER):
            {
                Instruction* initialPt = NULL;
                debugLog("ompProcessJoinFunction @" << __LINE__);
                Instruction* callPJF = CallInst::Create(cct->ompProcessJoinFunction, "", ci);
                MarkInstAsContechInst(callPJF);
                
                // OpenMP barriers use argument 1 for barrier ID
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                debugLog("ompGetParentFunction @" << __LINE__);
                CallInst* OGNLF = CallInst::Create(cct->ompGetNestLevelFunction, "", I);
                MarkInstAsContechInst(OGNLF);
                
                Value* sub1 = BinaryOperator::Create(Instruction::Sub,
                                            OGNLF,
                                            ConstantInt::get(cct->int32Ty, 1), "", I);
                Value* cArgGPF[] = {sub1}; // TODO: add check that this will saturate at 0
                CallInst* OGPF = CallInst::Create(cct->ompGetParentFunction, ArrayRef<Value*>(cArgGPF), "", I);
                MarkInstAsContechInst(OGPF);
                
                Value* mul8 = BinaryOperator::Create(Instruction::Mul,
                                            OGPF,
                                            ConstantInt::get(cct->int32Ty, 256), "", I);
                Value* mergV = BinaryOperator::Create(Instruction::Add,
                                            mul8,
                                            OGNLF, "", I);
                IntToPtrInst* bci = new IntToPtrInst(mergV, cct->voidPtrTy, "locktovoid", I);
                MarkInstAsContechInst(bci);
                
                // omp_get_active_level
                Value* c1 = ConstantInt::get(cct->int8Ty, 1);
                Value* cArgs[] = {c1, bci, nGetTick};
                // Record the barrier entry
                debugLog("storeBarrierFunction @" << __LINE__);
                CallInst* nStoreBarEn = CallInst::Create(cct->storeBarrierFunction, ArrayRef<Value*>(cArgs,3),
                                                    "", I);  
                MarkInstAsContechInst(nStoreBarEn);

                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                cArgs[0] = ConstantInt::get(cct->int8Ty, 0);
                // Record the barrier exit
                debugLog("storeBarrierFunction @" << __LINE__);
                CallInst* nStoreBarEx = CallInst::Create(cct->storeBarrierFunction, ArrayRef<Value*>(cArgs,3),
                                                    "", initialPt);
                MarkInstAsContechInst(nStoreBarEx);
                
                if (isa<CallInst>(ci))
                {
                    I = nStoreBarEx;
                    iPt = nStoreBarEn;
                }
            }
            break;
            case(OMP_TASK_CALL):
            {
                // __kmpc_omp_task_with_deps( ident_t *loc_ref, kmp_int32 gtid, kmp_task_t * new_task,
                //             kmp_int32 ndeps, kmp_depend_info_t *dep_list,
                //             kmp_int32 ndeps_noalias, kmp_depend_info_t *noalias_dep_list )
                //  IF the task has no dependencies, it is still invoked with this routine, with NULL depends lists
                //  new_task -> ... -> call __kmpc_omp_task_alloc(..., entry_point)
                //  kmp_depend_info_t { base_addr, in, out}
                //  Task will also be run in the current thread context
                Value* taskPtr = ci->getArgOperand(2);
                Value* nDeps = ci->getArgOperand(3);
                Value* depList = ci->getArgOperand(4);
                if (cct->ompPrepareTaskFunction == NULL)
                {
                    Type* argsPrepDep[] = {cct->voidPtrTy, cct->pthreadTy, depList->getType(), cct->int32Ty};
                    FunctionType* funPrepDepsTy = FunctionType::get(cct->voidTy, ArrayRef<Type*>(argsPrepDep, 4), false);
                    cct->ompPrepareTaskFunction = M.getOrInsertFunction("__ctOMPPrepareTask", funPrepDepsTy);
                }
                
                CallInst* taskAllocInst = dyn_cast<CallInst>(taskPtr);
                
                Value* baseTaskSize = taskAllocInst->getArgOperand(3);
                
                ConstantExpr* bci = NULL;
                Function* baseTask = NULL;
                if ((bci = dyn_cast<ConstantExpr>(taskAllocInst->getArgOperand(5))) != NULL)
                {
                    if (bci->isCast())
                    {
                        baseTask = dyn_cast<Function>(bci->getOperand(0));
                    }
                }
                else if ((baseTask = dyn_cast<Function>(taskAllocInst->getArgOperand(5))) != NULL)
                {
                    
                }
                else 
                {
                    errs() << "Need new casting route for omp task call\n";
                }
                
                Value* castTask = ctPass->castSupport(cct->voidPtrTy, taskPtr, ci);
                Value* cArgs[] = {castTask, baseTaskSize, depList, nDeps};
                Instruction* callPTF = CallInst::Create(cct->ompPrepareTaskFunction, ArrayRef<Value*>(cArgs, 4), "", ci);
                MarkInstAsContechInst(callPTF);
                
                ConstantInt* cnstTaskSize = dyn_cast<ConstantInt>(baseTaskSize);
                ConstantInt* cnstNDeps = dyn_cast<ConstantInt>(nDeps);
                
                Function* wrapDTask = ctPass->createMicroDependTaskWrap(baseTask, M, 
                                                                cnstTaskSize->getValue().getLimitedValue(), 
                                                                cnstNDeps->getValue().getLimitedValue());
                ctPass->contechAddedFunctions.insert(wrapDTask);
                
                // Add space for depend*, parentID, childID
                taskAllocInst->setArgOperand(3, BinaryOperator::Create(Instruction::Add,
                                            taskAllocInst->getArgOperand(3),
                                            ConstantInt::get(baseTaskSize->getType(), cct->pthreadSize + 2*4),
                                            "", taskAllocInst));
                taskAllocInst->setArgOperand(5, wrapDTask);
                
                // ParentID
                debugLog("getThreadNumFunction @" << __LINE__);
                Instruction* callTNF = CallInst::Create(cct->getThreadNumFunction, "", ci);
                MarkInstAsContechInst(callTNF);
            }
            break;
            case(MPI_SEND_BLOCKING):
            {
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                insertMPITransfer(true, true, nGetTick, ci, cct, ctPass);
            }
            break;
            case(MPI_RECV_BLOCKING):
            {
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                insertMPITransfer(false, true, nGetTick, ci, cct, ctPass);
            }
            break;
            case(MPI_SEND_NONBLOCKING):
            {
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                insertMPITransfer(true, false, nGetTick, ci, cct, ctPass);
            }
            break;
            case(MPI_RECV_NONBLOCKING):
            {
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                insertMPITransfer(false, false, nGetTick, ci, cct, ctPass);
            }
            break;
            case(MPI_TRANSFER_WAIT):
            {
                Instruction* initialPt = NULL;
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                Value* argWait[] = {ctPass->castSupport(cct->voidPtrTy, ci->getOperand(0), I), nGetTick};
                
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                CallInst* storeWait = CallInst::Create(cct->storeMPIWaitFunction, ArrayRef<Value*>(argWait, 2), "", initialPt);
                MarkInstAsContechInst(storeWait);
                
                if (isa<CallInst>(ci))
                {
                    I = storeWait;
                }
            }
            break;
            case (CILK_FRAME_CREATE):
            {
                // If this setjmp leads to cilk_sync, then ignore
                // N.B. LLVM 3.4 does not have getSingleSuccessor, but 3.6 does
                //   BasicBlock* sucB = ci->getParent()->getSingleSuccessor();
                BasicBlock* sucB = ci->getParent()->getTerminator()->getSuccessor(0);
                
                // If Contech has formed the basic blocks, then there should be 1 successor
                assert(sucB != NULL); 
                TerminatorInst* ti = sucB->getTerminator();
                bool isSyncFrame = false;
                for (unsigned i = 0; i < ti->getNumSuccessors(); i++)
                {
                    if (ctPass->blockContainsFunctionName(ti->getSuccessor(i), CILK_SYNC))
                    {
                        isSyncFrame = true;
                        break;
                    }
                }
                
                Instruction* initialPt = NULL;
                if (isa<CallInst>(ci))
                {
                    ++I;
                    initialPt = I;
                }
                else if (InvokeInst* ii = dyn_cast<InvokeInst>(ci))
                {
                    initialPt = ii->getNormalDest()->getFirstNonPHIOrDbgOrLifetime();
                }
                
                if (isSyncFrame)
                {
                    Value* ctCilkStructSync = ctPass->findCilkStructInBlock(ci->getParent()->getParent()->getEntryBlock(), false);
                    Value* argRest[] = {ctCilkStructSync};
                    debugLog("cilkParentFunction @" << __LINE__);
                    
                    CallInst* cilkRest = CallInst::Create(cct->cilkParentFunction, ArrayRef<Value*>(argRest, 1), "", initialPt);
                    MarkInstAsContechInst(cilkRest);
                    break;
                }
                
                Value* ctCilkStruct = ctPass->findCilkStructInBlock(ci->getParent()->getParent()->getEntryBlock(), true);
                if (ctCilkStruct == NULL)
                {
                    I = ci;
                    break;
                }
                
                // Add alloca, if not present, to entry block
                // cilkCreateFunction(%alloc, getCurrentTick, child, retval)
                debugLog("allocateCTidFunction @" << __LINE__);
                CallInst* nChildCTID = CallInst::Create(cct->allocateCTidFunction, "childCTID", ci);
                MarkInstAsContechInst(nChildCTID);
                debugLog("getCurrentTickFunction @" << __LINE__);
                CallInst* nGetTick = CallInst::Create(cct->getCurrentTickFunction, "tick", ci);
                MarkInstAsContechInst(nGetTick);
                
                Value* consZero = ConstantInt::get(cct->int64Ty, 0);
                Value* argParentCreate[] = {nChildCTID, consZero, nGetTick};
                debugLog("storeThreadCreateFunction @" << __LINE__);
                CallInst* parentCreate = CallInst::Create(cct->storeThreadCreateFunction,
                                                          ArrayRef<Value*>(argParentCreate, 3), "", ci);
                MarkInstAsContechInst(parentCreate);
                
                Value* argCreate[] = {ctCilkStruct, nGetTick, nChildCTID, ci};
                debugLog("cilkCreateFunction @" << __LINE__);
                CallInst* cilkCreate = CallInst::Create(cct->cilkCreateFunction, ArrayRef<Value*>(argCreate, 4), "", initialPt);
                MarkInstAsContechInst(cilkCreate);
                
                if (isa<CallInst>(ci))
                {
                    I = cilkCreate;
                }
            }
            break;
            case (CILK_FRAME_DESTROY):
            {
                Value* ctCilkStruct = ctPass->findCilkStructInBlock(ci->getParent()->getParent()->getEntryBlock(), false);
                if (ctCilkStruct == NULL)
                {
                    // Leave frame without creating a frame in this function
                    
                    Value* cinst = ctPass->castSupport(cct->voidPtrTy, ConstantInt::get(cct->int64Ty, 0), I);
                    Value* argRest[] = {cinst};
                    debugLog("cilkRestoreFunction @" << __LINE__);
                    
                    CallInst* cilkRest = CallInst::Create(cct->cilkRestoreFunction, ArrayRef<Value*>(argRest, 1), "", ci);
                    MarkInstAsContechInst(cilkRest);
                    
                    break;
                }
                
                
                Instruction* iPt = ci;//sucB->getFirstInsertionPt();
                
                Value* argRest[] = {ctCilkStruct};
                debugLog("cilkRestoreFunction @" << __LINE__);
                
                CallInst* cilkRest = CallInst::Create(cct->cilkRestoreFunction, ArrayRef<Value*>(argRest, 1), "", iPt);
                MarkInstAsContechInst(cilkRest);
                
                BasicBlock* sucB = ci->getParent()->getTerminator()->getSuccessor(0);
                iPt = sucB->getFirstInsertionPt();
                
                cilkRest = CallInst::Create(cct->cilkRestoreFunction, ArrayRef<Value*>(argRest, 1), "", iPt);
                MarkInstAsContechInst(cilkRest);
            }
            break;
            case (CILK_SYNC):
            {
                BasicBlock* sucB = ci->getParent()->getTerminator()->getSuccessor(0);
                
                Instruction* iPt = sucB->getFirstInsertionPt();
                
                Value* ctCilkStruct = ctPass->findCilkStructInBlock(ci->getParent()->getParent()->getEntryBlock(), true);
                if (ctCilkStruct == NULL)
                {
                    break;
                }
                
                Value* argSync[] = {ctCilkStruct};
                debugLog("cilkSyncFunction @" << __LINE__);
                CallInst* cilkSync = CallInst::Create(cct->cilkSyncFunction, ArrayRef<Value*>(argSync, 1), "", iPt);
                MarkInstAsContechInst(cilkSync);
                
                // Before syncing, restore to parent's frame
                Value* argRest[] = {ctCilkStruct};
                debugLog("cilkRestoreFunction @" << __LINE__);
                
                CallInst* cilkRest = CallInst::Create(cct->cilkRestoreFunction, ArrayRef<Value*>(argRest, 1), "", ci);
                MarkInstAsContechInst(cilkRest);
            }
            break;
            default:
            {
                // TODO: Function->isIntrinsic()
                if (0 == __ctStrCmp(fn, "memcpy")  ||
                    0 == __ctStrCmp(fn, "memmove"))
                {
                    Value* cArgS[] = {ci->getArgOperand(2), ci->getArgOperand(0), ci->getArgOperand(1)};
                    debugLog("storeBulkMemoryOpFunction @" << __LINE__);
                    Instruction* callBMOF = CallInst::Create(cct->storeBulkMemoryOpFunction, ArrayRef<Value*>(cArgS, 3), "", I);
                    MarkInstAsContechInst(callBMOF);
                    hasUninstCall = true;
                }
                else if (0 == __ctStrCmp(fn, "llvm."))
                {
                    if (0 == __ctStrCmp(fn + 5, "memcpy"))
                    {
                        // LLVM.memcpy can take i32 or i64 for size of copy
                        Value* castSize = ctPass->castSupport(cct->pthreadTy, ci->getArgOperand(2), I);
                        Value* cArgS[] = {castSize, ci->getArgOperand(0), ci->getArgOperand(1)};
                        debugLog("storeBulkMemoryOpFunction @" << __LINE__);
                        Instruction* callBMOF = CallInst::Create(cct->storeBulkMemoryOpFunction, ArrayRef<Value*>(cArgS, 3), "", I);
                        MarkInstAsContechInst(callBMOF);
                    }
                    else if (0 == __ctStrCmp(fn + 5, "memset"))
                    {
                        // LLVM.memset can take i32 or i64 for size of copy
                        Value* castSize = ctPass->castSupport(cct->pthreadTy, ci->getArgOperand(2), I);
                        // TODO: verify this construction works
                        Value* noSrcPtr = ctPass->castSupport(cct->voidPtrTy, ConstantInt::get(cct->int64Ty, 0), I);
                        Value* cArgS[] = {castSize, ci->getArgOperand(0), noSrcPtr};
                        debugLog("storeBulkMemoryOpFunction @" << __LINE__);
                        Instruction* callBMOF = CallInst::Create(cct->storeBulkMemoryOpFunction, ArrayRef<Value*>(cArgS, 3), "", I);
                        MarkInstAsContechInst(callBMOF);
                    }
                    else if (0 == __ctStrCmp(fn + 5, "dbg") ||
                             0 == __ctStrCmp(fn + 5, "lifetime"))
                    {
                        // IGNORE
                        hasUninstCall = false;
                    }
                    else
                    {
                        errs() << "Builtin - " << fn << "\n";
                        hasUninstCall = false;
                    }
                }
                else if (0 != __ctStrCmp(fn, "__ct"))
                {
                    // The function called is not something added by the instrumentation
                    //   and also not one that needs special treatment.
                }
                else
                {
                    hasUninstCall = false;
                }
            }
        }
        if (status == 0)
        {
            free(fdn);
        }
        
        return I;
    }
}

#endif
