#include "pinout.h"
#include <Arduino_RouterBridge.h>

void setup() {
  pinMode(3, OUTPUT);
  Bridge.begin();
  Bridge.provide("read_ultrasound", read_ultrasound);
  Bridge.provide("write_ultrasound", write_ultrasound);
}

void write_ultrasound(uint8_t pin, uint8_t value){
  analogWrite(pin, value);
}

int read_ultrasound(uint8_t pin){
  return analogRead(pin);
}

void loop() {
  
}
