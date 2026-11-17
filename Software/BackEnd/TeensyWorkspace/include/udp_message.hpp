#pragma once
#include <string>
#include <cstdint>

class udp_message {
    public:
        udp_message();
        udp_message(const std::string& name, float value);
        ~udp_message(void);

        std::string getName() const;
        float getValue() const;
        bool isValid() const;   // false when no packet / malformed packet

        void setName(const std::string& name);
        void setValue(float value);

    private:
        std::string name;
        float value;
};
