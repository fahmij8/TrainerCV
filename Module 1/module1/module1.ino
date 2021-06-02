#include <AntaresESP32HTTP.h>
#include <WiFi.h>

///////// EDIT HERE /////////
#define ACCESSKEY "" // Antares Key
#define projectName "" // Antares Project Name
#define deviceName "" // Antares Device Name
/////////////////////////////

const char* ssid = "";
const char* password = "";

AntaresESP32HTTP antares(ACCESSKEY);

void setup() {
  Serial.begin(9600);
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
  int status = antares.getInt("led");
  if(status == 1){
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
