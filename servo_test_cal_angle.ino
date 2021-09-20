#include <Servo.h>

Servo servo_h;
Servo servo_v;

int angle_h = 0;
int angle_v = 0;
int servoDirection = 1;
int x;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); // set up the Serial Library at 9600 bps 
  Serial.setTimeout(1);
  // servo_h.attach(9); // servo for horizontal movement connected to pin 9
  // servo_v.attach(10); // servo for vertical movement connected to pin 10
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!Serial.available());
  x = Serial.readString().toInt();

  // the motor set to be trigger when intputted 5
  if (x == 5) {
    Serial.println("Motor started:");
    while (angle_v < 180) {
      Serial.print("H: ");
      Serial.print(angle_h);
      Serial.print("; V: ");
      Serial.println(angle_v);
      
      if (servoDirection == 1)
        angle_h++;
      else
        angle_h--;

      if (angle_h == 180 || angle_h == 0) {
        servoDirection = -servoDirection;
        angle_h = angle_h % 181;
        angle_v++;
      }
    }
  } else {
    Serial.println("Not triggered");
  }
}
