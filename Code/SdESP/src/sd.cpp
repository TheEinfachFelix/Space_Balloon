#include "sd.hpp"

SPIClass sdSPI(VSPI);

bool setUpSD() {
  return setUpSD(sd_cs, sd_mosi, sd_miso, sd_sck);
}
bool setUpSD(int cs, int mosi, int miso, int sck) {
  sdSPI.begin(sck, miso, mosi, cs);
  return SD.begin(cs, sdSPI);
}

bool writeFile(const char* path, const char* message) {
  File file = SD.open(path, FILE_WRITE);
  if (!file) return false;
  file.println(message);
  file.close();
  return true;
}

bool appendFile(const char* path, const char* message) {
  File file = SD.open(path, FILE_WRITE);
  if (!file) return false;
  file.seek(file.size());
  file.println(message);
  file.close();
  return true;
}