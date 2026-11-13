#include <QNEthernet.h>

#include "pid_data.hpp"
#include "solenoid.hpp"
#include "load_cell.hpp"
#include "pressure_transducer.hpp"
#include "udp_server.hpp"
#include "udp_message.hpp"
#include "e_match.hpp"

void setup() {
  const uint8_t FIREPIN;
  const uint16_t FIRETIME = 2500;
  EMatch match = EMatch(FIREPIN, 2500);

  const uint8_t FMVPIN;   
  const bool FMV_DEF_STATE = False
  solenoid fmv = solenoid(FMVPIN, FMV_DEF_STATE)

  const unit8_t NPSPIN;
  const bool NPS_DEF_STATE = True
  solenoid nps = solenoid(NPSPIN, NPS_DEF_STATE)

  const unit8_t OPSPIN;
  const bool OPS_DEF_STATE = True
  solenoid ops = solenoid(OPSPIN, OPS_DEF_STATE)

  const unit8_t GBSPIN;
  const bool GBS_DEF_STATE = False
  solenoid gps = solenoid(GBSPIN, GBS_DEF_STATE)

  const unit8_t OMVPIN;
  const bool OMV_DEF_STATE = False
  solenoid omv = solenoid(OMVPIN, OMV_DEF_STATE)

  const
}

void loop() {

}


void ignition_state(EMatch _match, solenoid _fmv, solenoid _omv) {
  _match.fire();
  _match.update();
  delay(500);
  _fmv.setState(True);
  _omv.setState(True);
  delay(6000);
  _fmv.setState(False);

}

void safe_state() {

}