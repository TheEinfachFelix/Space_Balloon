#pragma once
#include <Arduino.h>
#include "config.hpp"
#include <SPI.h>
#include <SD.h>

bool setUpSD();
bool setUpSD(int cs, int mosi, int miso, int sck);

bool writeFile(const char* path, const char* message);
bool appendFile(const char* path, const char* message);