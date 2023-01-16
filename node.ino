#include <Esp32WifiManager.h>
#include <wifi.h>
#include <PubSubClient.h>
#include <Arduino.h>
#include <Wire.h>
#include "Adafruit_SHT31.h"


Adafruit_SHT31 sht31 = Adafruit_SHT31();
const char* mqtt_server = "192.168.1.23";  // IP  brokeru
const int mqtt_port = 1883;   // port pre MQTT
WiFiClient espClient;
PubSubClient client(espClient);

char msg[50];

const char* outTopicSensorTemp = "sensors/5/40/temperature"; // topic pre MQTT
const char* outTopicSensorHum = "sensors/5/40/humidity";

IPAddress ip;

void setup_wifi() {

  delay(1000);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");

  WiFi.begin("", "");  // SSID a heslo na wifi
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print(" Node IP address: ");
  ip = WiFi.localIP();
  Serial.println(ip);
}

void mqtt_reconnect() {

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("\nAttempting MQTT connection...");
    // Attempt to connect


    if (client.connect("ESP32", "", "")) {  // id, user, heslo pre MQTT broker
      Serial.println("connected");
      delay(5000);
    }
  }
}

int setup_mqtt() {
  return 0;
}

void setup() {

  Serial.begin(115200);
  Serial.setTimeout(2000);
  setup_wifi();
  setup_mqtt();
    if (! sht31.begin(0x44)) 
  {
    Serial.println("Couldn't find SHT31");
    while (1) delay(1);
  }
     float t = sht31.readTemperature();
     float h = sht31.readHumidity();
  char t_char[8];
  dtostrf(t, 6, 2, t_char);
  char h_char[8];
  dtostrf(h, 6, 2, h_char);
  
  
 if (!client.connected()) {
    mqtt_reconnect();
    delay(5000);
      client.publish(outTopicSensorTemp , t_char);
      Serial.println("temperature sent: ");
      Serial.print(t_char);
    
      client.publish(outTopicSensorHum, h_char);
      Serial.println("humidity sent: ");
      Serial.print(h_char);
      
  }
     delay(5000);
     Serial.println(" uspavam sa na 15 minut");
     ESP.deepSleep(900000000);  // 900000000 μs == 15 minut

}
void loop() {
  //loop je prazdny, ked sa zobudim z deepsleepu tak prejdem cely setup
}
