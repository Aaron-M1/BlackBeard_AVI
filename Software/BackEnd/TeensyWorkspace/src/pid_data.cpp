#include "pid_data.hpp"

/*-------------------------------------------------------
@BPL-2, Avionics
This is the p&id header file
Defines variables for valves, tanks, and sensors
See P&ID.jpeg in drive for more info
----------------------------------------------------------*/

pid_data::pid_data(void) {


        status = "Safe"; // 
        Interlock = true; //Only becomes false when in firing mode and ready to launch

        //VALVE BOOLEANS
        gcv_open = false; // GN2 Check Valve
        gpr_open = false; // GN2 Pressure Regulator
        gbp_open = false; //GN2 Back Pressurizing Solenoid
        fps_open = false; //Fuel Purging Solenoid
        fmv_open = false; //Fuel Main Valve
        fcv_open = false; //Fuel Check Valve
        omv_open = false; //Oxidizer Main Valve
        ocv_open = false; //Oxidizer Check Valve
        ccv_open = false; //Chiller Check Valve
        orips_open = false; //Oxidizer Run Tank Purge Solenoid
        cps_open = false; //Chiller Purge Solenoid
        cms_open = false; //Chiller Main Solenoid

        //PRESSURE TRANDUCER VALUES
        pressure_1 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_2 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_3 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_4 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_5 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_6 = 0.0; //TODO: Figure out what valves pressure is being read from
        pressure_7 = 0.0; //TODO: Figure out what valves pressure is being read from

        //THERMOCOUPLE VALUES
        n_thermocouple = 0.0; //Temperature from N20 run tank

        //TANK VOLUMES
        ksi_volume = 0.0000; // 2Ksi tank fill in gallons or liters
        ert_volume = 0.0000; // Ethanol Run tank fill in gallons or liters
        n_run_volume = 0.0000; // N20 run tank fill in gallons or liters
        n_kbottle_volume = 0.0000; // N20 K-Bottle tank fill in gallons or liters

        //CHECK-ALERT SYSTEMS
        ksi_online = false; //If true: KSI Sensors not obtaining readings
        ert_online = false; //If true: ERT Sensors not obtaining readings
        n_run_online = false; //If true: N20RUN Sensors not obtaining readings
        n_kbottle_online = false; //If true: N20KBOT Sensors not obtaining readings
}

void pid_data::setStatus(const std::string& status_input) {
    status = status_input;
}

void pid_data::setInterlock(bool interlock_input) {
    Interlock = interlock_input;
}

void pid_data::setGCV(bool is_open) {
    gcv_open = is_open;
}

void pid_data::setGPR(bool is_open) {
    gpr_open = is_open;
}

void pid_data::setGBP(bool is_open) {
    gbp_open = is_open;
}

void pid_data::setFPS(bool is_open) {
    fps_open = is_open;
}

void pid_data::setFMV(bool is_open) {
    fmv_open = is_open;
}

void pid_data::setFCV(bool is_open) {
    fcv_open = is_open;
}

void pid_data::setOMV(bool is_open) {
    omv_open = is_open;
}

void pid_data::setOCV(bool is_open) {
    ocv_open = is_open;
}

void pid_data::setCCV(bool is_open) {
    ccv_open = is_open;
}

void pid_data::setORIPS(bool is_open) {
    orips_open = is_open;
}

void pid_data::setCPS(bool is_open) {
    cps_open = is_open;
}

void pid_data::setCMS(bool is_open) {
    cms_open = is_open;
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

void pid_data::setPressure6(double pressure) {
    pressure_6 = pressure;
}

void pid_data::setPressure7(double pressure) {
    pressure_7 = pressure;
}

void pid_data::setNThermocouple(double temperature) {
    n_thermocouple = temperature;
}

void pid_data::setKSIVolume(double volume) {
    ksi_volume = volume;
}

void pid_data::setERTVolume(double volume) {
    ert_volume = volume;
}

void pid_data::setNRunVolume(double volume) {
    n_run_volume = volume;
}

void pid_data::setNKBottleVolume(double volume) {
    n_kbottle_volume = volume;
}

void pid_data::setKSIOnline(bool is_online) {
    ksi_online = is_online;
}

void pid_data::setERTOnline(bool is_online) {
    ert_online = is_online;
}

void pid_data::setNRunOnline(bool is_online) {
    n_run_online = is_online;
}

void pid_data::setNKBottleOnline(bool is_online) {
    n_kbottle_online = is_online;
}

std::string pid_data::getStatus() {
    return status;
}

bool pid_data::getInterlock() {
    return Interlock;
}

bool pid_data::getGCV() {
    return gcv_open;
}

bool pid_data::getGPR() {
    return gpr_open;
}

bool pid_data::getGBP() {
    return gbp_open;
}

bool pid_data::getFPS() {
    return fps_open;
}

bool pid_data::getFMV() {
    return fmv_open;
}

bool pid_data::getFCV() {
    return fcv_open;
}

bool pid_data::getOMV() {
    return omv_open;
}

bool pid_data::getOCV() {
    return ocv_open;
}

bool pid_data::getCCV() {
    return ccv_open;
}

bool pid_data::getORIPS() {
    return orips_open;
}

bool pid_data::getCPS() {
    return cps_open;
}

bool pid_data::getCMS() {
    return cms_open;
}

bool pid_data::getKSIOnline() {
    return ksi_online;
}

bool pid_data::getERTOnline() {
    return ert_online;
}

bool pid_data::getNRunOnline() {
    return n_run_online;
}

bool pid_data::getNKBottleOnline() {
    return n_kbottle_online;
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

double pid_data::getPressure6() {
    return pressure_6;
}

double pid_data::getPressure7() {
    return pressure_7;
}

double pid_data::getNThermocouple() {
    return n_thermocouple;
}

double pid_data::getKSIVolume() {
    return ksi_volume;
}

double pid_data::getERTVolume() {
    return ert_volume;
}

double pid_data::getNRunVolume() {
    return n_run_volume;
}

double pid_data::getNKBottleVolume() {
    return n_kbottle_volume;
}





pid_data::~pid_data(void) {

}

