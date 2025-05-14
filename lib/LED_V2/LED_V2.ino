#include <FastLED.h>

#define NUM_LEDS 27 // LED數量
#define DATA_PIN 13 // LED訊號腳位
#define NUM_CYCLES 3

volatile bool StopRequested = false; // 宣告interrupt bool

CRGB leds[NUM_LEDS]; // 建立LED leds(LED暫存區)
String CommandString = ""; // 建立存放String位置

void setup() {
  FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS); // 設定LED參數<LED型號, IO腳位, 色彩順序>
  pinMode(2, INPUT_PULLUP); // Set up the button pin
  Serial.begin(9600);  // 初始化序列通訊，速率為9600bps
  
  leds[0] = CRGB::Red; // 測試LED是否正常
  FastLED.show();
  delay(1000);
  leds[0] = CRGB::Black;
  FastLED.show();
  
}

void loop() {
  if (StopRequested == true) {
    for (int i = 0; i < NUM_LEDS; i++){
      leds[i] = CRGB::Black;
    }
    FastLED.show();
    StopRequested = false;
  }
  handleSerialCommand();
}


//======= Create receive command string  =======//
void handleSerialCommand() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      CommandString.trim();
      if (CommandString == "flash_white_light_3_times" || CommandString == "1") {
        flash_white_light_3_times();
      } else if (CommandString == "LED_cycle_3_times" || CommandString == "2") {
        LED_cycle_3_times();
      } else if (CommandString == "c" || CommandString == "C"){
        StopRequested = true;
      } else {
        Serial.println("Unknown Command : " + CommandString);
      }
      CommandString = "";
    } else {
      CommandString += c;
    }
  }
}



//======= Create interrupt keyboard =======//
void CheckStop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'c' || c == 'C') {
      StopRequested = true;
    }
  }
}


//======= 單顆閃三次 =======//
void flash_white_light_3_times() {
  for (int flash = 0; flash < 3; flash++) {

    CheckStop();
    if (StopRequested == true) {
      leds[0] = CRGB::Black;
      FastLED.show();
      StopRequested = false;
      return;
    }
    leds[0] = CRGB::White; // Turn on the first LED
    FastLED.show();
    delay(500);

    CheckStop();
    if (StopRequested == true) {
      leds[0] = CRGB::Black;
      FastLED.show();
      StopRequested = false;
      return;
    }
    leds[0] = CRGB::Black; // Turn off the first LED
    FastLED.show();
    delay(500);
  }

  for (int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB::Black;
  }
  FastLED.show();
  StopRequested = false;
}

//======= 從左到右，再右到左 =======//
void LED_cycle_3_times() {
  uint8_t hue = 0;
  for (int cycle = 0; cycle < NUM_CYCLES; cycle++) {

    for (int i = 0; i < NUM_LEDS; i++) {
      CheckStop();
      if (StopRequested == true) {
        for (int j = 0; j < NUM_LEDS; j++){
          leds[j] = CRGB::Black;
        }
        FastLED.show();
        StopRequested = false;
        return;
      }
      leds[i] = CHSV(hue, 255, 255);
      if (i > 0) {
        leds[i - 1] = CRGB::Black;
      }
      FastLED.show();
      delay(250);
      hue += 5;
    }

    for (int i = NUM_LEDS - 1; i >= 0; i--) {
      CheckStop();
      if (StopRequested == true) {
        for (int j = 0; j < NUM_LEDS; j++){
          leds[j] = CRGB::Black;
        }
        FastLED.show();
        StopRequested = false;
        return;
      }
      leds[i] = CHSV(hue, 255, 255);
      if (i < NUM_LEDS - 1) {
        leds[i + 1] = CRGB::Black;
      }
      FastLED.show();
      delay(250);
      hue += 5;
    }
  }

  // Turn off all the lights
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  FastLED.show();
  StopRequested = false;
}

