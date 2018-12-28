#pragma once

// #include <thread>
#include <string>
#include "signals.hpp"

namespace gecko {

/*
Spins off a thread for a given function
*/
class Threaded: protected SigCapture {
public:
    void run(void(*f)(void*));
};

// what is the value of this?
class Node {
public:
    Node();
};

class ThreadedNode: public Node, public Threaded {};

};
