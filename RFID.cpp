#include <Servo.h>
const int servoPin = 9;
const int greenLEDPin = 3;
const int redLEDPin = 6;
Servo myServo;

void setup() {
  Serial.begin(9600);       // Begin serial communication
  myServo.attach(servoPin); 
  pinMode(greenLEDPin, OUTPUT);
  pinMode(redLEDPin, OUTPUT);
  Serial.println("Arduino ready.");
}

void loop() {
  if (Serial.available() > 0) {
    char accessStatus = Serial.read(); // Read access status ('G' for granted, 'D' for denied)

    // Wait for the angle to be sent next
    delay(10); // Slight delay for data availability
    if (Serial.available() > 0) {
      int angle = Serial.parseInt(); // Read the servo angle sent from Python

      if (accessStatus == 'G') {
        digitalWrite(greenLEDPin, HIGH);  // Turn on green LED
        digitalWrite(redLEDPin, LOW);     // Turn off red LED
        myServo.write(angle);             // Move servo to granted angle
      } else if (accessStatus == 'D') {
        digitalWrite(greenLEDPin, LOW);   // Turn off green LED
        digitalWrite(redLEDPin, HIGH);    // Turn on red LED
        myServo.write(angle);             // Move servo to denied angle
      }
  }
 }
}
