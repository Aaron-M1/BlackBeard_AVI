#include "pid_data.hpp"

/*-------------------------------------------------------
@BPL-2, Avionics
This is the p&id header file
Defines variables for valves, tanks, and sensors
See P&ID.jpeg in drive for more info
----------------------------------------------------------*/

pid_data::pid_data(void) {

        //Solenoid valves
        nps_open = true; // Defaults to open
        ops_open = true; // Defaults to open
        gbs_open = false; // Defaults to closed
        fmv_open = false; // Defaults to closed
        omv_open = false; // Defaults to closed


        //PRESSURE TRANDUCER VALUES
        pressure_1 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_2 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_3 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_4 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_5 = 0.0; //TODO: Figure out what valves pressure is being read from
}


void pid_data::setNPS(bool is_open) {
    nps_open = is_open;
}

void pid_data::setOPS(bool is_open) {
    ops_open = is_open;
}


void pid_data::setGBS(bool is_open) {
    gbs_open = is_open;
}

void pid_data::setFMV(bool is_open) {
    fmv_open = is_open;
}

void pid_data::setOMV(bool is_open) {
    omv_open = is_open;
}



void pid_data::setPressure1(double pressure) {
    pressure_1 = pressure;
}

void pid_data::setPressure2(double pressure) {
    pressure_2 = pressure;
}

void pid_data::setPressure3(double pressure) {
    pressure_3 = pressure;
}

void pid_data::setPressure4(double pressure) {
    pressure_4 = pressure;
}

void pid_data::setPressure5(double pressure) {
    pressure_5 = pressure;
}


bool pid_data::getNPS() {
    return nps_open;
}

bool pid_data::getOPS() {
    return ops_open;
}

bool pid_data::getGBS() {
    return gbs_open;
}

bool pid_data::getFMV() {
    return fmv_open;
}

bool pid_data::getOMV() {
    return omv_open;
}

double pid_data::getPressure1() {
    return pressure_1;
}

double pid_data::getPressure2() {
    return pressure_2;
}

double pid_data::getPressure3() {
    return pressure_3;
}

double pid_data::getPressure4() {
    return pressure_4;
}

double pid_data::getPressure5() {
    return pressure_5;
}


std::string pid_data::toString() {
    std::string s = "pid_data {\n";
    s += "  NPS open: " + std::string(nps_open ? "true" : "false") + "\n";
    s += "  OPS open: " + std::string(ops_open ? "true" : "false") + "\n";
    s += "  GBS open: " + std::string(gbs_open ? "true" : "false") + "\n";
    s += "  FMV open: " + std::string(fmv_open ? "true" : "false") + "\n";
    s += "  OMV open: " + std::string(omv_open ? "true" : "false") + "\n";
    s += "  Pressure 1: " + std::to_string(pressure_1) + "\n";
    s += "  Pressure 2: " + std::to_string(pressure_2) + "\n";
    s += "  Pressure 3: " + std::to_string(pressure_3) + "\n";
    s += "  Pressure 4: " + std::to_string(pressure_4) + "\n";
    s += "  Pressure 5: " + std::to_string(pressure_5) + "\n";
    s += "}";
    return s;
}

pid_data::~pid_data(void) {

}

