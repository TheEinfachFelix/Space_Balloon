#include "adc.hpp"

bool setUpADC() {
  return setUpADC(adc_scl, adc_sda);
}

bool setUpADC(int SCL, int SDA){
    return true;
}

int readADC(int channel) {
  return channel * 100;
}