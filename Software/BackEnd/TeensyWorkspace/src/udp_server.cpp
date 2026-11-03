#include "udp_server.hpp"

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
    if (size <= 0) return udp_message("", 0.0f);

    // Remember who sent it so send() knows where to stream data
    peerIp = udp.remoteIP();
    peerPort = udp.remotePort();
    peerKnown = true;

    char buf[64];
    int n = udp.read(buf, sizeof(buf) - 1);
    if (n <= 0) return;
    buf[n] = '\0';

    char *nl = strpbrk(buf, "\r\n");
    if (nl) *nl = '\0';

    std::string name = "blank";
    float value = 0.0f;

    handleLine(buf, name, value);
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

void udp_server::handleLine(char *line, std::string& name, float& value) //Parses incoming packets and executes commands, or sends an ack if the command is a setpoint
{
    char *colon = strchr(line, ':');
    if (!colon) return udp_message("", 0.0f); // malformed
    *colon = '\0';
    std::string name = line;
    float value = atof(colon + 1);

    // if (name == "setpoint") {
    //     setpoint = value;
    //     send("ack_setpoint", setpoint);
    // } else if (commandCallback) {
    //     commandCallback(name, value);
    // }
}