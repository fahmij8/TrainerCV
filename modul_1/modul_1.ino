#include <DHT.h>
#include <LiquidCrystal.h>

//init sensor
DHT dht(2, DHT11); //Pin, Jenis DHT

//init lcd pins interface
LiquidCrystal lcd (13, 12, 9, 8, 7, 6);

//variabel dht11
float kelembaban;
float suhu;

//variabel led
int led_hijau = 3;
int led_kuning =4;
int led_merah = 5;

void setup()
{
Serial.begin(9600);
dht.begin();
lcd.begin(16, 2);

//pin led mode
pinMode(led_hijau, OUTPUT);
pinMode(led_kuning, OUTPUT);
pinMode(led_merah, OUTPUT);

}

void loop()
{
  delay(2000);
  
 kelembaban = dht.readHumidity();
 suhu = dht.readTemperature();

 if(suhu >= 0 && suhu <=25){
  digitalWrite(led_hijau, HIGH);
  digitalWrite(led_kuning, LOW);
  digitalWrite(led_merah, LOW);
 }
 else if (suhu >= 26 && suhu <= 35) {
  digitalWrite(led_hijau, LOW);
  digitalWrite(led_kuning, HIGH);
  digitalWrite(led_merah, LOW);
 }
 else if (suhu >= 36 && suhu <= 50) {
  digitalWrite(led_hijau, LOW);
  digitalWrite(led_kuning, LOW);
  digitalWrite(led_merah, HIGH);
 }
 else {
  digitalWrite(led_hijau, LOW);
  digitalWrite(led_kuning, LOW);
  digitalWrite(led_merah, LOW);
 }

 //print lcd
 lcd.setCursor(0,0);
 lcd.print("Suhu: ");
 lcd.print(suhu);
 delay(10);
 lcd.print("  ");
 delay(10);
 lcd.setCursor(0,1);
 if(suhu >= 0 && suhu <=25){
 lcd.print("Sejuk");
 lcd.print("           ");
 delay(10);
 }
 else if (suhu >= 26 && suhu <= 35) {
 lcd.print("Hareudang");
 lcd.print("           ");
 delay(10);
 }
 else if (suhu >= 36 && suhu <= 50) {
  lcd.print("Panas cuk!!!");
  lcd.print("           ");
  delay(10);
 }
 else {
  lcd.print("Sensing...");
  lcd.print("           ");
  delay(10);
 }
 
 //print serial monitor
 Serial.print("kelembaban: ");
 Serial.print(kelembaban);
 Serial.print(" ");
 Serial.print("suhu: ");
 Serial.println(suhu);
}
