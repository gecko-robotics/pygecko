#include "node.hpp"
#include <thread>

using namespace gecko;
using namespace std;

void Threaded::run(void(*f)(void)){
    thread t(f);
    t.join();
}

Node::Node(){
    ;
}
