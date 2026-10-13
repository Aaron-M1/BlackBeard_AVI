#include "pid_data.hpp"

pid_data my_pid_data;

 bool testing = false;

void setup() {
  my_pid_data.setGCV(true);
  testing = my_pid_data.getGCV();


}

void loop() {
  cout << testing << endl;
}
