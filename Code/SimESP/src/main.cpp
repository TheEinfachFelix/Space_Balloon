#include <Arduino.h>
#include "Sim800L/SIM800.hpp"
#include "Sim800L/SIM800Client.hpp"

SIM800 modem;
SIM800Client client(modem);

#define SimPin "2250"
#define PhoneNumber "+4916094842537"

void setup() {
  // Setup
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, 16, 17);
    modem.begin(Serial2, 9600, 23, 22); // DTR an Pin 23, RTS an Pin 22

    modem.enableDebug(Serial);   // Low-level Verkehr
    client.enableDebug(Serial);  // High-level Feedback

  // Run

    // TODO: READ GPS and send to sleep
    String gpsData = "Test";


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

    // TODO: ESP Sleep

}

void loop() {
    modem.loop();
}
