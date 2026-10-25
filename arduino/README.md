# Arduino Part

The Arduino side is the hardware part of this project.

It handles:

- PIN input through the 4x4 keypad
- Access checking
- LCD messages
- DHT11 temperature and humidity readings
- HC-SR04 distance readings
- Green and red LED feedback
- Buzzer feedback
- Serial messages for the Python data logger

The current tested hardware pin arrangement is documented in [`../docs/pinout.md`](../docs/pinout.md).

The final Arduino `.ino` file is intentionally not recreated from a different version of the old project. The old repository and this extended repository must stay separate, and the exact tested serial-enabled Arduino code should be added from the local working project so that the hardware setup is not changed accidentally.
