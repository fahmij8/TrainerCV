#include <AntaresESP32HTTP.h>
#include <WiFi.h>

#define ACCESSKEY "9634da50ff7abd7a:3bdb608765b907a4"
#define projectName "TrainerCV"
#define deviceName "LED1"

const char* ssid = "BigYellow";
const char* password = "thethepooh71";

AntaresESP32HTTP antares(ACCESSKEY);

void setup() {
  Serial.begin(115200);
  antares.setDebug(true);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  antares.get(projectName, deviceName);
  digitalWrite(LED_BUILTIN, antares.getInt("state"));
}
