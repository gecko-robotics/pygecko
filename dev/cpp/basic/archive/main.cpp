
// #include <iostream>
// #include <thread>
// #include <chrono>
// #include <sstream>
// #include <stdio.h>
// #include <stdlib.h>
// #include <stdint.h>
// #include <time.h>
// #include <unistd.h>
// // copy header from here
// // https://github.com/zeromq/cppzmq
// #include "zmq.hpp"
//
// #include <msgpack.hpp>

// #define within(num) (int) ((float) num * random () / (RAND_MAX + 1.0))
// inline int within(int num){
//     return (int)((float) num * random () / (RAND_MAX + 1.0));
// }

using std::cout;
using std::endl;

// void server(int t){
//
//     // serializes this object.
//     std::vector<std::string> vec;
//     vec.push_back("Hello");
//     vec.push_back("MessagePack");
//
//     // serialize it into simple buffer.
//     msgpack::sbuffer sbuf;
//     msgpack::pack(sbuf, vec);
//
//     // cout<< sbuf << endl;
//
//     //  Prepare our context and publisher
//     zmq::context_t context (1);
//     zmq::socket_t publisher (context, ZMQ_PUB);
//     publisher.bind("tcp://0.0.0.0:5556");
//     // publisher.bind("ipc://weather.ipc");                // Not usable on Windows.
//
//     //  Initialize random number generator
//     // srandom ((unsigned) time (NULL));
//     uint16_t count = 0;
//     while (1) {
//
//         // int zipcode, temperature, relhumidity;
//
//         //  Get values that will fool the boss
//         // zipcode     = within (100000);
//         // temperature = within (215) - 80;
//         // relhumidity = within (50) + 10;
//
//         //  Send message to all subscribers
//         zmq::message_t message(20);
//         snprintf ((char *) message.data(), 20 ,
//             "%s %d", "33", count);
//         publisher.send(message);
//
//         snprintf ((char *) message.data(), 20 ,
//             "hello %d", count);
//         publisher.send(message);
//
//         count++;
//
//         // cout << "server: " << count << endl;
//
//         usleep(100000);
//
//     }
// }
//
// void client(int t){
//     zmq::context_t context (1);
//
//     //  Socket to talk to server
//     cout << "Collecting updates from weather server…\n" << std::endl;
//     zmq::socket_t subscriber (context, ZMQ_SUB);
//     subscriber.connect("tcp://localhost:5556");
//
//     //  Subscribe to zipcode, default is NYC, 10001
//     // const char *filter = "hi";
//     // subscriber.setsockopt(ZMQ_SUBSCRIBE, "hi", 2);
//     subscriber.setsockopt(ZMQ_SUBSCRIBE, "33", 2);
//
//     //  Process 100 updates
//     // int update_nbr;
//     // long total_temp = 0;
//     uint16_t count, topic;
//     for (int i = 0; i < 100; i++) {
//
//         zmq::message_t update;
//         // int zipcode, temperature, relhumidity;
//
//         subscriber.recv(&update);
//
//         std::istringstream iss(static_cast<char*>(update.data()));
//         iss >> topic >> count ;
//
//         printf(">> client topic: %d  count: %d\n", topic, count);
//
//         topic = 0;
//         count = 0;
//
//         usleep(1000000);
//     }
// }

int main(){
    std::cout << "start" << std::endl;
    // std::thread t1(server, 500);
    // std::thread t2(client, 3000);
    // t1.join();
    // t2.join();

    return 0;
}
