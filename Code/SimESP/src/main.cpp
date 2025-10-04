#include <Arduino.h>
#include "Sim800L/SIM800.hpp"
#include "Sim800L/SIM800Client.hpp"

SIM800 modem;
SIM800Client client(modem);

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, 16, 17);
    modem.begin(Serial2);

    modem.enableDebug(Serial);   // Low-level Verkehr
    client.enableDebug(Serial);  // High-level Feedback

    auto r = client.testAT();
    if (r.result == SIM800Result::SUCCESS) Serial.println("Modem OK");

    if (client.setPin("2250").result == SIM800Result::SUCCESS) {
        Serial.println("SIM unlocked");
    } else {
        Serial.println("SIM unlock failed or not needed");
    }

    CSQInfo csq;
    if (client.getSignalQuality(csq)) {
        Serial.printf("Signal: RSSI=%d, BER=%d\n", csq.rssi, csq.ber);
    }

    CREGInfo creg;
    if (client.getNetworkRegistration(creg)) {
        Serial.printf("Network: n=%d, stat=%d\n", creg.n, creg.stat);
    }

    client.sendSMS("+4916094842537", "Hello from ESP32!"); // <-- eigene Nummer eintragen
}

void loop() {
    modem.loop();
}
