#include <Arduino.h>
#include "adc.hpp"
#include "config.hpp"
#include "gps.hpp"
#include "sd.hpp"
#include "spec.hpp"

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  Serial.println("Setup starting");
  setUpADC();
  setUpGPS();
  setUpSD();
  setUpSpec();
  
}

void loop() {
  Serial.println("Starting loop");
  readADC(1);
  writeFile("/data.txt", "Test data\n");
  appendFile("/data.txt", "More test data\n");
  readAll();
  Serial.println("Loop complete");
  delay(10000);
}