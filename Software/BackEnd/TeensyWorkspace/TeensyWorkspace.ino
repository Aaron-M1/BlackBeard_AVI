#include <QNEthernet.h>

#include "pid_data.hpp"
#include "solenoid.hpp"
#include "load_cell.hpp"
#include "pressure_transducer.hpp"
#include "udp_server.hpp"
#include "udp_message.hpp"
#include "e_match.hpp"

//IgnitionState
//SafeState

//FMV:OPEN
//NPS:CLOSE

enum IgnitionStep { IGN_IDLE, IGN_MATCH_WAIT, IGN_BURN };

IgnitionStep ignStep = IGN_IDLE;
uint32_t ignStepStart = 0;

const uint32_t MATCH_WAIT_MS = 500;
const uint32_t BURN_MS       = 6000;

const IPAddress TEENSY_IP(192, 168, 1, 177);  
const IPAddress SUBNET_MASK(255, 255, 255, 0);
const IPAddress GATEWAY(192, 168, 1, 1);

pid_data pid = pid_data();

const uint8_t FIREPIN;
const uint16_t FIRETIME = 2500;
EMatch match = EMatch(FIREPIN, FIRETIME);

const uint8_t FMVPIN;   
const bool FMV_DEF_STATE = false;
solenoid fmv = solenoid(FMVPIN, FMV_DEF_STATE);

const uint8_t NPSPIN;
const bool NPS_DEF_STATE = true;
solenoid nps = solenoid(NPSPIN, NPS_DEF_STATE);

const uint8_t OPSPIN;
const bool OPS_DEF_STATE = true;
solenoid ops = solenoid(OPSPIN, OPS_DEF_STATE);

const uint8_t GBSPIN;
const bool GBS_DEF_STATE = false;
solenoid gbs = solenoid(GBSPIN, GBS_DEF_STATE);

const uint8_t OMVPIN;
const bool OMV_DEF_STATE = false;
solenoid omv = solenoid(OMVPIN, OMV_DEF_STATE);

// ---- UDP command handling ----
const uint16_t UDP_PORT = 5000;   // TODO: set to the real port
udp_server server = udp_server(UDP_PORT);

struct SolEntry { const char *name; solenoid *sol; };
SolEntry sols[] = {
  {"FMV", &fmv},
  {"NPS", &nps},
  {"OPS", &ops},
  {"GBS", &gbs},
  {"OMV", &omv},
};

const int P1PIN;
pressure_transducer p1 = pressure_transducer(P1PIN);

const int P2PIN;
pressure_transducer p2 = pressure_transducer(P2PIN);

const int P3PIN;
pressure_transducer p3 = pressure_transducer(P3PIN);

const int P4PIN;
pressure_transducer p4 = pressure_transducer(P4PIN);

const int P5PIN;
pressure_transducer p5 = pressure_transducer(P5PIN);



void setup() {
  server.begin(TEENSY_IP, SUBNET_MASK, GATEWAY);
}

void loop() {
  
  if (!server.hasPeer())
  {
    safe_state();
  }
  else
  {
    handleMessage(server.update());
    ignition_update(); 

    pid.setFMV(fmv.getState());
    pid.setNPS(nps.getState());
    pid.setOPS(ops.getState());
    pid.setGBS(gbs.getState());
    pid.setOMV(omv.getState());

    pid.setPressure1(p1.getPressure());
    pid.setPressure2(p2.getPressure());
    pid.setPressure3(p3.getPressure());
    pid.setPressure4(p4.getPressure());
    pid.setPressure5(p5.getPressure());

    sendPidData();
  }

}

// Applies one parsed "NAME:OPEN|CLOSE" message (OPEN -> 1.0, CLOSE -> 0.0)
void handleMessage(const udp_message &msg) {
  if (!msg.isValid()) return;

  std::string name = msg.getName();
  if (strcasecmp(name.c_str(), "SafeState") == 0)     { safe_state();     return; }
  if (strcasecmp(name.c_str(), "IgnitionState") == 0) { ignition_state(); return; }

  solenoid *s = findSolenoid(name.c_str());
  if (!s) return;                       // unknown solenoid -> ignore
  s->setState(msg.getValue() != 0.0f);
}

solenoid* findSolenoid(const char *name) {
  for (auto &e : sols)
    if (strcasecmp(e.name, name) == 0) return e.sol;
  return nullptr;
}

// Sends every P&ID value as its own "NAME,value" packet (valves: 1 = open, 0 = closed)
void sendPidData() {
  server.send("FMV", pid.getFMV() ? 1.0f : 0.0f);
  server.send("NPS", pid.getNPS() ? 1.0f : 0.0f);
  server.send("OPS", pid.getOPS() ? 1.0f : 0.0f);
  server.send("GBS", pid.getGBS() ? 1.0f : 0.0f);
  server.send("OMV", pid.getOMV() ? 1.0f : 0.0f);

  server.send("P1", pid.getPressure1());
  server.send("P2", pid.getPressure2());
  server.send("P3", pid.getPressure3());
  server.send("P4", pid.getPressure4());
  server.send("P5", pid.getPressure5());
}

void ignition_state() {              
  if (ignStep != IGN_IDLE) return;   // ignore a repeat while already running
  match.fire();
  ignStep = IGN_MATCH_WAIT;
  ignStepStart = millis();
}

void safe_state() {
  ignStep = IGN_IDLE; 
  match.off();
  fmv.setDefault();
  nps.setDefault();
  ops.setDefault();
  gbs.setDefault();
  omv.setDefault();
}

void ignition_update() {
  match.update();                    // always service the match timer
  uint32_t elapsed = millis() - ignStepStart;

  switch (ignStep) {
    case IGN_IDLE:
      break;
    case IGN_MATCH_WAIT:
      if (elapsed >= MATCH_WAIT_MS) {
        fmv.setState(true);
        omv.setState(true);
        ignStep = IGN_BURN;
        ignStepStart = millis();
      }
      break;
    case IGN_BURN:
      if (elapsed >= BURN_MS) {
        fmv.setState(false);
        ignStep = IGN_IDLE;
      }
      break;
  }
}