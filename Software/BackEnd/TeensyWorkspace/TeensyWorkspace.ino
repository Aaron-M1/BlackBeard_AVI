#include "pid_data.hpp"
#include "solenoid.hpp"
#include <Arduino.h>
#include "load_cell.hpp"

bool ishigh = False




const uint8_t solenoidPin = LED_BUILTIN;
pid_data my_pid_data;
bool testing = false;

void setup() {
  my_pid_data.setGCV(true);
  testing = my_pid_data.getGCV();
  pinMode(solenoidPin, OUTPUT);

  load_cell my_load_cell(1, 2);

}

void loop() {
  cout << testing << endl;  

  auto var = my_load_cell.readLoadCellGrams();
  printf("%f", var);
}

void togglesolenoid(pin)
{
  if (ishigh == false){
    digitalWrite(pin, HIGH)
    ishigh = true
  }
  else{
  digitalWrite(pin, LOW)
  ishigh = false
  }
}