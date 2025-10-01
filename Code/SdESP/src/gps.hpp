#pragma once
#include <Arduino.h>
#include "config.hpp"
#include <TinyGPS++.h>

bool setUpGPS();
bool setUpGPS(int rx, int tx);

// Hier musst du gucken weche methoden du brauchst