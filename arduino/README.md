# Arduino Part

The Arduino side is the hardware and serial-data part of this project.

It handles:

- PIN input through the 4x4 keypad
- Access checking
- DHT11 temperature and humidity readings
- HC-SR04 distance readings
- Green and red LED feedback
- Buzzer feedback
- Serial messages for the Python data logger

The current Arduino code is `Smart_Security_System.ino`.

## Current security settings

- PIN: `111`
- Enter key: `4`
- `*`: clear the PIN when locked / lock the system after access is granted

## Current display setup

The LCD is **not used in the current tested version**. Python and the Excel dashboard are the main display and data-analysis part of this extended project.

An LCD can be added later using the free D8-D13 pins, but that would require updating the Arduino code and should be treated as a later hardware version.

## Serial output

The Arduino sends messages such as:

- `SYSTEM_STARTED`
- `ACCESS_GRANTED`
- `ACCESS_DENIED`
- `TEMPERATURE:<value>`
- `HUMIDITY:<value>`
- `DISTANCE:<value>`
- `DISTANCE:ERROR`

The Python logger uses these messages to build complete records in the CSV file.

The current tested pin arrangement is documented in [`../docs/pinout.md`](../docs/pinout.md).
