#include "gps.hpp"

TinyGPSPlus gps;
SoftwareSerial gpsSerial;

bool setUpGPS(int rx, int tx) {
    gpsSerial.begin(GPS_BAUD, SWSERIAL_8N1, rx, tx);

    unsigned long start = millis();
    while (millis() - start < 6000) {
        if (gpsSerial.available()) {
            updateGPS();
            if (gps.location.isValid()) {
                Serial.println("GPS fix detected");
                return true;
            }
        }
    }
    Serial.println("No GPS data received");
    return false;
}

void updateGPS()
{
  if (gpsSerial.available()) 
  {
    gps.encode(gpsSerial.read());
  }
}

double readLatitude() {
    if (gps.location.isValid()) {
        return gps.location.lat();
    }
    return NAN;
}

// Liest die aktuelle Länge
double readLongitude() {
    if (gps.location.isValid()) {
        return gps.location.lng();
    }
    return NAN;
}

// Liest die Höhe in Metern
double readAltitude() {
    if (gps.altitude.isValid()) {
        return gps.altitude.meters();
    }
    return NAN;
}

// Liest die Geschwindigkeit in km/h
double readSpeed() {
    if (gps.speed.isValid()) {
        Serial.println(gps.satellites.value());
        return gps.speed.kmph();
    }
    return NAN;
}



// Liest Datum und Uhrzeit vom GPS
// Gibt ein std::tm-Objekt zurück (lokale Zeit = UTC)
std::tm readDateTime() {
    std::tm timeinfo = {};

    if (gps.date.isValid() && gps.time.isValid()) {
        timeinfo.tm_year = gps.date.year() - 1900; // std::tm zählt ab 1900
        timeinfo.tm_mon  = gps.date.month() - 1;   // 0-basiert
        timeinfo.tm_mday = gps.date.day();
        timeinfo.tm_hour = gps.time.hour();
        timeinfo.tm_min  = gps.time.minute();
        timeinfo.tm_sec  = gps.time.second();
    } else {
        // Ungültig → setze 0-Zeit
        timeinfo = {};
    }

    return timeinfo;
}

