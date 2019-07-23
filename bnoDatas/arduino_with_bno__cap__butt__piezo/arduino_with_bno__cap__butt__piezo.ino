#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <CapacitiveSensor.h>
/*
   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3-5V DC
   Connect GROUND to common ground

*/

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

Adafruit_BNO055 bno = Adafruit_BNO055(55);

/**************************************************************************/
/*
    Display sensor calibration status
*/
/**************************************************************************/
void displayCalStatus(void)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  /* Display the individual values
  Serial.print("Sys:");
  Serial.print(system, DEC);
  Serial.print(" G:");
  Serial.print(gyro, DEC);
  Serial.print(" A:");
  Serial.print(accel, DEC);
  Serial.print(" M:");
  Serial.print(mag, DEC);
  */
}
// Piezo constants
const int piezo = A0;
const int threshold = 20;

// Piezo variable
int vibrationReading;

// Capacitive sensors
CapacitiveSensor cap1 = CapacitiveSensor(10, 9);
int capread1;
int capthresh1 = 5000;
CapacitiveSensor cap2 = CapacitiveSensor(8, 7);
int capread2;
int capthresh2 = 2500;

// Button stuff
const int buttonpin = 2;
int buttonstate;
/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }else{
  Serial.print("Hello");
  }

  delay(1000);

  bno.setExtCrystalUse(true);
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  Serial.print(event.orientation.x, 0);

  /* Optional: Display calibration status */
 // displayCalStatus();

  /* Optional: Display sensor status (debug only) */
  //displaySensorStatus();

  /* New line for the next sample */
  Serial.println("");
  /* Piezo sensor reading*/
  vibrationReading = analogRead(piezo);

  if (vibrationReading > threshold){
    Serial.println("contentup");
    Serial.println("");
  }

  /* Capacitive readings*/
  capread1 = cap1;
  capread2 = cap2;
  if (capread1 > capthresh1){
    Serial.println("contentup");
    Serial.println("");
  }
  if (capread2 > capthresh2) {
    Serial.println("userdetected");
    Serial.println("");
  }

  /* Button readings*/
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH){
    Serial.println("contentup");
    Serial.println("");
  }
  /* Wait the specified delay before requesting nex data */
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
