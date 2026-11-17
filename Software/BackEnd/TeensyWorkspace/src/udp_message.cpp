#include "udp_message.hpp"

udp_message::udp_message() : name(""), value(0.0f) {
}

udp_message::udp_message(const std::string& name, float value) {
    this->name = name;
    this->value = value;
}

udp_message::~udp_message(void) {
}

std::string udp_message::getName() const {
    return name;
}

float udp_message::getValue() const {
    return value;
}

bool udp_message::isValid() const {
    return !name.empty();
}

void udp_message::setName(const std::string& name) {
    this->name = name;
}

void udp_message::setValue(float value) {
    this->value = value;
}
