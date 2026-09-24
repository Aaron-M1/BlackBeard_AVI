#include <iostream>

int main() {

}   

// just a code example idk
// I want to find a way to convert python to C++ or vise versa (-parker pevehouse)
// also why won't it run i'm dumb

//Trip = boolvalue or status that activates an alarm or a unsafe condition alert (eg. low pressure trip, leak trip)

//-GLOBAL INITIALIZE-//
std::string Status = "Safe"; // 
bool Interlock = true; //Only becomes false when in firing mode and ready to launch

double GCV = 0.00; // GN2 Check Valve
double GPR = 0.00; // GN2 Pressure Regulator
double GBS = 0.00; //GN2 Back Pressurizing Solenoid
double GPRV = 0.00; //GN2 Pressure Relief Valve
double FPS = 0.00; //Fuel Purging Solenoid
double FMV = 0.00; //Fuel Main Valve
double FCV = 0.00; //Fuel Check Valve
double OMV = 0.00; //Oxidizer Main Valve
double OCV = 0.00; //Oxidizer Check Valve
double CCV = 0.00; //Chiller Check Valve
double ORIPS = 0.00; //Oxidizer Run Tank Purge Solenoid
double CPS = 0.00; //Chiller Purge Solenoid
double CMS = 0.00; //Chiller Main Solenoid

double Ksi_2GAL = 0.0000; // 2Ksi tank fill in gallons
double ERT = 0.0000; // Ethanol Run tank fill in gallons
double N20RUN = 0.0000; // N20 run tank fill in gallons
double N20KBOT = 0.0000; // N20 K-Bottle tank fill in gallons

//-TRIPS-//
bool KSI_Trip = false; //If true: KSI Sensors not obtaining readings
bool ERT = false; //If true: ERT Sensors not obtaining readings
bool N20RUN = false; //If true: N20RUN Sensors not obtaining readings
bool N20KBOT = false; //If true: N20KBOT Sensors not obtaining readings