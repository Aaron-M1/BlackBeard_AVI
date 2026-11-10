#include "udp_server.hpp"
#include "udp_message.hpp"
//Broken
int main(){

    srv udp_server(5000);
    server.begin(127.0.0.1 ,255.255.255.255 ,10.128.13.13);

    for (int i = 0; i < 5; i++) {

        server.send("string", 23.0);
        udp_message update = server.update();
        str = update.getName();
        val = update.getValue();
        std::cout << str << " " << val << std::endl;

        return 0;
    }



}