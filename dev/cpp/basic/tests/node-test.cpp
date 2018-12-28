#include <iostream>
#include "node.hpp"
#include "time.hpp"
#include "gecko.hpp"

using namespace std;
using namespace gecko;

void test(void* args){
    Rate r(1);
    bool* ok = (bool*)args;
    while(*ok){
        cout << "." << flush;
        r.sleep();
    }
    cout << endl;
    cout << "bye space cowboy ..." << endl;
}

int main(){
    ThreadedNode n;
    n.run(&test);
    return 0;
}
