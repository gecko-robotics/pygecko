#include <iostream>
#include <string>
#include <sstream>      // std::istringstream
#include <vector>
#include <map>
#include <arpa/inet.h>

using namespace std;
// typedef map<string,string> dictionary;

// std::map<std::string,std::string> getMsg(char* buf){
//     vector<string> container;
//
//     for (char *p = strtok(buf, ":"); p != NULL; p = strtok(NULL, ":")){
//         container.push_back( p );
//     }
//     dictionary dict;
//
//     vector<string> keys{"host","topic","address","port"};
//
//     for (int i=0; i < container.size(); ++i){
//         dict[keys[i]] = container[i];
//     }
//
//     return dict;
//
// }

bool validIpAddress(const string &ipAddress){
    struct sockaddr_in sa;
    // inet_pton returns -1 or 0 on error and 1 on success
    int result = inet_pton(AF_INET, ipAddress.c_str(), &(sa.sin_addr));
    return result == 1;
}

typedef struct {
    string host, topic, address, port;
} Msg_t;

class Msg {
public:
    // Msg(std::vector<std::string>);
    std::string host, topic, address, port;
};

class ReqMsg {
public:
    ReqMsg(){;}
    ReqMsg(std::vector<std::string>);
    std::string host, topic;
};

ReqMsg::ReqMsg(vector<string> v){
    host = v[0];
    topic = v[1];
}

class RepMsg: public ReqMsg {
public:
    RepMsg(std::vector<std::string>);
    std::string address, port;
};

RepMsg::RepMsg(vector<string> v){
    host = v[0];
    topic = v[1];
    if (validIpAddress(v[2])) address = v[2];
    else cout << "crap ip address" << endl;
    port = v[3];
}


// Msg_t getMsg2(char* buf){
//     vector<string> container;
//
//     for (char *p = strtok(buf, ":"); p != NULL; p = strtok(NULL, ":")){
//         container.push_back( p );
//     }
//     Msg_t dict;
//
//     if (container.size() == 4){
//         dict.host = container[0];
//         dict.topic = container[1];
//         dict.address = container[2];
//         dict.port = container[3];
//     }
//     else cout << "crap!!" << endl;
//
//     return dict;
// }

std::vector<std::string> split(const std::string& s, char delimiter)
{
   std::vector<std::string> tokens;
   std::string token;
   std::istringstream tokenStream(s);
   while (std::getline(tokenStream, token, delimiter))
   {
      tokens.push_back(token);
   }
   return tokens;
}


int main(){
    char buf[] = "dalek.buff:bob:1.2.3.4:1234";
    cout << buf << " " << sizeof(buf) << endl;

    // dictionary dict = getMsg(buf);
    // for (auto const& [k,v]: dict) cout << k << " -> " << v << endl;

    // Msg_t ans = getMsg2(buf);
    // cout << ans.host << ans.port << endl;

    vector<string> ans = split(buf, ':');
    for (auto const& s: ans) cout << s << endl;

    // Msg m(ans);
    // cout << m.host << " " << m.port << endl;

    vector<string> q = split("Dalek.string:pinkbunny",':');
    ReqMsg m(q);
    cout << m.host << " " << m.topic << endl;

    RepMsg n(ans);
    cout << n.host << " " << n.address << " " << n.topic << endl;
    // cout << buf << endl;

    return 0;
}
