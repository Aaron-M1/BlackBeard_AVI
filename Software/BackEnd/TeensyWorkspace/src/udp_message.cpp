#include "udp_message.hpp"

udp_message::udp_message(std::string& name, float value) {
    this->name = name;
    this->value = value;
}

udp_message::~udp_message(void) {
}

std::string udp_message::getName() {
    return name;
}

float udp_message::getValue() {
    return value;
}

void udp_message::setName(std::string& name) {
    this->name = name;
}

void udp_message::setValue(float value) {
    this->value = value;
}