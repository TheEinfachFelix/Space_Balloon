#include <Arduino.h>
#include "Sim800L/SIM800.hpp"
#include "Sim800L/SIM800Client.hpp"
#include "gps.hpp"

SIM800 modem;
SIM800Client client(modem);

#define SimPin "2250"
#define PhoneNumber "+4916094842537"

#define uS_TO_S_FACTOR 1000000ULL  // Conversion factor for micro seconds to seconds
#define TIME_TO_SLEEP  60           // Time ESP32 will go to sleep (in seconds)


void setup() {
  // Setup
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, 16, 17);
    modem.begin(Serial2, 9600, 23, 22); // DTR an Pin 23, RTS an Pin 22
    setUpGPS(34, 32);

    modem.enableDebug(Serial);   // Low-level Verkehr
    client.enableDebug(Serial);  // High-level Feedback


    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);

    // Run
    String gpsData = "Lon: " + String(readLongitude(), 6) + ", Lat: " + String(readLatitude(), 6) + ", Alt: " + String(readAltitude(), 1) + "m, Speed: " + String(readSpeed(), 1) + "km/h";
    Serial.println(gpsData);

    client.wakeUp();
    delay(500);

    auto r = client.testAT();
    if (r.result == SIM800Result::SUCCESS) Serial.println("Modem OK");
    else
    {
      modem.reset();
      delay(5000);
      r = client.testAT();
      if (r.result == SIM800Result::SUCCESS) Serial.println("Modem OK after reset");
      else Serial.println("Modem not responding");
    }

    if (client.setPin(SimPin).result == SIM800Result::SUCCESS) {
        Serial.println("SIM unlocked");
        delay(1000);
    } else {
        Serial.println("SIM unlock failed or not needed");
    }

    if(client.sendSMS(PhoneNumber, gpsData).result != SIM800Result::SUCCESS) {
        Serial.println("SMS send failed");
        client.sendSMS(PhoneNumber, gpsData);
    }

    client.sleep();
    Serial.println("Modem to sleep");

    delay(500);
    Serial.println("Going to sleep now");
    Serial.flush();
    esp_deep_sleep_start();

}

void loop() {
    modem.loop();
}
