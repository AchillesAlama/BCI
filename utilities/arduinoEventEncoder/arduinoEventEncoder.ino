/*
File: arduinoEventEncoder.ino
Date: 19-02-2020
Author: Ludwig von Feilitzen
Description:
  This code was put on an Arduino Nano which was connected to a USB to TTL chip which in turn
  was connected to the computer via, you guessed it, USB. Using the pySerial library we can write to the serial port
  of the USB to TTL chip which then sends this info serially to the Arduino, which then sets four of its pins
  HIGH or LOW using this code. These four pins acts as our encoding scheme for sending the current "event" (image on screen)
  to the Ultracortex, so the Cyton board can include the current event in the samples. This way we know which image
  was shown when the sample was taken without having to worry about the unknown delays between a sample being taken
  and the callback function being called for that sample, and be sure that the sample belongs to a certain image/event.

  We are using three pins (d10-d12) with d12 = MSB. Therefore we can encode 8 different events (0-7). These pins need to be 
  connected to the digital inputs on the Cyton board, D11, D12, and D17 where D17 is MSB.
*/

int ledPin = 13;
String inString = "";

//Encoding pins
int d10 = 10;
int d11 = 11;
int d12 = 12;


void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
  pinMode(ledPin, OUTPUT);
  pinMode(d10, OUTPUT);
  pinMode(d11, OUTPUT);
  pinMode(d12, OUTPUT);

}

void loop() {
  // send data only when you receive data:
  while (Serial.available() > 0) {
    
    int inChar = Serial.read(); //We get the ascii code of each digit
    inString += (char)inChar;
   
    // if you get a newline transmission is over, set the pins
    if (inChar == '\n') {
      int val = inString.toInt() & 0x0f;

      if (val >= 0 && val <= 7){
        digitalWrite(d10, val & 0x01);
        digitalWrite(d11, val & 0x02);
        digitalWrite(d12, val & 0x04); 
      }
      // clear the string for new input:
      inString = "";
    }
  }
}
