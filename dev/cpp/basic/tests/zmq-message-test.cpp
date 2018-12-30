#include <iostream>
#include "zmq.hpp"

using namespace std;

zmq::message_t func(zmq::message_t& m){
    cout << "m mem: " << m.data() << endl;
    string s(static_cast<char*>(m.data()), m.size());
    cout << "func m string: " << s << endl;

    zmq::message_t n((void*)"hello - 2", 9);
    cout << "func n mem: " << n.data() << endl;

    return n;
    // return zmq::message_t((void*)"hello - 2", 5);
}

int main(void){
    zmq::message_t m((void*)"Hello", 5);

    cout << "m mem: " << m.data() << endl;

    // zmq::message_t n = func(std::move(m));
    // zmq::message_t n = func(zmq::message_t((void*)"Helso", 5));
    zmq::message_t n = func(m);

    string s(static_cast<char*>(n.data()), n.size());
    cout << "n mem: " << n.data() << endl;
    cout << "string: " << s << endl;

    return 0;
}
