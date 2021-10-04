#include <AntaresESP32HTTP.h>
#include <Servo.h>

#define ACCESSKEY "your-access-key" // get ur acces key on your antares account
#define WIFISSID "your-wifi-ssid" // input ur wifi ssid
#define PASSWORD "your-wifi-password" // input ur wifi password

#define projectName "your-project-name" // input ur antares project name on antares application 
#define deviceName "your-project-name" // input ur antares device name on antares application
AntaresESP32HTTP antares(ACCESSKEY);

Servo servo1;
int servo1_pin = 27;

Servo servo2;
int servo2_pin = 26;

int led = 13;
int led2 = 12;

int pb1 = 34;
int pb2 = 35;
int pb1_val;
int pb2_val;

int count = 0;
int state = 0;
int wait;
int servo_open = 90;
int servo_close = 0;

void setup() {
    Serial.begin(115200);
    antares.setDebug(true);
    antares.wifiConnection(WIFISSID, PASSWORD);
    servo1.attach (servo1_pin);
    servo2.attach (servo2_pin);
    pinMode (led, OUTPUT);
    pinMode (led2, OUTPUT);
    pinMode (pb1, INPUT);
    pinMode (pb2, INPUT);
}

void loop() {
  // Get the latest data from your Antares device
  antares.get(projectName, deviceName);
  int state = antares.getInt("state");
  pb1_val = digitalRead (pb1);
  pb2_val = digitalRead (pb2);
  
  if(pb1_val == 1 && state == 1){
    count++;
    delay (300);
    if (count == 1){
      digitalWrite(led, HIGH);
      servo1.write(servo_open);
      wait = 1500;
    }
  }
  
  if (pb1_val == 1 && state == 2){
    count++;
    delay (300);
    if (count == 1){
      digitalWrite(led2, HIGH);
      servo1.write(servo_open);
      wait = 1500;
    }
  }

   if (pb2_val == 1 && state == 1){
    count++;
    delay (300);
    if (count == 1){
      digitalWrite(led, LOW);
      servo2.write(servo_open);
      wait = 1500;
    }  
  }

   if (pb2_val == 1 && state == 2){
    count++;
    delay (300);
    if (count == 1){
      digitalWrite(led2, LOW);
      servo2.write(servo_open);
      wait = 1500;
    } 
  }
  count = 0;
  wait--;
  if (wait < 0) {
    wait = 0;
      servo1.write(servo_close);
      servo2.write(servo_close);
  }
  
  Serial.print ("State= " + String(state));
  Serial.print (" count= " + String(count));
  Serial.print (" pb1= " + String(pb1_val));
  Serial.print (" pb2= " + String(pb2_val));
  Serial.println (" wait= " + String(wait));  
    
  delay(2000);
}
