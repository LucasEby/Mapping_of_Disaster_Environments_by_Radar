#inlcude <Servo.h>

Servo servo_h;
Servo servo_v;

int angle_h = 0;
int angle_v = 0;
int servoDirection = 1;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // set up the Serial Library at 9600 bps 
  servo_h.attach(9); // servo for horizontal movement connected to pin 9
  servo_v.attach(10); // servo for vertical movement connected to pin 10
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()) {
    // change the position of the servo when the PC instructs
    // how to stop the loop when scanning finished??? 
    // exit(0) could stop the loop
    servo_h.write(angle_h);
    servo_v.write(angle_v);

    // MAKE THE SCAN AND GET THE RESULT FROM THE RADAR

    // check the horizontal scanning direction
    if (servoDirection == 1)
      angle_h++;
    else
      angle_h--;

    // Change the direction when edges is reached
    if (angle_h == 180 || servoRotatePosition == 0) {
      servoDirection = -servoDirection;
      angle_h = angle_h%181;
      angle_v++;
    }
  }
}
