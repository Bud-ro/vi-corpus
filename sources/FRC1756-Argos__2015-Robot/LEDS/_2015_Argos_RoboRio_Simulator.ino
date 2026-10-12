// Wire Master Writer
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Writes data to an I2C/TWI slave device
// Refer to the "Wire Slave Receiver" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>
#define NUMPIXELS 60 // Number of LEDs in strip
const int battPin = 2;     // the number of the pushbutton pin
const int totePin = 3;     // the number of the pushbutton pin
int battPinState = 0;         // variable for reading the pushbutton status
int totePinState = 0;         // variable for reading the pushbutton status

void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
  pinMode(battPin, INPUT);
  pinMode(totePin, INPUT);
  Serial.begin(9600); 
}

//Game Mode: 'A' Autonomous, 'T' Teleop, 'D' for Disabled, 'X' Test Mode
char gameMode = 'D';
byte gameTime = 0;
char battLevel = 'N';
byte toteLevel = 0;
bool win = false;


int x = 0;

void loop()
{
  Wire.beginTransmission(4); // transmit to device #4
  //Wire.write('A');
  Wire.write(gameMode);        // sends five bytes
  //Wire.write(";")'
  Wire.write(gameTime);
  //Wire.write(";")'
  Wire.write(battLevel);
  Wire.write(toteLevel);
  //Wire.write(";")'
  Wire.write(win);
  Wire.endTransmission();    // stop transmitting

  gameTime++;
  if (gameTime > 255)
    gameTime = 0;
 
  if (gameTime >= 0 && gameTime<15)
    gameMode = 'A';
  else if (gameTime >= 15 && gameTime < 150)
    gameMode = 'T';
  else if (gameTime >= 150 && gameTime < 200)
    gameMode = 'X';
  else
    gameMode = 'D';
    
 if (gameTime > 240)
 {
  win = true;  
 }
 else
 {
  win = false;
 }
  battPinState = digitalRead(battPin);
  //Serial.print(buttonState);

  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (battPinState == HIGH) {
    // turn LED on:
    battLevel = 'L';
  }
  else {
    // turn LED off:
    battLevel = 'N';
  }
    totePinState = digitalRead(totePin);
  //Serial.print(buttonState);

  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (totePinState == HIGH) {
    // turn LED on:
    toteLevel++;
    if (toteLevel == 7)
      toteLevel = 0;
  }
//  else {
    // turn LED off:
//    battLevel = 'N';
//  }
  delay(200);
}
