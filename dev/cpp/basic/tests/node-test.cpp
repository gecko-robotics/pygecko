#include <iostream>
#include "node.hpp"
#include "time.hpp"

using namespace std;
using namespace gecko;

void test(void){
    Rate r(1);
    while(true){
        cout << "." << flush;
        r.sleep();
    }
    cout << endl;
}

int main(){
    ThreadedNode n;
    n.run(&test);
    return 0;
}
