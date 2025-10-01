#pragma once
#include <Arduino.h>
#include "config.hpp"
#include <Adafruit_ADS1x15.h>

bool setUpADC(int SCL, int SDA);
bool setUpADC();
int readADC(int channel);