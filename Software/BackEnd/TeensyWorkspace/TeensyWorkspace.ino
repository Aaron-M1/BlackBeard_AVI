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





pid_data pid = pid_data()

const uint8_t FIREPIN;
const uint16_t FIRETIME = 2500;
EMatch match = EMatch(FIREPIN, 2500);

const uint8_t FMVPIN;   
const bool FMV_DEF_STATE = False;
solenoid fmv = solenoid(FMVPIN, FMV_DEF_STATE);

const unit8_t NPSPIN;
const bool NPS_DEF_STATE = True;
solenoid nps = solenoid(NPSPIN, NPS_DEF_STATE);

const unit8_t OPSPIN;
const bool OPS_DEF_STATE = True;
solenoid ops = solenoid(OPSPIN, OPS_DEF_STATE);

const unit8_t GBSPIN;
const bool GBS_DEF_STATE = False;
solenoid gbs = solenoid(GBSPIN, GBS_DEF_STATE);

const unit8_t OMVPIN;
const bool OMV_DEF_STATE = False;
solenoid omv = solenoid(OMVPIN, OMV_DEF_STATE);

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

}

void loop() {
  pid.setFMV(fmv.getState());
  pid.setNPS(nps.getState());
  pid.setOPS(ops.getState());
  pid.setGBS(gbs.setState());
  pid.setOMV(omv.setState());

  pid.setPressure1(p1.getPressure());
  pid.setPressure2(p2.getPressure());
  pid.setPressure3(p3.getPressure());
  pid.setPressure4(p4.getPressure());
  pid.setPressure5(p5.getPressure());
}


void ignition_state() {
  match.fire();
  match.update();
  delay(500);
  fmv.setState(True);
  omv.setState(True);
  delay(6000);
  fmv.setState(False);
}

void safe_state() {
  fmv.setDefault();
  nps.setDefault();
  ops.setDefault();
  gbs.setDefault();
  omv.setDefault();
}