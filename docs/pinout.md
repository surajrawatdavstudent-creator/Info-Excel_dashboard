# Pinout

## Current hardware setup

| Component | Pin |
|---|---|
| Red LED | D2 |
| Green LED | D3 |
| DHT11 | D4 |
| Buzzer | D5 |
| HC-SR04 Echo | D6 |
| HC-SR04 Trig | D7 |
| LCD RS | D8 |
| LCD E | D9 |
| LCD D4 | D10 |
| LCD D5 | D11 |
| LCD D6 | D12 |
| LCD D7 | D13 |
| Keypad Row 1 | A0 |
| Keypad Row 2 | A1 |
| Keypad Row 3 | A2 |
| Keypad Row 4 | A3 |
| Keypad Column 1 | A4 |
| Keypad Column 2 | A5 |
| Keypad Column 3 | D0 |
| Keypad Column 4 | D1 |

## Important note about serial communication

Arduino Uno uses D0 and D1 for the hardware serial connection. The current hardware setup also uses these pins for two keypad columns.

Because of this, the exact tested Arduino `.ino` file is important. This repository does not replace that tested wiring with a new pin arrangement. The working Arduino code should be added from the local tested version when it is available.
