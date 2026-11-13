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
  EMatch match = EMatch(FIREPIN, 2500)

  const uint8_t FMVPIN;
  const bool FMV_DEF_STATE = False
  solenoid fmv = solenoid(FMVPIN, FMV_DEF_STATE)
}

void loop() {

}


void ignition_state() {

}

void safe_state() {

}