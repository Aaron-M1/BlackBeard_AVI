#include "pid_data.hpp"

const uint8_t solenoidPin = LED_BUILTIN;
pid_data my_pid_data;
bool testing = false;

void setup() {
  my_pid_data.setGCV(true);
  testing = my_pid_data.getGCV();
  pinMode(solenoidPin, OUTPUT);

}

void loop() {
  cout << testing << endl;
}

