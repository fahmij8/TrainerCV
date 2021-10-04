#include <AntaresESP32HTTP.h>

#define ACCESSKEY "your-access-key" // get ur acces key on your antares account
#define WIFISSID "your-wifi-ssid" // input ur wifi ssid
#define PASSWORD "your-wifi-password" // input ur wifi password

#define projectName "your-project-name" // input ur antares project name on antares application 
#define deviceName "your-project-name" // input ur antares device name on antares application
AntaresESP32HTTP antares(ACCESSKEY);
int pin1 = 13;
int pin2 = 12;
int pin3 = 14;
int pin4 = 27;
int pin5 = 26;


void setup() {
    Serial.begin(115200);
    antares.setDebug(true);
    antares.wifiConnection(WIFISSID, PASSWORD);
    pinMode (pin1, OUTPUT);
    pinMode (pin2, OUTPUT);
    pinMode (pin3, OUTPUT);
    pinMode (pin4, OUTPUT);
    pinMode (pin5, OUTPUT);
}

void loop() {
  // Get the latest data from your Antares device
  antares.get(projectName, deviceName);
    int num = antares.getInt("number");
    Serial.println("number: " + (num));
  if (num == 1) {
    digitalWrite (pin1, HIGH);
    digitalWrite (pin2, LOW);
    digitalWrite (pin3, LOW);
    digitalWrite (pin4, LOW);
    digitalWrite (pin5, LOW);
  }
  else if (num == 2){
    digitalWrite (pin1, HIGH);
    digitalWrite (pin2, HIGH);
    digitalWrite (pin3, LOW);
    digitalWrite (pin4, LOW);
    digitalWrite (pin5, LOW);
  }
  else if (num == 3){
    digitalWrite (pin1, HIGH);
    digitalWrite (pin2, HIGH);
    digitalWrite (pin3, HIGH);
    digitalWrite (pin4, LOW);
    digitalWrite (pin5, LOW);
  }
  else if (num == 4){
    digitalWrite (pin1, HIGH);
    digitalWrite (pin2, HIGH);
    digitalWrite (pin3, HIGH);
    digitalWrite (pin4, HIGH);
    digitalWrite (pin5, LOW);
  }
  else if (num == 5){
    digitalWrite (pin1, HIGH);
    digitalWrite (pin2, HIGH);
    digitalWrite (pin3, HIGH);
    digitalWrite (pin4, HIGH);
    digitalWrite (pin5, HIGH);
  }
  else {
    digitalWrite (pin1, LOW);
    digitalWrite (pin2, LOW);
    digitalWrite (pin3, LOW);
    digitalWrite (pin4, LOW);
    digitalWrite (pin5, LOW);
  }
  delay(5000);
}
