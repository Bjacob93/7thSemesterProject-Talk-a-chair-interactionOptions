#include <CapacitiveSensor.h>

CapacitiveSensor cap = CapacitiveSensor(12, 11);

void setup() {
  
  Serial.begin(115200);
}

void loop() {
  
  Serial.println(cap.capacitiveSensor(30));
}
