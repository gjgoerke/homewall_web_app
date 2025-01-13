#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <NeoPixelBus.h>
#include <ArduinoJson.h>
#include "config.h"

#define LED_PIN     5
#define NUM_LEDS    350

// Static IP configuration
IPAddress staticIP(10, 0, 0, 250);     
IPAddress gateway(10, 0, 0, 1);        // Router
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(8, 8, 8, 8);            // Google DNS

WebServer server(80);
NeoPixelBus<NeoRgbFeature, NeoEsp32Rmt0Ws2811Method> strip(NUM_LEDS, LED_PIN);

void handleLights() {
    if (server.hasArg("plain")) {
        String message = server.arg("plain");
        DynamicJsonDocument doc(1024);
        DeserializationError error = deserializeJson(doc, message);
        
        if (error) {
            Serial.println("JSON Parse Error");
            return;
        }

        JsonArray holds = doc["holds"];
        if (!holds) {
            Serial.println("No holds array found");
            return;
        }

        strip.ClearTo(RgbColor(0, 0, 0));
        
        // Debug print
        Serial.print("Number of holds: ");
        Serial.println(holds.size());
        
        for (JsonVariant hold : holds) {
            int index = hold["index"].as<int>();  // Explicit conversion
            int type = hold["type"].as<int>();    // Explicit conversion
            
            // Debug print
            Serial.print("Hold - Index: ");
            Serial.print(index);
            Serial.print(", Type: ");
            Serial.println(type);
            
            if (index < 0 || index >= NUM_LEDS) {
                Serial.println("Index out of bounds!");
                continue;
            }
            
            RgbColor color;
            switch(type) {
                case 1: color = RgbColor(0, 255, 0); break;   // Start
                case 2: color = RgbColor(255, 0, 0); break;   // Finish
                case 3: color = RgbColor(0, 0, 255); break;   // General
                case 4: color = RgbColor(255, 0, 255); break; // Feet
                case 5: color = RgbColor(255, 255, 0); break; // Hands
                default: 
                    Serial.println("Invalid type!");
                    continue;
            }
            
            strip.SetPixelColor(index, color);
        }
        strip.Show();
        
        server.send(200, "application/json", "{\"status\":\"success\"}");
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    String ssid = Config::getWiFiSSID();
    String password = Config::getWiFiPassword();

    Serial.println("\n\nStarting fresh connection attempt...");
    
    // Full WiFi reset without ESP restart
    WiFi.persistent(false);
    WiFi.disconnect(true);
    delay(1000);
    WiFi.mode(WIFI_STA);
    delay(1000);
    

    Serial.println("Scanning for networks...");
    int n = WiFi.scanNetworks();
    if (n == 0) {
        Serial.println("No networks found!");
    } else {
        Serial.printf("%d networks found\n", n);
        for (int i = 0; i < n; ++i) {
            Serial.printf("%d: %s (Strength: %d dBm)\n", 
                i + 1, 
                WiFi.SSID(i).c_str(), 
                WiFi.RSSI(i)
            );
        }
    }
    
    Serial.printf("\nAttempting to connect to: %s\n", ssid);
    WiFi.begin(ssid, password);
    
    int attempts = 0;
    while (attempts < 30) {
        int status = WiFi.status();
        Serial.printf("Status: %d - ", status);
        
        switch(status) {
            case WL_DISCONNECTED:
                Serial.println("Disconnected - retrying");
                break;
            case WL_CONNECTED:
                Serial.println("Connected!");
                goto connected;
            case WL_CONNECT_FAILED:
                Serial.println("Connection failed - check password");
                break;
            case WL_NO_SSID_AVAIL:
                Serial.println("Network not found");
                break;
            default:
                Serial.printf("Other status: %d\n", status);
        }
        
        delay(1000);
        attempts++;
        
        if (attempts % 5 == 0) {
            Serial.println("\nDebug Info:");
            Serial.printf("RSSI: %d dBm\n", WiFi.RSSI());
            Serial.printf("Mode: %d\n", WiFi.getMode());
        }
    }
    
connected:
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nConnection established!");
        Serial.printf("Connected to: %s\n", WiFi.SSID().c_str());
        Serial.printf("IP address: %s\n", WiFi.localIP().toString().c_str());
        Serial.printf("Channel: %d\n", WiFi.channel());
        Serial.printf("RSSI: %d dBm\n", WiFi.RSSI());
    } else {
        Serial.println("\nFailed to connect");
    }
    
    // Configure static IP
    if (!WiFi.config(staticIP, gateway, subnet, dns)) {
        Serial.println("Static IP Configuration Failed");
    } else {
        Serial.println("Static IP Configuration Success");
    }
    
    // Initialize NeoPixelBus
    strip.Begin();
    strip.Show();

    // Handle CORS preflight
    server.on("/lights", HTTP_OPTIONS, []() {
        server.sendHeader("Access-Control-Allow-Origin", "*");
        server.sendHeader("Access-Control-Allow-Methods", "POST,GET,OPTIONS");
        server.sendHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        server.send(200, "text/plain", "");
    });

    // Handle POST request
    server.on("/lights", HTTP_POST, []() {
        server.sendHeader("Access-Control-Allow-Origin", "*");
        handleLights();
    });

    server.begin();
}

void loop() {
    server.handleClient();
}