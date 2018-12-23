#include <vector>
#include <msgpack.hpp>
#include <iostream>
#include <string>
#include <sstream>

using namespace std;

class Vector {
public:
    Vector(double,double,double);
    Vector(double*);
    double &operator[] (int);
    double data[3];
};

Vector::Vector(double x, double y, double z){
    data[0] = x;
    data[1] = y;
    data[2] = z;
}

Vector::Vector(double *v){}

double &Vector::operator[](int index){
    // if (index > 2) || (index < 0) {
    //     cout << "Array index out of bound, exiting" << endl;
    // }
    if (index == 0) return data[0];
    else if (index == 1) return data[1];
    else if (index == 2) return data[2];
    else cout << "Vector[" << index <<"] is out of bounds" << endl;
}


class MsgBase {
public:
    MsgBase(int);
    MsgBase();
    auto to_tuple();
    int timestamp;
};

MsgBase::MsgBase(int ts): timestamp(ts){}
MsgBase::MsgBase(){timestamp = 0;}  // FIXME: grab current time

class IMU: public MsgBase {
public:
    IMU(Vector&,Vector&,Vector&); // accel gyro mag
    auto to_tuple();
    Vector accels, gyros, mags;
};

IMU::IMU(Vector& a, Vector& g, Vector& m): accels(a), gyros(g), mags(m)
{}

auto IMU::to_tuple(){
    msgpack::type::tuple<int, double, double> src(1,3.14,4.123456789E-5);
    return src;
}

int main(void){
    cout << "hello" << endl;

    Vector a(1,2,3), b(3,4,5), c(6,7,8);
    IMU imu(a,b,c);

    msgpack::type::tuple<int, bool, std::string> src(1, true, "example");

    // serialize the object into the buffer.
    // any classes that implements write(const char*,size_t) can be a buffer.
    std::stringstream buffer;
    // msgpack::pack(buffer, src);
    msgpack::pack(buffer, imu.to_tuple());

    // send the buffer ...
    buffer.seekg(0);

    // deserialize the buffer into msgpack::object instance.
    std::string str(buffer.str());

    msgpack::object_handle oh = msgpack::unpack(str.data(), str.size());

    // deserialized object is valid during the msgpack::object_handle instance is alive.
    msgpack::object deserialized = oh.get();

    // msgpack::object supports ostream.
    std::cout << deserialized << std::endl;

    // std::cout << deserialized[0] << std::endl;

    // convert msgpack::object instance into the original type.
    // if the type is mismatched, it throws msgpack::type_error exception.
    msgpack::type::tuple<int, double, double> dst;
    deserialized.convert(dst);

    // or create the new instance
    msgpack::type::tuple<int, double, double> dst2 =
        deserialized.as<msgpack::type::tuple<int, double, double> >();
    return 0;
}
