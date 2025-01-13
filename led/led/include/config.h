#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// Function to get WiFi credentials from environment
class Config {
public:
    static String getWiFiSSID() {
        #ifdef WIFI_SSID
            return String(WIFI_SSID);
        #else
            return String("default_ssid");
        #endif
    }
    
    static String getWiFiPassword() {
        #ifdef WIFI_PASSWORD
            return String(WIFI_PASSWORD);
        #else
            return String("default_password");
        #endif
    }
};

#endif

