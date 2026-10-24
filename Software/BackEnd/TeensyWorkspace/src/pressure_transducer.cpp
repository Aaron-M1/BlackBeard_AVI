# include "pressure_transducer.hpp"


pressure_transducer::pressure_transducer(int pin)
{
   int sensor_pin = pin;
}

double pressure_transducer::get_pressure();
{
    sensor_value = analogRead(sensorPin);
    return sensor_value;
}