#include "ADS1256.h"

ADS1256 A(21, 26, 20, 47, 2.500); // DRDY, RESET, SYNC(PDWN), CS, VREF(float).

long rawConversion = 0; // 24-bit raw value
float voltageValue = 0; // human-readable floating point value
double offset = 0.0;

int singleEndedChannels[8] = {SING_0, SING_1, SING_2, SING_3, SING_4, SING_5, SING_6, SING_7}; // Array to store the single-ended channels
int differentialChannels[4] = {DIFF_0_1, DIFF_2_3, DIFF_4_5, DIFF_6_7};                        // Array to store the differential channels
int inputChannel = 0;                                                                          // Number used to pick the channel from the above two arrays
char inputMode = ' ';                                                                          // can be 's' and 'd': single-ended and differential

int pgaValues[7] = {PGA_1, PGA_2, PGA_4, PGA_8, PGA_16, PGA_32, PGA_64}; // Array to store the PGA settings
int pgaSelection = 0;                                                    // Number used to pick the PGA value from the above array

int drateValues[16] =
    {
        DRATE_30000SPS,
        DRATE_15000SPS,
        DRATE_7500SPS,
        DRATE_3750SPS,
        DRATE_2000SPS,
        DRATE_1000SPS,
        DRATE_500SPS,
        DRATE_100SPS,
        DRATE_60SPS,
        DRATE_50SPS,
        DRATE_30SPS,
        DRATE_25SPS,
        DRATE_15SPS,
        DRATE_10SPS,
        DRATE_5SPS,
        DRATE_2SPS}; // Array to store the sampling rates

int drateSelection = 0; // Number used to pick the sampling rate from the above array

String registers[11] =
    {
        "STATUS",
        "MUX",
        "ADCON",
        "DRATE",
        "IO",
        "OFC0",
        "OFC1",
        "OFC2",
        "FSC0",
        "FSC1",
        "FSC2"}; // Array to store the registers

int registerToRead = 0;       // Register number to be read
int registerToWrite = 0;      // Register number to be written
int registerValueToWrite = 0; // Value to be written in the selected register
int cal[4];
int sum[4];
void setup()
{
  Serial.begin(115200); // The value does not matter if you use an MCU with native USB

  while (!Serial)
  {
    ; // Wait until the serial becomes available
  }

  // Serial.println("ADS1256 - Custom Library Demo File by Curious Scientist - 2022-07-14");

  A.InitializeADC(); // See the documentation for every details
  // Setting up CS, RESET, SYNC and SPI
  // Assigning default values to: STATUS, MUX, ADCON, DRATE
  // Performing a SYSCAL

  // Below is a demonstration to change the values through the built-on functions of the library
  // Set a PGA value
  A.setPGA(PGA_8); // 0b00000000 - DEC: 0
  //--------------------------------------------

  // Set input channels
  A.setMUX(DIFF_6_7); // 0b01100111 - DEC: 103
  //--------------------------------------------

  // Set DRATE
  A.setDRATE(DRATE_100SPS); // 0b00010011 - DEC: 19
  //--------------------------------------------

  // Read back the above 3 values to check if the writing was succesful
  // Serial.print("PGA: ");
  // Serial.println(A.readRegister(IO_REG));
  delay(100);
  //--
  // Serial.print("MUX: ");
  // Serial.println(A.readRegister(MUX_REG));
  delay(100);
  //--
  // Serial.print("DRATE: ");
  // Serial.println(A.readRegister(DRATE_REG));
  delay(100);

  // Freeze the display for 3 sec
  delay(3000);
  for (int i = 0; i < 100; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      sum[j] += A.convertToVoltage(A.cycleDifferential()) * .004 * 2.05;
    }
  }
  cal[0] = int(sum[0] / 100);
  cal[1] = int(sum[1] / 100);
  cal[2] = int(sum[2] / 100);
  cal[3] = int(sum[3] / 100);

  // Take multiple readings to find the offset value
}

String str = "";
float num = 0.0;
int adcPD1 = 0;
int adcPD2 = 0;
int adcTS1 = 0;
int adcTS2 = 0;

void loop()
{
  str = "";

  for (int j = 0; j < 4; j++)
  {
    num = A.convertToVoltage(A.cycleDifferential()) * .004 * 2.05 - cal[j];
    // Serial.print(A.convertToVoltage(A.cycleDifferential())*.004*2.05-10.9);//print the converted differential results with 4 digits
    // Serial.print("\t"); //tab separator to separate the 4 conversions shown in the same line
    str = String(str + String(num) + "  ");
  }
  adcPD1 = analogRead(1);
  str = String(str + String(adcPD1) + "  ");
  adcPD2 = analogRead(2);
  str = String(str + String(adcPD2) + "  ");
  // adcTS1 = analogRead(4);
  // str = String(str + String(adcTS1) + "  ");
  // adcTS2 = analogRead(5);
  // str = String(str + String(adcTS2) + "  ");
  Serial.println(str);
  delay(1000);
}
