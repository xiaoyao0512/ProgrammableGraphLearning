#ifndef CT_EVENT_H
#define CT_EVENT_H

#include "../taskLib/ct_file.h"
#include "ct_event_st.h"
#include <stdint.h>
#include <stdarg.h>

namespace contech
{
    //
    // Maps basic_block_ids to string identifiers
    //
    typedef struct _ct_basic_block_info
    {
        uint32_t basic_block_id, fun_name_len, file_name_len, callFun_name_len, num_mem_ops, line_num, num_ops, crit_path_len;
        uint32_t flags;
        char* file_name;
        char* fun_name;
        char* callFun_name;
    } ct_basic_block_info, *pct_basic_block_info;

    typedef struct _ct_basic_block
    {
        uint32_t basic_block_id, len;
        pct_memory_op mem_op_array;
    } ct_basic_block, *pct_basic_block;

    typedef struct _ct_memory
    {
        bool isAllocate;
        uint64_t size;  // Only has meaning if isAllocate = true
        ct_addr_t alloc_addr;
    } ct_memory, *pct_memory;

    typedef struct _ct_sync
    {
        int sync_type;
        ct_tsc_t start_time;
        ct_tsc_t end_time;
        ct_addr_t sync_addr;
        uint64_t ticketNum;
    } ct_sync, *pct_sync;

    typedef struct _ct_barrier
    {
        bool onEnter;
        ct_tsc_t start_time;
        ct_tsc_t end_time;
        ct_addr_t sync_addr;
        uint64_t barrierNum;
    } ct_barrier, *pct_barrier;

    typedef struct _ct_task_create
    {
        uint32_t other_id; // child if id is creator, parent if id is created
        ct_tsc_t start_time;
        ct_tsc_t end_time;
        int64_t approx_skew; // 0 if parent, value if child, middle layer uses this as a flag
    } ct_task_create, *pct_task_create;

    typedef struct _ct_task_join
    {
        bool isExit;
        ct_tsc_t start_time;
        ct_tsc_t end_time;
        uint32_t other_id; // self if calling exit, child if calling join
    } ct_task_join, *pct_task_join;

    typedef struct _ct_buffer_info
    {
        uint32_t pos;
    } ct_buffer_info, *pct_buffer_info;

    typedef struct _ct_bulk_memory
    {
        uint64_t size;
        ct_addr_t dst_addr;
        ct_addr_t src_addr;
    } ct_bulk_memory, *pct_bulk_memory;

    typedef struct _ct_delay
    {
        ct_tsc_t start_time;
        ct_tsc_t end_time;
    } ct_delay, *pct_delay;

    typedef struct _ct_rank
    {
        uint32_t rank;
    } ct_rank, *pct_rank;

    typedef struct _ct_mpi_transfer
    {
        bool isSend, isBlocking;
        int comm_rank;
        int tag;
        ct_addr_t buf_ptr;
        size_t buf_size;
        ct_tsc_t start_time;
        ct_tsc_t end_time;
        ct_addr_t req_ptr; // Used when the request is non-blocking
    } ct_mpi_transfer, *pct_mpi_transfer;

    typedef struct _ct_mpi_wait
    {
        ct_addr_t req_ptr;
        ct_tsc_t start_time;
        ct_tsc_t end_time;
    } ct_mpi_wait, *pct_mpi_wait;

    typedef struct _ct_roi_event
    {
        ct_tsc_t start_time;
    } ct_roi_event, *pct_roi_event;

    //
    // There are two ways to combine objects with common fields.
    //   1) Common fields in a single type that is the first field
    //       in the other structs
    //   2) Union block of the other structs
    //
    //  Should a basic block contain an event header or should events be basic blocks?
    //
    typedef struct _ct_event {
        unsigned int contech_id;
        ct_event_id event_type;
        
        union {
            ct_basic_block      bb;
            ct_basic_block_info bbi;
            ct_barrier          bar;
            ct_sync             sy;
            ct_task_create      tc;
            ct_task_join        tj;
            ct_memory           mem;
            ct_buffer_info      buf;
            ct_bulk_memory      bm;
            ct_delay            dly;
            ct_rank             rank;
            ct_mpi_transfer     mpixf;
            ct_mpi_wait         mpiw;
            ct_roi_event        roi;
        };
    } ct_event, *pct_event;
    
    class EventLib
    {
        private:
            // DEBUG information
            uint64_t sum;
            uint64_t bufSum;
            unsigned int lastBufPos;
            unsigned int lastID;
            unsigned int lastBBID;
            unsigned int lastType;
            
            typedef struct _ct_event_debug
            {
                unsigned int sum, id, type;
                unsigned int data0, data1;
            } ct_event_debug, *pct_event_debug;
            
            ct_event_debug  ced[64];

            unsigned int cedPos ;

            unsigned int binInfo[1024];

            FILE* debug_file;

            // Per 9/17/13, event list will now contain a version event
            //   This will help with detecting compatibility issues
            unsigned int version ;

            // In version 1, we get currentID from the header events, instead
            // of from the individual events
            unsigned int currentID;

            // Interpret basic blocks using the following information
            unsigned int bb_count;
            
            typedef struct _internal_memory_op_info
            {
                char memFlags, size;
                unsigned short baseOp;
                int baseOffset;  // N.B. Offset can be negative
            } internal_memory_op_info, *pinternal_memory_op_info;

            typedef struct _internal_basic_block_info
            {
                unsigned int len;
                pinternal_memory_op_info mem_op_info;
            } internal_basic_block_info, *pinternal_basic_block_info;

            pinternal_basic_block_info bb_info_table;
            
            int unpack(uint8_t *buf, char const fmt[], ...);
            void dumpAndTerminate(FILE *fptr);
            void fread_check(void* x, size_t y, size_t z, FILE* a);
    
        public:
            EventLib();
            pct_event createContechEvent(FILE*);
            static void deleteContechEvent(pct_event);
            void displayContechEventDebugInfo();
            void displayContechEventDiagInfo();
            void displayContechEventStats();
            void resetEventLib();
    };
    
    
}

#endif

