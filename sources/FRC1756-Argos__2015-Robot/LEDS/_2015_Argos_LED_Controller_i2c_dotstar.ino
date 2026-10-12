// 2015 Argos LED Controller i2c


// Receives Game Status from Robo RIO over i2c and controls LEDs


#include <Wire.h>
#include <Adafruit_DotStar.h>
#include <SPI.h> 

#define NUMPIXELS 60 // Number of LEDs in strip

// control the LEDs pins:
#define DATAPIN    4
#define CLOCKPIN   5

int yoyoMax = 60;

Adafruit_DotStar strip = Adafruit_DotStar(NUMPIXELS, DATAPIN, CLOCKPIN);

char gameMode = 'D';
unsigned char gameTime = 0;
char battLevel = 'N';
unsigned char yoyoPos = 30;
float yoyoPercent = 0.50;
char win = 'C';
char alliance = 'R';
int toteLevel = 0;



void setup()
{
  Wire.begin(84);                // join i2c bus with address #4
  TWBR = 12;
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(115200);           // start serial for output
 
  strip.begin(); // Initialize pins for output
  strip.show();  // Turn all LEDs off ASAP
  //strip.setBrightness(64);
  
  Serial.print("ARGOS 1756!");
  
}
int head  = 0, tail = -30; // Index of first 'on' and 'off' pixels
uint32_t autonColor = 0x555000;      // 'On' color (starts red)
uint32_t teleColor = 0x00FF00;      // 'On' color (starts red)
uint32_t testColor = 0xFF0000;      // 'On' color (starts red)
uint32_t color = 0xFF0000;      // 'On' color (starts red)

void loop()
{
      
//   Serial.print(gameMode);
//   Serial.print(gameTime);
//   Serial.print(battLevel);
//   Serial.print(yoyoPos);      
//   Serial.print(win);
//   Serial.println(alliance);
  
  
  //Serial.println("main");
  if (win == 'W') {
    celebrationMode();
  }
  else 
  {
    if (battLevel == 'L') {
      battLowMode();
    }
    else {
      switch (gameMode)
      {
        case 'A':
          autonMode();  //Auto Blue
          break;
        case 'T':
          teleopMode(); //Tele Green
          break;
        case 'X':
          testMode(); //Test Multi color
          break;
        default:
          disabledMode(); // Disabled Red
  
      }    
    }
  }

//  strip.show();
}

void celebrationMode()
{
  for (int x=0; x<NUMPIXELS; x++)
  {
    color = random(); 
    strip.setPixelColor (x, color);
  }
  strip.show();
  delay(50);
}
void battLowMode()
{
  for (int x=0; x<NUMPIXELS; x++)
  {
    color = 0x000000;
    strip.setPixelColor (x, color);
  }
  strip.show();


  delay(200);
  for (int x=0; x<NUMPIXELS; x++)
  {
    color = 0x300000;
    strip.setPixelColor (x, color);
  }
  strip.show();
  delay(200); 
  
}
void autonMode()
{
  for (int x=0; x<(yoyoPercent*NUMPIXELS); x++)
  {

    strip.setPixelColor (x, autonColor);
  }
   for (int x=(yoyoPercent*NUMPIXELS); x<NUMPIXELS; x++)
  {
    color = 0x000000; 
    strip.setPixelColor (x, color);
  } 
  strip.show();
}

void teleopMode()
{
  for (int x=0; x<(yoyoPercent*NUMPIXELS); x++)
  {
    if (gameTime <= 20)
    {
      teleColor = 0xFFFF00; 
    } 
    strip.setPixelColor (x, teleColor);
   }
      for (int x=(yoyoPercent*NUMPIXELS); x<NUMPIXELS; x++)
  {
    color = 0x444400; 
    strip.setPixelColor (x, color);
  } 
  strip.show();
}
void testMode()
{
  for (int x=0; x<(yoyoPercent*NUMPIXELS); x++)
  {
    color = rand(); 
    strip.setPixelColor (x, color);
  }
  for (int x=(yoyoPercent*NUMPIXELS); x<NUMPIXELS; x++)
  {
    color = 0x000000; 
    strip.setPixelColor (x, color);
  } 
  strip.show();
  delay(100);
}

void disabledMode()
{
  strip.setPixelColor(head, color); // 'On' pixel at head
  strip.setPixelColor(tail, 0);     // 'Off' pixel at tail
  if(++head >= NUMPIXELS) {         // Increment head index.  Off end of strip?
    head = 0;                       //  Yes, reset head index to start
    if((color >>= 8) == 0)          //  Next color (R->G->B) ... past blue now?
      color = 0xFF0000;             //   Yes, reset to red
  }
  if(++tail >= NUMPIXELS) tail = 0; // Increment, reset tail index
  strip.show();
  delay(40); 
}

void toteHandler()
{
  if yoyoPos
  
  
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int numBytes)
{
  String temp = "";
  int byteNum = 10;
  char text[byteNum+1];
  char blank[byteNum+1];
  int i = 0;
   while(Wire.available()){
      text[i] = Wire.read();
  //         Serial.print(text[i]);
          text[i+1] = '\0';
          i++;
   
   } 
   // Serial.println('\0');
    gameMode = text[1]; // receive byte as a character
 //   Serial.print(gameMode);         // print the character
    gameTime = text[2];
//    Serial.print(gameTime);
    battLevel = text[3];
 //   Serial.print(battLevel);
    yoyoPos = text[4];
    yoyoPercent = (float)yoyoPos/(float)yoyoMax;
    Serial.println(yoyoPos);
    Serial.println(yoyoPercent);
 //   Serial.print(yoyoPos);      
    win = text[5];
 //   Serial.print(win);
    alliance = text[6];
 //   Serial.println(alliance);
    
    if (alliance == 'R')
    {
      teleColor = 0xFF0000;
    }
    else
    {
      teleColor = 0X0000FF;
    }
}
