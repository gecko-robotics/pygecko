#include "node.hpp"
#include <thread>

using namespace gecko;
using namespace std;


// FIXME: pass other args
void Threaded::run(void(*f)(void* args)){
    thread t(f, &ok);
    t.join();
}

Node::Node(){
    ;
}
