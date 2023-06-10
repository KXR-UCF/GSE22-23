#include <LiquidCrystal_I2C.h>
#include <FastLED.h>
#include <Wire.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDRESS 0x3C
LiquidCrystal_I2C lcd(0x27, 16, 4);

#define LED_PIN 32
#define NUM_LEDS 10
CRGB leds[NUM_LEDS];

#define powerSwitchPin 33 // Power switch pin
#define fillSwitchPin 25  // Fill switch pin
#define ventSwitchPin 26  // Vent switch pin
#define fireSwitchPin 14  // Fire button pin
#define closeSwitchPin 13 // Close switch pin
#define abortSwitchPin 12 // Abort switch pin
#define QDSwitchPin 23    // QD switch pin

#define QDButton 5     // QD Button
#define fireButton 18  // Fire Button
#define closeButton 4  // Close Button
#define abortButton 19 // Abort Button

struct swState
{
  bool power = 0;
  bool powerP = 0;
  bool fill = 0;
  bool fillP = 1;
  bool vent = 0;
  bool ventP = 1;
  bool fire = 0;
  bool fireP = 0;
  bool abort = 0;
  bool abortP = 0;
  bool close = 0;
  bool closeP = 0;
  bool QD = 0;
  bool QDP = 0;
} swState;

struct btState
{
  bool close = 0;
  bool closeP = 0;
  bool abort = 0;
  bool abortP = 0;
  bool fire = 0;
  bool fireP = 0;
  bool QD = 0;
  bool QDP = 0;
} btState;

struct iLED
{
  int power = 6;
  int fill = 5;
  int vent = 4;
  int QD = 3;
  int fire = 2;
  int abort = 1;
  int close = 0;
} iLED;

int printState = 0;
int printStateP = 0;
/*
  0 -> null (print nothing)
  1 -> LAUNCH ARM
  2 -> FIRE!!
  3 -> ABORT ARM
  4 -> ABORT!!
  5 -> CLOSE ARM
  6 -> CLOSE
*/

unsigned long lcdTimer = millis();
int indicatorState;
unsigned long lastCheckTime = 0;
const unsigned long checkInterval = 100; // Interval to check buttons (in milliseconds)

void setup()
{
  lcd.begin(); // initialize the LCD
  lcd.clear();
  FastLED.addLeds<WS2811, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(255);
  delay(5);
  pinSetup();

  Serial.begin(115200);
  delay(3000);
  Serial.println("----READY-----");
  ledInitColor();
}

void loop()
{
  checkButtons();
  FastLED.show();
  delay(10);
}

void checkButtons()
{
  runPower();
  runFill();
  runVent();
  runLaunch();
  runAbort();
  // runQD();
  runClose();
  lastStateLCD();
}
