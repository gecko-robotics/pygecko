#include <iostream>
#include <thread>
#include "mbeacon.hpp"

using namespace std;

void bs(void){
    Search s;
    string ans = s.find("kevin");
    cout << "search returned: " << ans << endl;
}

void listener(void){
    Listener l;
    int ret = l.listen();
    cout << "listener returned: " << ret << endl;
}

int main(){
    cout << "START" << endl;

    thread l(listener);
    thread s(bs);
    // thread p2(pinger);
    // thread p3(pinger);

    l.join();
    s.join();
    // p2.join();
    // p3.join();

    return 0;
}
