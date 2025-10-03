#include <Arduino.h>
#include "Sim800L/Sim800.hpp"
#include <SoftwareSerial.h> 
             

#define GSM_RX  16
#define GSM_TX  17
#define GSM_RST 22
#define GSM_delay 23

Sim800L GSM(GSM_RX, GSM_TX);

char* text;
char* number;
bool error; 
char* Inhalt_SMS;

void setup() {
  GSM.begin(); 			
  GSM.setDebugMode(true);
  Serial.begin(9600);

  String pin = "2250";
  if (GSM.checkStatus().indexOf("READY") == -1) {
      if (GSM.setPIN(pin)) Serial.println("Pin set");
      else Serial.println("Pin NOT set");
  }
  delay(100);
  GSM.checkStatus();
  delay(8000); //wait for the module to be ready
  //
  Serial.println("get Operator"); //ping the module to check if it is ready
  Serial.println(GSM.getOperator());
  delay(100);
  Serial.println(GSM.signalQuality());
  delay(100);
	text="Testing Sms";  		//text for the message. 
	number="+4916094842537"; 		//change to a valid number.
	//error=GSM.sendSms(number,text);
  //delay(100);
  Serial.println("Message sent"); //message sent
  Serial.println(error); //error is true if the message was sent, false if not.
	GSM.getCallStatus();

  //GSM.callNumber(number);
  Serial.println("call"); //message sent
	// OR 
	//Sim800L.sendSms("+540111111111","the text go here")
  GSM.checkStatus();
  delay(100);
}

void loop() {
  Inhalt_SMS = "GPSDaten"; // holt sich GPS Daten
  GSM.sendSms(number, Inhalt_SMS); // Sendet die GPS Daten per SMS
  Serial.println(Inhalt_SMS); // Weils so schön ist, printet er die nochmal
  delay(300000); // 8 min warten
  // put your main code here, to run repeatedly:
}