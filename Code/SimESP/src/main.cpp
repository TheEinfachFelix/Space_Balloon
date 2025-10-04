#include <Arduino.h>
#include "Sim800L/SIM800.hpp"
#include "Sim800L/SIM800Client.hpp"

SIM800 modem;
SIM800Client client(modem);

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, 16, 17);
    modem.begin(Serial2, 9600, 23, 22); // DTR an Pin 23, RTS an Pin 22

    modem.enableDebug(Serial);   // Low-level Verkehr
    client.enableDebug(Serial);  // High-level Feedback

    auto r = client.testAT();
    if (r.result == SIM800Result::SUCCESS) Serial.println("Modem OK");

    if (client.setPin("2250").result == SIM800Result::SUCCESS) {
        Serial.println("SIM unlocked");
    } else {
        Serial.println("SIM unlock failed or not needed");
    }


        auto r2 = client.testAT();
    if (r2.result == SIM800Result::SUCCESS) Serial.println("Modem OK");
    client.sleep(); // SIM800 in den Sleep schicken
        auto r3 = client.testAT();
    if (r3.result == SIM800Result::SUCCESS) Serial.println("Modem OK");

    delay(5000); // 5 Sekunden warten
        auto r4 = client.testAT();
    if (r4.result == SIM800Result::SUCCESS) Serial.println("Modem OK");
    client.wakeUp(); // SIM800 aufwecken
        auto r5 = client.testAT();
    if (r5.result == SIM800Result::SUCCESS) Serial.println("Modem OK");

    delay(2000); // 2 Sekunden warten
        auto r6 = client.testAT();
    if (r6.result == SIM800Result::SUCCESS) Serial.println("Modem OK");

    //CSQInfo csq;
    //if (client.getSignalQuality(csq)) {
    //    Serial.printf("Signal: RSSI=%d, BER=%d\n", csq.rssi, csq.ber);
    //}
//
    //CREGInfo creg;
    //if (client.getNetworkRegistration(creg)) {
    //    Serial.printf("Network: n=%d, stat=%d\n", creg.n, creg.stat);
    //}

    //client.sendSMS("+4916094842537", "Hello from ESP32!"); // <-- eigene Nummer eintragen
}

void loop() {
    modem.loop();
}
