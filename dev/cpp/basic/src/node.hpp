#pragma once

// #include <thread>
#include <string>
#include "signals.hpp"

namespace gecko {

class Threaded {
public:
    void run(void(*f)(void));
};

class Node: protected SigCapture {
public:
    Node();
};

class ThreadedNode: public Node, public Threaded {};

};
