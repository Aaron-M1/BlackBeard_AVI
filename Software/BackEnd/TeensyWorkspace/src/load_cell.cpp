#include "load_cell.hpp"

/*-------------------------------------------------------
@BPL-2, Avionics
This is the load cell header file
Creates a load cell object to use in foreign files
----------------------------------------------------------*/

load_cell::load_cell(int dout_pin, int sck_pin){ 
    //Constructor, defining important variables and performing any initital setup functions hear
    //Constructor run when new instance of class is created

    LOADCELL_DOUT_PIN = dout_pin;
    LOADCELL_SCK_PIN = sck_pin;

    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    delay(500);  
    scale.tare();
}

load_cell::~load_cell(void) {
    // Destructor, used to kill any instances of classes when they are unnecessary.
}

bool load_cell::isLoadCellReady() {
    //Checking if load cell is ready to read
    return scale.is_ready(); //True if ready, false if not
}

long load_cell::readLoadCell() {
    long reading = scale.read(); // Process the reading as needed
    return reading;
}

float load_cell::readLoadCellGrams() {
    long reading = scale.read() * 266;
    float grams = float(reading) / 100000.0; // Convert to grams (may need error tweaking)
    return grams;
}

float load_cell::readLoadCellNewtons() {
    float newtons = readLoadCellGrams() * 0.00980665f;   // g → N
    return newtons;
}