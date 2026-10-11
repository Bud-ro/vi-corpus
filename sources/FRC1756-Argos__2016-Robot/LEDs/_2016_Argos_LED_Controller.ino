// 2016 Argos LED Controller i2c


// Receives Game Status from Robo RIO over i2c and controls LEDs


#include <Wire.h>
#include <Adafruit_DotStar.h>
#include <SPI.h>

#define NUMPIXELS 60// Number of LEDs in strip

// control the LEDs pins:
#define DATAPIN1    4
#define CLOCKPIN1   5
#define DATAPIN2    8
#define CLOCKPIN2   9


Adafruit_DotStar strip1 = Adafruit_DotStar(NUMPIXELS, DATAPIN1, CLOCKPIN1);
Adafruit_DotStar strip2 = Adafruit_DotStar(NUMPIXELS, DATAPIN2, CLOCKPIN2);
const int sampleWindow = 50; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;
char gameMode = 'D';
char autonMode = 'L';
char ballPos = 'N';
char aimed = 'O';
char win = 'C';
char alliance = 'R';
int head  = 0, tail = -10; // Index of first 'on' and 'off' pixels
int p2p_average = 0;
int sound_scale = 512;

//Color Definitions
uint32_t auto_rockwall = 0xFF0000; //Red
uint32_t auto_lowbarshot = 0x0000FF; //Blue
uint32_t auto_lowbar = 0x0000FF; //Green
uint32_t auto_cheval = 0xFFFF00; //Yellow
uint32_t auto_port = 0xFF00FF; //Pink
uint32_t auto_rough = 0xFFFFFF; //white
uint32_t auto_moat = 0x00FFFF; //Teal
uint32_t auto_coals = 0xF000FF; //Purple

uint32_t teleColor = 0x00FF00;      // 'On' color (starts red)
uint32_t testColor = 0xFF0000;      // 'On' color (starts red)
uint32_t aimedColor = 0x00FF00;      // 'On' color (aimed = green)
uint32_t alliancecolor = 0xFF0000;      // 'On' color (starts red)
uint32_t disablecolor = 0xFF0000;      // 'On' color (starts red)
uint32_t catyellowcolor = 0x444400;      // 'On' color (starts red)
uint32_t autonModecolor = 0x0000FF;      // 'On' color (starts red)
uint32_t color = 0xFF0000;

void setup()
{
  Wire.begin(84);                // join i2c bus with address #84
  TWBR = 12;
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(115200);           // start serial for output

  strip1.begin(); // Initialize pins for output
  strip1.show();  // Turn all LEDs off ASAP
  strip2.begin(); // Initialize pins for output
  strip2.show();  // Turn all LEDs off ASAP
  //strip.setBrightness(20);

  Serial.print("ARGOS 1756!");

}



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
    switch (gameMode)
    {
      case 'A':
        auton();  //Auto Blue
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

  //  strip.show();
}

void celebrationMode()
{
  for (int x = 0; x < NUMPIXELS; x++)
  {
    color = random();
    strip1.setPixelColor (x, color);
    strip2.setPixelColor (x, color);
  }
  strip1.show();
  strip2.show();
  delay(50);
}

void auton()
{
 
  for (int x = 0; x < NUMPIXELS; x++)
  {

    strip1.setPixelColor (x, alliancecolor);
    strip2.setPixelColor (x, alliancecolor);
  }
  while (gameMode == 'A')
  {
  
  for (int x = tail; x < head; x++)
  {
    strip1.setPixelColor (x, 0x00FF00);
    strip2.setPixelColor (x, 0x00FF00);
  }
    strip1.setPixelColor (tail-1, alliancecolor);
    strip2.setPixelColor (tail-1, alliancecolor);
  strip1.show();
  strip2.show();
  if (tail <= NUMPIXELS)
  {
    head++;
    tail++;
  }
  else
  {
    head=0;
    tail=-10;
  }
  }


}

void teleopMode()
{
  for (int x = 0; x < (36); x++)
  {

    strip1.setPixelColor (x, teleColor);
    strip2.setPixelColor (x, teleColor);
  }
  for (int x = (36); x < NUMPIXELS; x++)
  {

    strip1.setPixelColor (x, color);
    strip2.setPixelColor (x, color);
  }
  strip1.show();
  strip2.show();

}
void testMode()
{
  for (int x = 0; x < 36; x++)
  {
    color = rand();
    strip1.setPixelColor (x, color);
    strip2.setPixelColor (x, color);
  }
  for (int x = 36; x < NUMPIXELS; x++)
  {
    color = 0x000000;
    strip1.setPixelColor (x, color);
    strip2.setPixelColor (x, color);
  }
  strip1.show();
  strip2.show();
  delay(100);
}

void disabledMode()
{
   unsigned long startMillis= millis();  // Start of sample window
   unsigned int peakToPeak = 0;   // peak-to-peak level
   int i,j;
   unsigned int signalMax = 0;
   unsigned int signalMin = 600;
 
   // collect data for 50 mS
   while (millis() - startMillis < sampleWindow)
   {
      sample = analogRead(0);
      if (sample < 1024)  // toss out spurious readings
      {
         if (sample > signalMax)
         {
            signalMax = sample;  // save just the max levels
         }
         else if (sample < signalMin)
         {
            signalMin = sample;  // save just the min levels
         }
      }
      if (gameMode != 'D') {
      break;
      }
   }
   peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude
   p2p_average = (peakToPeak + p2p_average) / 2;
   if (p2p_average > 450)
   {
    sound_scale = 612;
   }
   else if (p2p_average <= 450 && p2p_average > 100)
   {
    sound_scale = 512;
   }
   //else if (p2p_average <= 250 && p2p_average > 100)
   //{
   // sound_scale = 412;
   // }
    else
      sound_scale = 100;
   

   int height = (peakToPeak * NUMPIXELS/2) / sound_scale ; // convert to volts
 
   for(i=NUMPIXELS/2; i>=0; i--) {
    if(i < NUMPIXELS/2 - height)
    {
      strip1.setPixelColor(i,0);
      strip2.setPixelColor(i,0);
      strip1.setPixelColor(NUMPIXELS-i,0);
      strip2.setPixelColor(NUMPIXELS-i,0);
    }
    else
    {
      strip1.setPixelColor(i,autonModecolor);
      strip2.setPixelColor(i,autonModecolor);
      strip1.setPixelColor(NUMPIXELS-i,autonModecolor);
      strip2.setPixelColor(NUMPIXELS-i,autonModecolor);
    }
  }
  strip1.show(); // Update strip
  strip2.show(); // Update strip
   Serial.print(height);
   Serial.print(" , ");
   Serial.println(peakToPeak);
   Serial.print(" , ");
   Serial.println(sound_scale);

  
}


// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int numBytes)
{
  String temp = "";
  int byteNum = 10;
  char text[byteNum + 1];
  char blank[byteNum + 1];
  int i = 0;
  while (Wire.available()) {
    text[i] = Wire.read();
    //         Serial.print(text[i]);
    text[i + 1] = '\0';
    i++;
  }
  // Serial.println('\0');
  gameMode = text[1]; // receive byte as a character
  //   Serial.print(gameMode);         // print the character
  autonMode = text[2];
  //   Serial.print(autonMode);
  ballPos = text[3];
  //    Serial.println(ballPos);
  aimed = text[4];
  //    Serial.println(aimed);
  win = text[5];
  //   Serial.print(win);
  alliance = text[6];
  //   Serial.println(alliance);



  if (alliance == 'R')
  {
    alliancecolor = 0xFF0000;
  }
  else
  {
    alliancecolor = 0x0000FF;
  }
  if (aimed == 'X')
  {
    teleColor = aimedColor;
  }
  else
  {
    teleColor = alliancecolor;
  }
  switch (autonMode)
    {
      case 'K':
        autonModecolor = auto_rockwall;
        break;
      case 'H':
        autonModecolor = auto_lowbarshot;
        break;
      case 'L':
        autonModecolor = auto_lowbar;
        break;
      case 'V':
        autonModecolor = auto_cheval;
        break;
      case 'P':
        autonModecolor = auto_port;
        break; 
       case 'G':
        autonModecolor = auto_rough;
        break;       
       case 'M':
        autonModecolor = auto_moat;
        break;             
      default:
        autonModecolor = auto_coals;
    }


}
