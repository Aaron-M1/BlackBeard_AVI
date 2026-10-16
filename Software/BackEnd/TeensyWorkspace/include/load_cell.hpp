#pragma once
#include <string>
#include <cstdint>
#include "HX711.h"
/*-------------------------------------------------------
@BPL-2, Avionics
This is the load cell header file
Creates a load cell object to use in foreign files
----------------------------------------------------------*/

class load_cell {
    public:
        load_cell(int dout_pin, int sck_pin);
        ~load_cell(void);

        long readLoadCell();
        float readLoadCellGrams();
        
        bool isLoadCellReady();

    private:
        HX711 scale;

        const int LOADCELL_DOUT_PIN;
        const int LOADCELL_SCK_PIN;
};