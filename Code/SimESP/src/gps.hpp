#pragma once
#include <Arduino.h>
#include <TinyGPS++.h>
#include <ctime>

#define GPS_BAUD 9600

bool setUpGPS(int rx, int tx);
void updateGPS();

double readLatitude();
double readLongitude();
double readAltitude();
double readSpeed();
std::tm readDateTime();

// Hier musst du gucken weche methoden du brauchst