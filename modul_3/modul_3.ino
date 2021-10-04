#include <AntaresESP32HTTP.h>

#define ACCESSKEY "your-access-key" // get ur acces key on your antares account
#define WIFISSID "your-wifi-ssid" // input ur wifi ssid
#define PASSWORD "your-wifi-password" // input ur wifi password

#define projectName "your-project-name" // input ur antares project name on antares application 
#define deviceName "your-project-name" // input ur antares device name on antares application
AntaresESP32HTTP antares(ACCESSKEY);

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
    Serial.begin(115200);
    antares.setDebug(true);
    antares.wifiConnection(WIFISSID, PASSWORD);
    lcd.init();                      // initialize the lcd 
    lcd.backlight();                 // turn on LCD backlight
}

void loop() {
  // Get the latest data from your Antares device
  antares.get(projectName, deviceName);
    String colour = antares.getString("colour");

    Serial.println("colour: " + (colour));
    lcd.setCursor (0,0);
    lcd.print ("colour: " + (colour));
delay (5000);
}
