#pragma once
#include <string>
#include <cstdint>

class udp_message {
    public:
        udp_message(std::string& name, float value);
        ~udp_message(void);

        std::string getName();
        float getValue();

        void setName(std::string& name);
        void setValue(float value);

    private:
        std::string name;
        float value;
};