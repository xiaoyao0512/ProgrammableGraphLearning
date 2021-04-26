#include "middle.hpp"
#include "taskWrite.hpp"
#include <sys/timeb.h>
#include <pthread.h>
#include <unordered_map>

using namespace std;
using namespace contech;

void* backgroundTaskWriter(void*);

int main(int argc, char* argv[])
{
    bool parallelMiddle = true;
    pthread_t backgroundT;
    EventQ eventQ;
    bool roiEvent = false;
    
    // First attempt middle layer in parallel, if there is an error,
    //   then restart in serial mode.
    //   TODO: Implement restart / reset, or a flag for running serially.
reset_middle:
    if (argc < 3)
    {
        fprintf(stderr, "Missing positional argument(s)\n");
        fprintf(stderr, "%s <event trace>* <taskgraph> [-d]\n", argv[0]);
        return 1;
    }
    
    // Print debug statements?
    bool DEBUG = false;
    
    int lastInPos = argc - 2;
    int totalRanks = 0;
    if (DEBUG == true) lastInPos--;
    
    for (int argPos = 1; argPos <= lastInPos; argPos++, totalRanks++)
    {
        FILE* in;
        in = fopen(argv[argPos], "rb");
        eventQ.registerEventList(in);
    }
    
    // Open output file
    // Use command line argument or stdout
    //FILE* out;
    FILE* out;
    int outArgPos = argc - 1;
    if (DEBUG == true) outArgPos--;
    out = fopen(argv[outArgPos], "wb");
    
    int taskGraphVersion = TASK_GRAPH_VERSION;
    unsigned long long space = 0;
    
    // Init TaskGraphFile
    ct_write(&taskGraphVersion, sizeof(int), out);
    ct_write(&space, sizeof(unsigned long long), out); // Index
    ct_write(&space, sizeof(unsigned long long), out); // ROI start
    ct_write(&space, sizeof(unsigned long long), out); // ROI end
    
    pthread_mutex_init(&taskQueueLock, NULL);
    pthread_cond_init(&taskQueueCond, NULL);
    taskQueue = new deque<Task*>;
    int r = pthread_create(&backgroundT, NULL, backgroundTaskWriter, &out);
    assert(r == 0);
    
    // Track the owners of sync primitives
    map<ct_addr_t, Task*> ownerList;
    
    // Track the barrier task for each address
    map<ct_addr_t, BarrierWrapper> barrierList;

    // Declare each context
    map<ContextId, Context> context;

    // MPI Transfers src-rank -> dst rank -> tag -> task
    map <int, map <int, map <int, Task*> > > mpiSendQ;
    map <int, map <int, map <int, Task*> > > mpiRecvQ;
    map <int, map <ct_addr_t, mpi_recv_req> > mpiReq;
    
    // Context 0 is special, since it is uncreated
    if (totalRanks > 1)
    {
        //context[0].tasks.push_front(new Task(0, task_type_create));
        context[0].tasks[0] = new Task(0, task_type_create);
    }
    else
    {
        //context[0].tasks.push_front(new Task(0, task_type_basic_blocks));
        context[0].tasks[0] = new Task(0, task_type_basic_blocks);
    }
    context[0].hasStarted = true;
    

    // Count the number of events processed
    uint64 eventCount = 0;

    
    // Scan through the file for the first real event
    bool seenFirstEvent = false;
    int currentRank = 0;
    TaskGraphInfo *tgi = new TaskGraphInfo();
    while (ct_event* event = eventQ.getNextContechEvent(&currentRank))
    {
        if (event->contech_id == 0
        &&  event->event_type == ct_event_task_create
        &&  event->tc.other_id == 0)
        {
            // Use the timestamp of the first event in context 0 as t=0 in absolute time
            context[(currentRank << 24) | 0].timeOffset = event->tc.start_time;
            
            // Since every instance should have identical bbinfo, the first create should be
            //   rank 0, and then every other rank
            seenFirstEvent = true;
        }
        else if (event->event_type == ct_event_basic_block_info && currentRank == 0)
        {
            string functionName, fileName, callFunName;
            if (event->bbi.fun_name != NULL) functionName.assign(event->bbi.fun_name);
            if (event->bbi.file_name != NULL) fileName.assign(event->bbi.file_name);
            if (event->bbi.callFun_name != NULL) callFunName.assign(event->bbi.callFun_name);
            //printf("%d - %d at %d\t", event->bbi.basic_block_id, event->bbi.num_mem_ops, event->bbi.line_num);
            //printf("in %s() of %s\n", event->bbi.fun_name, event->bbi.file_name);
            //printf("%d <> %d\n", event->bbi.crit_path_len, event->bbi.num_ops);
            
            tgi->addRawBasicBlockInfo(event->bbi.basic_block_id, 
                                     event->bbi.flags,
                                     event->bbi.line_num, 
                                     event->bbi.num_mem_ops,
                                     event->bbi.num_ops,
                                     event->bbi.crit_path_len,
                                     functionName,
                                     fileName,
                                     callFunName);
            //std::cout << "HHHHHHH\n";
        }
        EventLib::deleteContechEvent(event);
        if (seenFirstEvent) break;
    }
    assert(seenFirstEvent);
    
    tgi->writeTaskGraphInfo(out);
    delete tgi;
    unordered_map<int, int> hash;
    int resolution = 20;
    // Main loop: Process the events from the file in order
    while (ct_event* event = eventQ.getNextContechEvent(&currentRank))
    {
        ++eventCount;

        // Whitelist of event types that we handle. Others are informational/debug info and can be skipped
        // Be sure to add event types to this list if you handle new ones
        switch (event->event_type)
        {
            case ct_event_task_create:
            case ct_event_sync:
            case ct_event_barrier:
            case ct_event_task_join:
            case ct_event_basic_block:
            case ct_event_memory:
            case ct_event_bulk_memory_op:
            case ct_event_mpi_transfer:
            case ct_event_mpi_wait:
            case ct_event_roi:
                break;
            default:
                EventLib::deleteContechEvent(event);
                continue;
        }
        
        // The context in which this event occurred
        Context& activeContech = context[(currentRank << 24) | event->contech_id];
  
        // Basic blocks: Record basic block ID and memOp's
        if (event->event_type == ct_event_basic_block)
        {
            Task* activeT = activeContech.activeTask();
            int id = event->bbi.basic_block_id;
            if (hash.find(id) == hash.end()) {
                hash[id] = 1;
                std::cout << "BasicBlock# = " << id << std::endl;
            } else {
                if (hash[id] <= resolution) {
                    hash[id] += 1;
                    std::cout << "BasicBlock# = " << id << std::endl;
                }
            }
            
            //
            // If transitioning into a basic block task, perhaps the older tasks
            //   are complete and can be queued to the background thread.
            //
            if (activeT->getType() != task_type_basic_blocks &&
                parallelMiddle)
            {
                activeContech.createBasicBlockContinuation();
                //std::cout << "1" << std::endl;
                if (DEBUG) {fprintf(stderr, "%s (%d) -> %s via Basic Block (%d)\n", 
                                            activeT->getTaskId().toString().c_str(), activeT->getType(),
                                            activeContech.activeTask()->getTaskId().toString().c_str(),
                                            event->bb.basic_block_id);}
                
                // Is the current active task a create or a complete join?
                attemptBackgroundQueueTask(activeT, activeContech);
                
                updateContextTaskList(activeContech);
                
                activeT = activeContech.activeTask();
            }
            else if (activeT->getBBCount() >= MAX_BLOCK_THRESHOLD)
            {
                // There is no available time stamp for ending this task
                //   Assume that every basic block costs 1 cycle, which is a
                //   lower bound
                //std::cout << "overflow\n"; 
                //std::cout << "2" << std::endl;
                activeT->setEndTime(activeT->getStartTime() + MAX_BLOCK_THRESHOLD);
                activeContech.createBasicBlockContinuation();
                activeContech.removeTask(activeT);
                backgroundQueueTask(activeT);
                updateContextTaskList(activeContech);
                
                activeT = activeContech.activeTask();
            }
            
            // If the basic block action will overflow, then split the task at this time
            try {
                // Record that this task executed this basic block
                activeT->recordBasicBlockAction(event->bb.basic_block_id);
                //std::cout << "3" << std::endl;
            }
            catch (std::bad_alloc)
            {
                activeT->setEndTime(activeT->getStartTime() + MAX_BLOCK_THRESHOLD);
                activeContech.createBasicBlockContinuation();
                activeContech.removeTask(activeT);
                backgroundQueueTask(activeT);
                updateContextTaskList(activeContech);
                
                activeT = activeContech.activeTask();
                activeT->recordBasicBlockAction(event->bb.basic_block_id);
            }

            // Examine memory operations
            for (uint i = 0; i < event->bb.len; i++)
            {
                ct_memory_op memOp = event->bb.mem_op_array[i];
                memOp.rank = currentRank;
                //std::cout << "4" << std::endl;
                activeT->recordMemOpAction(memOp.is_write, memOp.pow_size, memOp.data);
                //std::cout << "size is " << memOp.pow_size << std::endl;
            }
        }


        else if (event->event_type == ct_event_memory)
        {
            ct_memory_op memA;
            memA.data = 0;
            //std::cout << "event_memory\n";
            memA.addr = event->mem.alloc_addr;
            memA.rank = currentRank;
            if (event->mem.isAllocate)
            {
                activeContech.activeTask()->recordMallocAction(memA.data, event->mem.size);
            } else {
                activeContech.activeTask()->recordFreeAction(memA.data);
            }

        } 
        
        // Memcpy etc
        //  In the case of etc, src may be NULL
        else if (event->event_type == ct_event_bulk_memory_op)
        {
            ct_memory_op srcA, dstA;
            srcA.data = 0;
            srcA.addr = event->bm.src_addr;
            srcA.rank = currentRank;
            dstA.data = 0;
            dstA.addr = event->bm.dst_addr;
            dstA.rank = currentRank;
            //std::cout << "event_memory\n";
            //std::cout << "9" << std::endl;
            activeContech.activeTask()->recordMemCpyAction(event->bm.size, dstA.data, srcA.data);
        }
        // End switch block on event type

        // Free memory for the processed event
        EventLib::deleteContechEvent(event);
    }
    //displayContechEventDiagInfo();

    // TODO: for every context if endtime == 0, then join?
   
    //printf("Processed %lu events.\n", eventCount);
    // Write out all tasks that are ready to be written
    
    char* d = NULL;
    int task = 0;
    
    for (auto& p : context)
    {
        Context& c = p.second;
        
        //printf("%d\t%llx\t%llx\t%llx\n", p.first, c.timeOffset, c.startTime, c.endTime);
        
        //for (Task* t : c.tasks)
        for (auto t : c.tasks)
        {
            backgroundQueueTask(t.second);
        	task++;
        }
    }
    //std::cout << "task: " << task << std::endl;
    
    pthread_mutex_lock(&taskQueueLock);
    noMoreTasks = true;
    pthread_cond_signal(&taskQueueCond);
    pthread_mutex_unlock(&taskQueueLock);
    {
        struct timeb tp;
        ftime(&tp);
        printf("MIDDLE_QUEUE: %d.%03d\n", (unsigned int)tp.time, tp.millitm);
    }
    pthread_join(backgroundT, (void**) &d);
    
    {
        struct timeb tp;
        ftime(&tp);
        printf("MIDDLE_END: %d.%03d\n", (unsigned int)tp.time, tp.millitm);
    }
    
    fclose(out);
    
    return 0;
}
