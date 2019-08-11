#include <Adafruit_DotStar.h>
#include <SPI.h>

#define NUMPIXELS 72 // Number of LEDs in strip
#define NUMUSING 20 // Number of LEDs to actually illuminate

#define DATAPIN 4
#define CLOCKPIN 5

Adafruit_DotStar strip(NUMPIXELS, DATAPIN, CLOCKPIN, DOTSTAR_BRG);

// Buffer for holding colours sent via serial
char inputBuffer[NUMUSING * 3];

void setup() {
  // Setup serial and DotStar strip
  Serial.begin(9600);
  strip.begin();
  strip.show(); // Turn all LEDs off
}

void loop() {
  if (Serial.available() > 0) {
    // Read colours from serial
    Serial.readBytes(inputBuffer, NUMUSING * 3);
    
    // Set LED colours
    for (int i = 0; i < NUMUSING; i++) {
      strip.setPixelColor(i,
        // Note colours are sent as [R,G,B] but DotStar expects [G,R,B]
        int(inputBuffer[i*3 + 1]), int(inputBuffer[i*3]), int(inputBuffer[i*3 + 2])
      );
    }
    // Display colours on DotStar
    strip.show();
  }
}
