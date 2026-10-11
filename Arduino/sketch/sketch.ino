#include "pinout.h"
#include <Arduino_RouterBridge.h>

void setup() {
  pinMode(SERVO_1, OUTPUT);
  pinMode(SERVO_2, OUTPUT);
  pinMode(ULTRASOUND_TRIGGER, INPUT);
  pinMode(ULTRASOUND_ECHO, OUTPUT);
  Bridge.begin();
  Bridge.provide("read_ultrasound", trigger);
  Bridge.provide("write_ultrasound", echo);
  Bridge.provide("servo", servo);
}

void servo(uint8_t servo, uint8_t value){
  analogWrite(servo == 1 ? SERVO_1: SERVO_2, value);
}

void echo(uint8_t value){
  analogWrite(ULTRASOUND_ECHO, value);
}

int trigger(){
  return analogRead(ULTRASOUND_TRIGGER);
}

void loop() {
  
}
