# Pinout

## Current LCD-free hardware setup

| Component | Pin |
|---|---|
| Red LED | D2 |
| Green LED | D3 |
| DHT11 | D4 |
| Buzzer | D5 |
| HC-SR04 Echo | D6 |
| HC-SR04 Trig | D7 |
| Keypad Row 1 | A0 |
| Keypad Row 2 | A1 |
| Keypad Row 3 | A2 |
| Keypad Row 4 | A3 |
| Keypad Column 1 | A4 |
| Keypad Column 2 | A5 |
| Keypad Column 3 | D0 |
| Keypad Column 4 | D1 |

## Security settings

- PIN: `111`
- Enter key: `4`
- `*`: clear / lock

## LCD later

The LCD is currently disconnected. If it is added later, the available D8-D13 pins can be used as follows:

| LCD | Arduino |
|---|---|
| RS | D8 |
| E | D9 |
| D4 | D10 |
| D5 | D11 |
| D6 | D12 |
| D7 | D13 |
| RW | GND |

The LCD power and contrast connections are not included in the digital pin table.

## Important note about serial communication

Arduino Uno uses D0 and D1 for the hardware serial connection. The current keypad also uses D0 and D1 for two keypad columns.

This means the keypad and USB Serial connection can interfere with each other. The current `.ino` file documents the tested project arrangement; if this causes unstable serial/keypad behavior, the next hardware revision should move the keypad columns away from D0/D1 rather than changing the LCD pins.
