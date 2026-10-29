#include <QNEthernet.h>
using namespace qindesign::network;

//This is all vibecoded lmao we will need to make this actually good next week


EthernetServer server(5000);
EthernetClient client;

String rxBuf;
float loadGrams = 0.0f;       // stand-in for your load cell reading
float setpoint  = 0.0f;       // value the PC can set
uint32_t lastSend = 0;

void handleLine(const String &line) {
  int comma = line.indexOf(',');
  if (comma < 0) return;                       // malformed
  String name = line.substring(0, comma);
  float value = line.substring(comma + 1).toFloat();

  if (name == "setpoint") {
    setpoint = value;
    client.printf("ack_setpoint,%.3f\n", setpoint);
  } else if (name == "fire") {
    // solenoid.fire(value);
    client.printf("ack_fire,%.3f\n", value);
  }
}

void setup() {
  Serial.begin(115200);
  Ethernet.begin(IPAddress(192,168,1,100),
                 IPAddress(255,255,255,0),
                 IPAddress(192,168,1,1));
  server.begin();
}

void loop() {
  // Accept a new connection if we don't have a live one
  if (!client || !client.connected()) {
    EthernetClient c = server.accept();   // use server.available() on older versions
    if (c) { client = c; rxBuf = ""; }
  }

  if (client && client.connected()) {
    // Receive: collect bytes until newline
    while (client.available()) {
      char ch = client.read();
      if (ch == '\n') { handleLine(rxBuf); rxBuf = ""; }
      else if (ch != '\r') rxBuf += ch;
    }

    // Send: stream the load value every 500 ms
    if (millis() - lastSend >= 500) {
      lastSend = millis();
      loadGrams += 0.1f;                   // fake data
      client.printf("load,%.3f\n", loadGrams);
      client.flush();
    }
  }
}