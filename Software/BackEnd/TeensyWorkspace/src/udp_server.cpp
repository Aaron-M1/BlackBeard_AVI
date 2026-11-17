#include "udp_server.hpp"
#include <string.h>
#include <strings.h>   // strcasecmp

/*-------------------------------------------------------
@BPL-2, Avionics
This is the udp protocol source file
Creates a udp object that exchanges "name,value\n" packets with a PC client
----------------------------------------------------------*/
udp_server::udp_server(uint16_t port) //Constructor 
{
    localPort = port;
    peerPort = 0;
    peerKnown = false;
    setpoint = 0.0f;
}

udp_server::~udp_server(void) //Destructor
{
    udp.stop();
}

void udp_server::begin(IPAddress ip, IPAddress mask, IPAddress gateway) //Initializes the UDP object with needed params
{
    qindesign::network::Ethernet.begin(ip, mask, gateway);
    udp.begin(localPort);
}

udp_message udp_server::update() //Must run in the loop func, checks for incoming packets and handles them, also sends outgoing packets
{
    // One UDP packet is one whole message, so no framing buffer is needed
    int size = udp.parsePacket();
    if (size <= 0) return udp_message();

    // Remember who sent it so send() knows where to stream data
    peerIp = udp.remoteIP();
    peerPort = udp.remotePort();
    peerKnown = true;

    char buf[64];
    int n = udp.read(reinterpret_cast<uint8_t*>(buf), sizeof(buf) - 1);
    if (n <= 0) return udp_message();
    buf[n] = '\0';

    char *nl = strpbrk(buf, "\r\n");
    if (nl) *nl = '\0';

    std::string name;
    float value = 0.0f;

    if (!handleLine(buf, name, value)) return udp_message();   // malformed -> invalid message
    return udp_message(name, value);
}

void udp_server::send(const char *name, float value) //sends packets to verified clients
{
    if (!peerKnown) return;   // PC hasn't sent anything yet
    udp.beginPacket(peerIp, peerPort);
    udp.printf("%s,%.3f\n", name, value);
    udp.endPacket();
}

bool udp_server::hasPeer() //checks if someone is on the line
{
    return peerKnown;
}

bool udp_server::handleLine(char *line, std::string& name, float& value) //Parses "NAME:VALUE" lines; returns false if malformed
{
    char *colon = strchr(line, ':');
    if (!colon) {
        // Only the whole-packet commands are valid without a colon
        if (strcasecmp(line, "SafeState") == 0 || strcasecmp(line, "IgnitionState") == 0) {
            name = line;
            value = 0.0f;
            return true;
        }
        return false;
    }
    if (colon == line) return false; // empty name
    *colon = '\0';
    name = line;

    const char *action = colon + 1;
    if      (strcasecmp(action, "OPEN")  == 0) value = 1.0f;
    else if (strcasecmp(action, "CLOSE") == 0) value = 0.0f;
    else                                       value = atof(action);   // numeric values, e.g. setpoint
    return true;

    // if (name == "setpoint") {
    //     setpoint = value;
    //     send("ack_setpoint", setpoint);
    // } else if (commandCallback) {
    //     commandCallback(name, value);
    // }
}
