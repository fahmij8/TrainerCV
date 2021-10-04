#include <AntaresESP32HTTP.h>

#define ACCESSKEY "your-access-key" // get ur acces key on your antares account
#define WIFISSID "your-wifi-ssid" // input ur wifi ssid
#define PASSWORD "your-wifi-password" // input ur wifi password

#define projectName "your-project-name" // input ur antares project name on antares application 
#define deviceName "your-project-name" // input ur antares device name on antares application
AntaresESP32HTTP antares(ACCESSKEY);
int ledpin = 27;

void setup() {
    Serial.begin(115200);
    antares.setDebug(true);
    antares.wifiConnection(WIFISSID, PASSWORD);
    pinMode (ledpin, OUTPUT);
}

void loop() {
  // Get the latest data from your Antares device
  antares.get(projectName, deviceName);
    int led = antares.getInt("led");

    Serial.println("led: " + (led));
  delay(5000);
  if (led == 1) {
    digitalWrite (ledpin, HIGH);
  }
  else {
    digitalWrite (ledpin, LOW);
  }
}
