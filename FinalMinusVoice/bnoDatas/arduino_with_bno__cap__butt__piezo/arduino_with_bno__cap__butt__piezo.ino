#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <CapacitiveSensor.h>
/*
   Connections
   ===========
   BNO:
   Connect SCL to pin 3
   Connect SDA to pin 2
   Connect VDD to 3-5V DC
   Connect GROUND to common ground
   
   External Button:
   connect to pin 12
   
   Piezo:
   connect to analog 0
   
   Capacitive 1 (sitting):
   connect to pin
   
   Capacitive 2 (touch):
   connect to pin

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
long capread1;
long capthresh1 = 5000;
CapacitiveSensor cap2 = CapacitiveSensor(8, 7);
long capread2;
long capthresh2 = 5000;

// Button stuff
const int buttonPin = 12;
int buttonState;
/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  
  cap1.set_CS_AutocaL_Millis(0xFFFFFFFF);
  cap2.set_CS_AutocaL_Millis(0xFFFFFFFF);

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
  Serial.print ("\t");

  /* Optional: Display calibration status */
 // displayCalStatus();

  /* Optional: Display sensor status (debug only) */
  //displaySensorStatus();

  /* New line for the next sample */
  Serial.println("");
  /* Piezo sensor reading*/
  vibrationReading = analogRead(piezo);

  if (vibrationReading > threshold){
    Serial.println("contentUp");
  }

  /* Capacitive readings*/
  capread1 = cap1.capacitiveSensor(30);
  capread2 = cap2.capacitiveSensor(30);
  if (capread1 > capthresh1){
    Serial.println("userDetected");
    //Serial.println("");
  }
  if (capread2 > capthresh2) {
    Serial.println("contentUp");
    //Serial.println("");
  }

  /* Button readings*/
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH){
    Serial.println("contentUp");
  }  
  /* Wait the specified delay before requesting nex data */
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
