#include "e_match.hpp"


/*-------------------------------------------------------
@BPL-2, Avionics
This is the EMatch header file
Creates an EMatch object to use in foreign files
----------------------------------------------------------*/


EMatch::EMatch(uint8_t firePin, uint16_t fireTimeMs){
    _firePin = firePin;
    _fireTimeMs = min(fireTimeMs, (uint16_t)3000);
    _firing = false;
    _fireStart = 0;
}
    

void EMatch::begin() {
    pinMode(_firePin, OUTPUT);
    digitalWrite(_firePin, LOW);
}

void EMatch::fire() {
    _fireStart = millis();
    digitalWrite(_firePin, HIGH);
    _firing = true;
}

void EMatch::off() {
    digitalWrite(_firePin, LOW);
    _firing = false;
}

void EMatch::update() {
    if (_firing && (millis() - _fireStart) >= _fireTimeMs) {
        off();
    }
}