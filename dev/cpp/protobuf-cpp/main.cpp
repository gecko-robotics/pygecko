#include <iostream>
#include <string>
#include <sys/time.h>

#include "test.pb.h"
#include <google/protobuf/text_format.h>
#include <google/protobuf/util/time_util.h>

using namespace std;
using namespace google::protobuf::util;

void fillIMU(msg::IMU& imu, double ax, double ay, double az){
    msg::Vector v;
    v.set_x(ax);
    v.set_y(ay);
    v.set_z(az);
    *(imu.mutable_accel()) = v;
}

int main(){
    GOOGLE_PROTOBUF_VERIFY_VERSION;
    msg::Vector v;
    msg::IMU imu;

    v.set_x(5.0);
    v.set_y(15.0);
    v.set_z(25.0);

    *(imu.mutable_accel()) = v;

    v.set_x(15.0);
    v.set_y(215.0);
    v.set_z(325.0);

    *(imu.mutable_gyro()) = v;
    *(imu.mutable_mag()) = v;

    struct timeval tv;
    gettimeofday(&tv, NULL);
    google::protobuf::Timestamp timestamp;
    timestamp.set_seconds(tv.tv_sec);
    timestamp.set_nanos(tv.tv_usec * 1000);  // tv.tv_usec is micro seconds
    *(imu.mutable_timestamp()) = timestamp;

    cout << "IMU " << imu.DebugString() << endl;

    std::string serialized_update;
    imu.SerializeToString(&serialized_update);

    google::protobuf::ShutdownProtobufLibrary();
    return 0;
}
