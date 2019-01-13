#include "gecko.hpp"
#include <string>
#include <thread>
#include <iostream>
#include "time.h"

using namespace std;


void pubt(void){
    gecko::init();

    Rate rate(2);

    Publisher *p = gecko::advertise("bob");

    while(gecko::ok()){
        zmq::message_t msg("hello",5);
        cout << msg << endl;
        p->pub(msg);
        rate.sleep();
    }

    delete p;
}


void callback(zmq::message_t& m){
    cout << m << endl;
}

void subt(void){
    gecko::init();
    // gecko::subscribe("bob", callback);
    // gecko::spin();
}

int main(int argc, char* argv[]){
    thread t1(pubt);
    thread t2(subt);

    t1.join();
    t2.join();

    return 0;
}
