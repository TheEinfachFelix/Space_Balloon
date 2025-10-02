#include "adc.hpp"
Adafruit_ADS1115 ads;
bool setUpADC() {
  return setUpADC(adc_scl, adc_sda);
}

bool setUpADC(int SCL, int SDA){
  Wire.begin(SDA, SCL);
  return ads.begin();
   
}

int readADC(int channel) {
  if (channel < 0 || channel > 3) return 0; 
  return ads.readADC_SingleEnded(channel);
}