#include "ADS1256.h"
ADS1256 adc(5, 3, 3, 10, 2.500);  //DRDY, RESET, SYNC(PDWN), CS, VREF(float).
String str = "";
float num = 0.0;
double adcPD1 = 0;
double adcPD2 = 0;
int adcTS1 = 0;
int adcTS2 = 0;
int cal[4];
int sum[4];

struct data {
  float force[4];
  float pressure[2];
  float temperature[2];
};

data databus = {{0,0,0,0}, {0,0}, {0,0}};

void setup() {
  Serial.begin(115200);  //The value does not matter if you use an MCU with native USB
  while (!Serial) {}
  adcSetup();
  tempSetup();
}

void loop() {
  str = "";
  getData();
  for(int i = 0; i < 4; i++){
    str = String(str + String(databus.force[i]) + "  ");
  }
  str = String(str + String(databus.pressure[0]) + "  ");
  str = String(str + String(databus.pressure[1]) + "  ");
  str = String(str + String(databus.temperature[0]) + "  ");
  str = String(str + String(databus.temperature[1]) + "  ");

  Serial.println(str);
}