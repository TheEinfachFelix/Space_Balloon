#include <Arduino.h>
#include "adc.hpp"
#include "config.hpp"
#include "gps.hpp"
#include "sd.hpp"
#include "spec.hpp"

void setup() {
  setUpADC();
  setUpGPS();
  setUpSD();
  setUpSpec();
}

void loop() {
  readADC(1);
  writeFile("/data.txt", "Test data\n");
  appendFile("/data.txt", "More test data\n");
  readAll();
  delay(10000);
}