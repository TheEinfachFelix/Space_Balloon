#pragma once
#include <Arduino.h>
#include "config.hpp"
#include <SparkFun_AS7265x.h>

bool setUpSpec();
bool setUpSpec(int scl, int sda);
float readOne();
float* readAll();