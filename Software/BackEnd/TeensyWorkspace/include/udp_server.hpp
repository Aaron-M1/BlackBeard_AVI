
#pragma once
#include <Arduino.h>
#include <QNEthernet.h>
#include "udp_message.hpp"
/*-------------------------------------------------------
@BPL-2, Avionics
This is the udp protocol header file
Creates a udp object that exchanges "name,value\n" packets with a PC client
----------------------------------------------------------*/

class udp_server {
    public:
        // Called for every received packet that isn't handled internally ("setpoint")
        typedef void (*command_callback)(const String &name, float value);

        udp_server(uint16_t port);
        ~udp_server(void);

        void begin(IPAddress ip, IPAddress mask, IPAddress gateway);
        udp_message update();   // call every loop(): reads at most one packet, never blocks

        void send(const char *name, float value);
        void onCommand(command_callback callback);

        bool hasPeer();

    private:
        void handleLine(char *line, std::string& name, float& value);

        qindesign::network::EthernetUDP udp;
        uint16_t localPort;
        IPAddress peerIp;
        uint16_t peerPort;
        bool peerKnown;
        float setpoint;
        command_callback commandCallback;

        udp_message message;
};