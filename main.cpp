/*
  LiquidCrystal Library - Serial Input

 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.

 This sketch displays text sent over the serial port
 (e.g. from the Serial Monitor) on an attached LCD.

 The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 modified 7 Nov 2016
 by Arturo Guadalupi

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystalSerialDisplay

*/

// include the library code:
#include <Arduino.h>
#include <LiquidCrystal.h>
#include <stdio.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
uint8_t lenofmsg = 0;
char msg;
String msg1;
int8_t i = 0;
int8_t j = 0;
int8_t k = 0;
char message[32];
char message_old[32];
 


void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // initialize the serial communications:
  Serial.begin(9600);
}

void loop() {
  // when characters arrive over the serial port...
  if (Serial.available()) {
    i = 0;
    j = 0;
    // wait a bit for the entire message to arrive
    delay(100);
    // clear the screen
    // lcd.clear();
    // read all the available characters
    while (Serial.available() > 0) {
      // msg = Serial.read();
      // msg1 = msg;
      // lenofmsg = msg1.length();
      // display each character to the LCD
      // lcd.setCursor(0, 1);
      for (k = 0; k < 32; k++){
        message[k] = Serial.read();
      }
      for (k = 0; k < 32; k++){
        lcd.setCursor(i, j);
        if (message[k] != message_old[k]){
          lcd.write(message[k]);
          message_old[k] = message[k];
        }
        i++;
        if (i == 16 && j == 0) {
          i = 0;
          j = 1;
        }
        // else if (i == 16 && j == 1) {
        //   i = 0;
        //   j = 0;
        // }
      }
      //shift message to old message
      // for (k = 0; k < 32; k++){
      //   message_old[k] = message[k];
      // }

      // lcd.setCursor(0, 0);
      // //remove first 16 characters from msg1
      // if (lenofmsg > 16) {
      //   msg1.remove(0, 16);
      //   lcd.print(msg1);a
      // }
    }
  }
}
