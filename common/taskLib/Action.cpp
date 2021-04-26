#include "Action.hpp"
using namespace contech;

MemoryAction::MemoryAction() {}
MemoryAction::MemoryAction(Action a) : data(a.data) {}
BasicBlockAction::BasicBlockAction() {}
BasicBlockAction::BasicBlockAction(Action a) : data(a.data) {}

Action::Action() {}
Action::Action(BasicBlockAction a) : data(a.data) {};
Action::Action(MemoryAction a) : data(a.data) {};
action_type Action::getType() const { return (action_type)type; }
bool Action::isMemOp() const { return type == action_type_mem_read || type == action_type_mem_write; }
bool Action::isMemoryAction() const { return type != action_type_basicBlock; }
bool Action::isBasicBlockAction() const { return type == action_type_basicBlock; }
bool Action::operator==(const Action& rhs) const { return data == rhs.data; }
bool Action::operator!=(const Action& rhs) const { return data != rhs.data; }
bool operator< (const Action& lhs, const Action& rhs){ return lhs.data < rhs.data; }
bool operator< (const MemoryAction& lhs, const MemoryAction& rhs){ return lhs.data < rhs.data; }
bool operator< (const BasicBlockAction& lhs, const BasicBlockAction& rhs){ return lhs.data < rhs.data; }
void Action::ac_str(FILE* fp){
	//fprintf(fp,"ac_str() called\n");
	switch (type)
    {
        case action_type_basicBlock:
        {
            BasicBlockAction bb = *this;
	    fprintf(fp," BB# %lu",bb.basic_block_id);
            break;
        }
        case action_type_mem_write:
        {
            MemoryAction mem = *this;
	    fprintf(fp," Mem_W %x",mem.addr);
            break;
        }
        case action_type_mem_read:
        {
            MemoryAction mem = *this;
	    fprintf(fp," Mem_R %x",mem.addr);
            break;
        }
        case action_type_malloc:
        {
            MemoryAction mem = *this;
	    fprintf(fp," malloc %x",mem.addr);
            break;
        }
        case action_type_size:
        {
            MemoryAction mem = *this;
	    fprintf(fp," of size %d",mem.addr);
            break;
        }
        case action_type_free:
        {
            MemoryAction mem = *this;
	    fprintf(fp," free %x",mem.addr);
            break;
        }

        case action_type_memcpy:
        {
            MemoryAction mem = *this;
	    fprintf(fp," memcpy addr %x",mem.addr);
            break;
        }
        
        default:
        {
	    fprintf(fp," UNKNOWN: %lu",data);
        }
}
fprintf(fp,"\n");
}
std::string Action::toString() const
{
    std::ostringstream out;
    out << std::showbase;
    switch (type)
    {
        case action_type_basicBlock:
        {
            BasicBlockAction bb = *this;
            out << " BB#" << bb.basic_block_id;
            break;
        }
        case action_type_mem_write:
        {
            MemoryAction mem = *this;
            out << " ST " << std::hex << mem.addr;
            break;
        }
        case action_type_mem_read:
        {
            MemoryAction mem = *this;
            out << " LD " << std::hex << mem.addr;
            break;
        }
        case action_type_malloc:
        {
            MemoryAction mem = *this;
            out << " malloc " << std::hex << mem.addr;
            break;
        }
        case action_type_size:
        {
            MemoryAction mem = *this;
            out << " of size " << mem.addr;
            break;
        }
        case action_type_free:
        {
            MemoryAction mem = *this;
            out << " free " << std::hex << mem.addr;
            break;
        }

        case action_type_memcpy:
        {
            MemoryAction mem = *this;
            out << " memcpy addr " << std::hex << mem.addr;
            break;
        }
        
        default:
        {
            out << " UNKNOWN: " << data;
        }
    }
    return out.str();
}

