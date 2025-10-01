#include "sd.hpp"

bool setUpSD() {
  return setUpSD(sd_cs, sd_mosi, sd_miso, sd_sck);
}
bool setUpSD(int cs, int mosi, int miso, int sck) {
  return true;
}

bool writeFile(const char* path, const char* message) {
  return true;
}
bool appendFile(const char* path, const char* message) {
  return true;
}