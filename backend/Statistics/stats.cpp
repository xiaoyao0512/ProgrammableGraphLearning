#include "../../common/taskLib/TaskGraph.hpp"
#include <algorithm>
#include <iostream>
#include <set>
#include <stdio.h>

using namespace std;
using namespace contech;

int main(int argc, char const *argv[])
{
    //input check
    if (argc < 2)
    {
        cout << "Usage: " << argv[0] << " taskGraphInputFile [ROI]" << endl;
        exit(1);
    }

    FILE* taskGraphIn  = fopen(argv[1], "rb");
    if(taskGraphIn == NULL)
    {
        cerr << "ERROR: Couldn't open input file" << endl;
        exit(1);
    }

    uint64 totalTasks = 0;
    uint64 totalBasicBlocks = 0;
    uint64 totalMemOps = 0, totalMemBytes = 0;
    uint64 totalBlocksWithGlobals = 0;
    uint64 totalBlocksWithCalls = 0;
    uint64 totalBlocksInROI = 0;
    bool inROI = false;
    bool modelROI = (argc > 2);

    double averageBasicBlocksPerTask = 0;
    uint maxBasicBlocksPerTask = 0;

    double averageMemOpsPerTask = 0;
    uint maxMemOpsPerTask = 0;

    double averageMemOpsPerBasicBlock = 0;
    uint maxMemOpsPerBasicBlock = 0;

    uint syncCount = 0;
    uint barrCount = 0;
    uint createCount = 0;
    uint joinCount = 0;

    set<uint> uniqueBlocks;

    TaskGraph* tg = TaskGraph::initFromFile(taskGraphIn);
    
    if (tg == NULL) 
    {
        fprintf(stderr, "Failure to open task graph\n");
    }
    
    TaskGraphInfo* tgi = tg->getTaskGraphInfo();
    if (modelROI) tg->setTaskOrderCurrent(tg->getROIStart());

    while(Task* currentTask = tg->getNextTask())
    {

        totalTasks++;
        uint basicBlocksInTask = 0;
        uint memOpsInTask = 0;
        
        if (currentTask->getTaskId() == tg->getROIStart())
        {
            inROI = true;
        }
        else if (currentTask->getTaskId() == tg->getROIEnd())
        {
            inROI = false;
            if (modelROI)
            {
                delete currentTask;
                break;
            }
        }

        switch(currentTask->getType())
        {
            case task_type_basic_blocks:
            {
                auto bba = currentTask->getBasicBlockActions();
                for (auto f = bba.begin(), e = bba.end(); f != e; ++f)
                {
                    BasicBlockAction bb = *f;
                    uniqueBlocks.insert((uint)bb.basic_block_id);
                    
                    auto bbi = tgi->getBasicBlockInfo((uint)bb.basic_block_id);
                    
                    if (0 != (bbi.flags & BBI_FLAG_CONTAIN_CALL))
                    {
                        totalBlocksWithCalls++;
                    }
                    if (0 != (bbi.flags & BBI_FLAG_CONTAIN_GLOBAL_ACCESS))
                    {
                        totalBlocksWithGlobals++;
                    }
                    
                    if (inROI) totalBlocksInROI++;
                    
                    totalBasicBlocks++;
                    basicBlocksInTask++;

                    uint memOpsInBlock = 0;
                    // Note that memory actions include malloc, etc
                    for (MemoryAction mem : f.getMemoryActions())
                    {
                        totalMemOps++;
                        memOpsInTask++;
                        memOpsInBlock++;
                        if (mem.type == action_type_mem_read || mem.type == action_type_mem_write)
                            totalMemBytes += (0x1 << mem.pow_size);
                    }

                    maxMemOpsPerBasicBlock = max(maxMemOpsPerBasicBlock, memOpsInBlock);
                }

                maxBasicBlocksPerTask = max(maxBasicBlocksPerTask, basicBlocksInTask);
                maxMemOpsPerTask = max(maxMemOpsPerTask, memOpsInTask);

                break;
            }
            case task_type_sync:
                syncCount++;
                break;

            case task_type_barrier:
                barrCount++;
                break;

            case task_type_create:
                createCount++;
                break;

            case task_type_join:
                joinCount++;
                break;

        }

        delete currentTask;
    }
    
    delete tg;

    averageMemOpsPerBasicBlock = ((double)totalMemOps / totalBasicBlocks);
    averageBasicBlocksPerTask = ((double)totalBasicBlocks / totalTasks);
    averageMemOpsPerTask = ((double)totalMemOps / totalTasks);


    printf("\n");
    printf("Statistics for %s\n", argv[1]);
    printf("----------------------------------\n");
    printf("Total Tasks: %llu\n", totalTasks);
    printf("\n");
    printf("Unique Basic Blocks: %llu\n", uniqueBlocks.size());
    printf("Average Basic Blocks per Task: %f\n", averageBasicBlocksPerTask);
    printf("Max Basic Blocks per Task: %u\n", maxBasicBlocksPerTask);
    printf("Total Basic Blocks: %llu\n", totalBasicBlocks);
    printf("Total Blocks in ROI: %llu\n", totalBlocksInROI);
    printf("Blocks with Function Calls: %lf\n", (double)(totalBlocksWithCalls) / (double)(totalBasicBlocks));
    printf("Blocks with Global Accesses: %lf (%llu)\n", (double)(totalBlocksWithGlobals) / (double)(totalBasicBlocks), totalBlocksWithGlobals);
    printf("\n");
    printf("Total MemOps: %llu\n", totalMemOps);
    printf("Total Bytes Accessed: %llu\n", totalMemBytes);
    printf("Average MemOps per Task: %f\n", averageMemOpsPerTask);
    printf("Max MemOps per Task: %u\n", maxMemOpsPerTask);
    printf("Average MemOps per Basic Block: %f\n", averageMemOpsPerBasicBlock);
    printf("Max MemOps per Basic Block: %u\n", maxMemOpsPerBasicBlock);
    printf("\n");
    printf("Sync tasks: %u\n", syncCount);
    printf("Barrier tasks: %u\n", barrCount);
    printf("Create tasks: %u\n", createCount);
    printf("Join tasks: %u\n", joinCount);
    printf("\n");

    fclose(taskGraphIn);
    return 0;
}
