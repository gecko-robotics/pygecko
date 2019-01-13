#pragma once

#include <string>
// #include <memory>
// #include <iostream>
// #include <cstdio>
// #include <vector>


// https://stackoverflow.com/a/26221725/5374768
// template<typename ... Args>
// std::string fmtstr( const std::string& format, Args ... args ){
//     size_t size = snprintf( nullptr, 0, format.c_str(), args ... ) + 1; // Extra space for '\0'
//     std::unique_ptr<char[]> buf( new char[ size ] );
//     snprintf( buf.get(), size, format.c_str(), args ... );
//     return std::string( buf.get(), buf.get() + size - 1 ); // We don't want the '\0' inside
// }

inline std::string zmqTCP(std::string addr, std::string port){
    // return fmtstr("tcp://%s:%s", addr.c_str(), port.c_str());
    return std::string("tcp://") + addr + std::string(":") + port;
}

inline std::string zmqTCP(std::string addr){
    // return fmtstr("tcp://%s:*", addr.c_str());
    return std::string("tcp://") + addr + std::string(":*");
}
//
// // forgot where on stack exchange I found this
// std::vector<std::string> split(const std::string& s, char delimiter)
// {
//    std::vector<std::string> tokens;
//    std::string token;
//    std::istringstream tokenStream(s);
//    while (std::getline(tokenStream, token, delimiter))
//    {
//       tokens.push_back(token);
//    }
//    return tokens;
// }
