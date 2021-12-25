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
    while (Serial.available() > 0) {
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
      }
    }
  }
}
