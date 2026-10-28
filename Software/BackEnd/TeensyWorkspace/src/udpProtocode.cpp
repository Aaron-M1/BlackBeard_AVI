#include "udp_protocol.hpp"

/*-------------------------------------------------------
@BPL-2, Avionics
This is the udp protocol source file
Creates a udp object that exchanges "name,value\n" packets with a PC client
----------------------------------------------------------*/
udp_protocol::udp_protocol(uint16_t port)
{
    localPort = port;
    peerPort = 0;
    peerKnown = false;
    setpoint = 0.0f;
    commandCallback = nullptr;
}

udp_protocol::~udp_protocol(void)
{
}

void udp_protocol::begin(IPAddress ip, IPAddress mask, IPAddress gateway)
{
    qindesign::network::Ethernet.begin(ip, mask, gateway);
    udp.begin(localPort);
}

void udp_protocol::update()
{
    // One UDP packet is one whole message, so no framing buffer is needed
    int size = udp.parsePacket();
    if (size <= 0) return;

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
    handleLine(buf);
}

void udp_protocol::send(const char *name, float value)
{
    if (!peerKnown) return;   // PC hasn't sent anything yet
    udp.beginPacket(peerIp, peerPort);
    udp.printf("%s,%.3f\n", name, value);
    udp.endPacket();
}

void udp_protocol::onCommand(command_callback callback)
{
    commandCallback = callback;
}

float udp_protocol::getSetpoint()
{
    return setpoint;
}

bool udp_protocol::hasPeer()
{
    return peerKnown;
}

void udp_protocol::handleLine(char *line)
{
    char *comma = strchr(line, ',');
    if (!comma) return;                          // malformed
    *comma = '\0';
    String name = line;
    float value = atof(comma + 1);

    if (name == "setpoint") {
        setpoint = value;
        send("ack_setpoint", setpoint);
    } else if (commandCallback) {
        commandCallback(name, value);
    }
}