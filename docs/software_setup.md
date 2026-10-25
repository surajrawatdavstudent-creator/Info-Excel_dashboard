# Software Setup

## Python

Install Python 3 and open a terminal at the repository root. Install the listed Python dependencies:

```bash
python -m pip install -r requirements.txt
```

The current `requirements.txt` includes:

- `pyserial` — Arduino USB Serial communication
- `openpyxl` — read/write the Excel workbook and create charts

## Arduino IDE

Install the Arduino libraries required by `arduino/Smart_Security_System.ino`:

- `Keypad`
- `DHT sensor library`

If the DHT library installer asks for an additional dependency, install it as well.

## Run order

1. Connect the Arduino Uno by USB and upload the sketch.
2. Confirm the COM port in `python/arduino_python.py` (currently `COM4`).
3. Close the Arduino Serial Monitor.
4. From the repository root, run `python python/arduino_python.py`.
5. Use the keypad and check `data/arduino_data.csv`.
6. Open `dashboard/Smart_Security_Auto_Dashboard.xlsx`.

## Troubleshooting

- **COM port unavailable:** close Serial Monitor and other programs using the Arduino port; confirm the port in Device Manager/Arduino IDE.
- **Dashboard not updated:** check that the CSV path is valid and that the Python terminal shows no permission error. Close the workbook in Excel if it is locked or open read-only.
- **No sensor record:** a granted access record is saved only after Python receives temperature, humidity and distance messages. A distance error is still recorded as `ERROR`.
- **Keypad/Serial instability:** the current wiring shares D0/D1 between the keypad and hardware Serial. This is a known pin-allocation issue to address in a future hardware revision.
