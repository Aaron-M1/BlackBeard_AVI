#include "solenoid.hpp"

/*-------------------------------------------------------
@BPL-2, Avionics
This is the solenoid header file
Creates a solenoid object to use in foreign files
----------------------------------------------------------*/
solenoid::solenoid(uint8_t pin, bool default_state)
{
    defaultState = default_state;
    SOLENOID_PIN = pin;

    this->setState(defaultState);

}

void solenoid::togglesolenoid()
{
  if (isOpen == false){
    digitalWrite(SOLENOID_PIN, HIGH);
    isOpen = true;
  }
  else{
  digitalWrite(SOLENOID_PIN, LOW); 
  isOpen = false;
  }
}

void solenoid::setState(bool state){
    if (state == false){
        digitalWrite(SOLENOID_PIN, LOW);
        isOpen = false;
    }
    else{
        digitalWrite(SOLENOID_PIN, HIGH);
        isOpen = true;
    }
}
uint8_t solenoid::getPin()
{
    return SOLENOID_PIN;
}
bool solenoid::getState()
{
    return isOpen;
}