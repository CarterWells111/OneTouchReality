#include <Servo.h>

Servo servos[5];

void setup() {
  Serial.begin(9600); 
  servos[0].attach(5);  
  servos[1].attach(3);  
  servos[2].attach(9);  
  servos[3].attach(6);  
  servos[4].attach(10);
  setAllServos(0);
  setAllServos(180);
  delay(100);
  setAllServos(0);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    int spaceIndex = data.indexOf(' ');
    if (spaceIndex != -1) {
      int finger = data.substring(0, spaceIndex).toInt();
      int angle = data.substring(spaceIndex + 1).toInt();
      
      if (finger >= 0 && finger < 5 && angle >= 0 && angle <= 180) {
        servos[finger].write(angle);
        Serial.print("Moving servo ");
        Serial.print(finger);
        Serial.print(" to ");
        Serial.println(angle);
      }
    }
  }
}

void setAllServos(int angle) {
  for (int i = 0; i < 5; i++) {
    servos[i].write(angle);
  }
}