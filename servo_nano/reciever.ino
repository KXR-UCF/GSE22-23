#include "Servo.h"

#define N_PIN 11
#define E_PIN 9
#define F_PIN 7
#define V_PIN 8

#define CLOSE 95 // DPF close =98    IREC close= 0
#define OPEN 45  // DPF open = 40    IREC open = 120                        //Use E_pin / Ethanol for IREC valve

Servo n;
Servo e;
Servo f;
Servo v;

const int SIGNAL_PIN1 = 4; //  23   ETh
const int SIGNAL_PIN2 = 5; //  24   Nox
const int SIGNAL_PIN3 = 2; //  25   Fill
const int SIGNAL_PIN4 = 6; //  21   Vent    now 8
const int SIGNAL_PIN5 = 3; //  26   Toggle

// Pin to receive the signal from the first Arduino
// Pin to control the buzzer

int num = 0;

void setup()
{
  Serial.begin(19200);
  pinMode(LED_BUILTIN, OUTPUT);
  // make sure we pin up at the beginnning
  pinMode(SIGNAL_PIN1, INPUT);
  pinMode(SIGNAL_PIN2, INPUT);
  pinMode(SIGNAL_PIN3, INPUT);
  pinMode(SIGNAL_PIN4, INPUT);
  pinMode(SIGNAL_PIN5, INPUT);

  n.attach(N_PIN);
  e.attach(E_PIN);
  f.attach(F_PIN);
  v.attach(V_PIN);

  n.write(91);
  e.write(91);
  f.write(91);
  v.write(91);

  delay(1000);
}

void loop()
{

  if (digitalRead(SIGNAL_PIN1) == HIGH)
  {
    e.write(OPEN);
  }
  else
    e.write(CLOSE);

  if (digitalRead(SIGNAL_PIN2) == HIGH)
  {
    n.write(120); // IREC change
  }
  else
    n.write(0);

  if (digitalRead(SIGNAL_PIN3) == HIGH)
  {
    f.write(OPEN);
  }
  else
    f.write(CLOSE);

  if (digitalRead(SIGNAL_PIN4) == HIGH)
  {
    v.write(OPEN);
  }
  else
    v.write(CLOSE);

  if (digitalRead(SIGNAL_PIN5) == HIGH)
  {
    // e.write(CLOSE);
    // n.write(OPEN);
  }

  Serial.print(num);
  Serial.print(" ");
  Serial.print(" ");
  Serial.print(digitalRead(SIGNAL_PIN1) == HIGH);
  Serial.print(" ");
  Serial.print(digitalRead(SIGNAL_PIN2) == HIGH);
  Serial.print(" ");
  Serial.print(digitalRead(SIGNAL_PIN3) == HIGH);
  Serial.print(" ");
  Serial.print(digitalRead(SIGNAL_PIN4) == HIGH);
  Serial.print(" ");
  Serial.println(digitalRead(SIGNAL_PIN5) == HIGH);
}
