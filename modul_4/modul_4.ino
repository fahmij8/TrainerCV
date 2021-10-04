#include <AntaresESP32HTTP.h>

#define ACCESSKEY "your-access-key" // get ur acces key on your antares account
#define WIFISSID "your-wifi-ssid" // input ur wifi ssid
#define PASSWORD "your-wifi-password" // input ur wifi password
#define projectName "your-project-name" // input ur antares project name on antares application 
#define deviceName "your-project-name" // input ur antares device name on antares application
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

static const int servoPin = 14;
int servo = 0;

Servo servo1;
AntaresESP32HTTP antares(ACCESSKEY);
LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
    Serial.begin(115200);
    antares.setDebug(true);
    antares.wifiConnection(WIFISSID, PASSWORD);
    lcd.init();                      // initialize the lcd 
    lcd.backlight();                 // turn on LCD backlight
    servo1.attach(servoPin);
}

void loop() {
  // Get the latest data from your Antares device
  antares.get(projectName, deviceName);
    String fruit = antares.getString("fruit");
    float conf = antares.getFloat("confidence");

    if (conf <= 50) {
      servo = 180;
      servo1.write (servo);
      Serial.println (servo);
    }
    else {
      servo = 0;
      servo1.write (servo);
      Serial.println (servo);
    }
    
    Serial.println("fruit: " + (fruit));
    Serial.println("confidence: " + String(conf)+"%");
    
    lcd.setCursor (0,0);
    lcd.print ("fruit: " + (fruit));
    lcd.setCursor (0,1);
    lcd.print ("ripeness: " + String(conf)+ "%");
delay (5000);
}
