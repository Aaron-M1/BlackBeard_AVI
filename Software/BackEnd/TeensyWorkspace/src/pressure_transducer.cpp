# include "pressure_transducer.hpp"

/*-------------------------------------------------------
@BPL-2, Avionics
This is the pressure transducer source file
Defines variables and functions for the pressure transducer
----------------------------------------------------------*/

pressure_transducer::pressure_transducer(int pin)
{
   sensorPin = pin;
}

double pressure_transducer::get_pressure()
{
    sensor_value = analogRead(sensorPin);
    return sensor_value;
}