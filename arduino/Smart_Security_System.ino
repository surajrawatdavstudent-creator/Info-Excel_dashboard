#include <Keypad.h>
#include <DHT.h>

// =========================
// PIN DEFINITIONS
// =========================

#define RED_LED 2
#define GREEN_LED 3

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define BUZZER 5

#define ECHO_PIN 6
#define TRIG_PIN 7

// =========================
// KEYPAD
// =========================

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {A0, A1, A2, A3};
byte colPins[COLS] = {A4, A5, 0, 1};

Keypad keypad = Keypad(
  makeKeymap(keys),
  rowPins,
  colPins,
  ROWS,
  COLS
);

// =========================
// SECURITY SETTINGS
// =========================

String correctPIN = "111";
String enteredPIN = "";
bool accessGranted = false;

// =========================
// SENSOR VALUES
// =========================

float temperature = 0;
float humidity = 0;
float distance = 0;

// =========================
// TIMERS
// =========================

unsigned long lastDHT = 0;
unsigned long lastDistance = 0;

// =========================
// SETUP
// =========================

void setup() {
  Serial.begin(9600);

  dht.begin();

  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
  noTone(BUZZER);

  Serial.println("SYSTEM_STARTED");
  Serial.println("ENTER_PIN");
}

// =========================
// MAIN LOOP
// =========================

void loop() {
  // =========================
  // LOCKED MODE
  // =========================

  if (!accessGranted) {
    char key = keypad.getKey();

    if (key) {
      Serial.print("KEY:");
      Serial.println(key);

      if (key == '*') {
        enteredPIN = "";
        digitalWrite(RED_LED, LOW);
        noTone(BUZZER);
        Serial.println("PIN_CLEARED");
        Serial.println("ENTER_PIN");
      }
      else if (key == '4') {
        checkPIN();
      }
      else if (key >= '0' && key <= '9') {
        if (enteredPIN.length() < 8) {
          enteredPIN += key;
          Serial.print("PIN_LENGTH:");
          Serial.println(enteredPIN.length());
        }
      }
    }

    return;
  }

  // =========================
  // UNLOCKED MODE
  // =========================

  char key = keypad.getKey();

  if (key == '*') {
    accessGranted = false;
    enteredPIN = "";
    digitalWrite(GREEN_LED, LOW);
    noTone(BUZZER);
    Serial.println("SYSTEM_LOCKED");
    Serial.println("ENTER_PIN");
    return;
  }

  // =========================
  // READ DHT11
  // =========================

  if (millis() - lastDHT >= 2000) {
    lastDHT = millis();

    float newHumidity = dht.readHumidity();
    float newTemperature = dht.readTemperature();

    if (!isnan(newHumidity) && !isnan(newTemperature)) {
      humidity = newHumidity;
      temperature = newTemperature;

      Serial.print("TEMPERATURE:");
      Serial.println(temperature, 1);

      Serial.print("HUMIDITY:");
      Serial.println(humidity, 1);
    }
  }

  // =========================
  // READ DISTANCE
  // =========================

  if (millis() - lastDistance >= 1000) {
    lastDistance = millis();

    distance = getDistance();

    if (distance >= 0) {
      Serial.print("DISTANCE:");
      Serial.println(distance, 1);
    }
    else {
      Serial.println("DISTANCE:ERROR");
    }
  }
}

// =========================
// CHECK PIN
// =========================

void checkPIN() {
  if (enteredPIN == correctPIN) {
    accessGranted = true;

    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);

    Serial.println("ACCESS_GRANTED");

    tone(BUZZER, 1000);
    delay(250);
    noTone(BUZZER);

    enteredPIN = "";
    delay(500);
  }
  else {
    accessGranted = false;

    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, HIGH);

    Serial.println("ACCESS_DENIED");

    tone(BUZZER, 1000);
    delay(3000);
    noTone(BUZZER);

    digitalWrite(RED_LED, LOW);
    enteredPIN = "";

    Serial.println("ENTER_PIN");
  }
}

// =========================
// HC-SR04 DISTANCE
// =========================

float getDistance() {
  float total = 0;
  byte validReadings = 0;

  for (byte i = 0; i < 5; i++) {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000);

    if (duration > 0) {
      float d = duration * 0.0343 / 2.0;

      if (d >= 2 && d <= 400) {
        total += d;
        validReadings++;
      }
    }

    delay(10);
  }

  if (validReadings > 0) {
    return total / validReadings;
  }

  return -1;
}
