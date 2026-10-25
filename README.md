# Info-Excel_dashboard

## Overview

This project is an extended version of my Arduino Smart Security System. The main difference is that this version connects the Arduino project to a Python data pipeline and an Excel dashboard.

The main workflow is:

**Arduino → Serial Communication → Python → CSV → Excel Dashboard**

The original Arduino-only project is kept in a separate repository. This repository focuses on collecting, processing and displaying the project data.

## What the project does

### Arduino

The Arduino handles:

- 4x4 keypad PIN entry
- Access checking
- DHT11 temperature and humidity readings
- HC-SR04 distance readings
- Green LED for granted access
- Red LED for denied access
- 5V buzzer for feedback
- Serial communication with Python

The current version is **LCD-free**. The LCD was removed because Python and the Excel dashboard are the main display and data-analysis part of this project.

Current security settings:

- PIN: `111`
- Enter key: `4`
- `*`: clear the PIN / lock the system

### Python

Python receives the Arduino serial messages and combines the sensor readings into complete records.

The main Python files are:

- `python/arduino_python.py` — reads Arduino data and saves records to CSV
- `python/update_dashboard.py` — reads the CSV and updates the Excel dashboard

### CSV

The collected data is stored in:

`data/arduino_data.csv`

Columns:

```text
Date,Time,Access,Temperature_C,Humidity_percent,Distance_cm
```

### Excel dashboard

The dashboard contains:

- Total access attempts
- Granted access count
- Denied access count
- Latest temperature
- Latest humidity
- Latest distance
- Access result chart
- Temperature chart
- Humidity chart
- Distance chart

The current tested dashboard data is included in the repository CSV.

## Current pin setup

| Component | Arduino pin |
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

The full pin information is in [`docs/pinout.md`](docs/pinout.md).

### LCD later

The LCD is currently disconnected. D8-D13 are available for a future LCD version:

| LCD | Arduino |
|---|---|
| RS | D8 |
| E | D9 |
| D4 | D10 |
| D5 | D11 |
| D6 | D12 |
| D7 | D13 |

This is a future hardware version and is not part of the current Arduino code.

## Important Serial note

Arduino Uno uses D0 and D1 for hardware Serial. The current keypad also uses D0 and D1 for two keypad columns. This can cause interference between the keypad and USB Serial connection.

The current code keeps the tested project pin arrangement. If this becomes unstable during further hardware testing, the better next revision is to move the two keypad columns away from D0/D1.

## Python setup

Python version used during development: **Python 3.14.2**

Required libraries are listed in `requirements.txt`:

```text
pyserial
openpyxl
```

Install them with:

```bash
pip install -r requirements.txt
```

The current local Arduino connection uses:

```text
COM4
9600 baud
```

Close the Arduino Serial Monitor before running the Python logger because both programs cannot use the same Serial connection at the same time.

## Running the project

### 1. Upload the Arduino code

Open:

```text
arduino/Smart_Security_System.ino
```

Upload it to the Arduino Uno.

### 2. Connect the Arduino

Check that the Arduino is connected to the correct COM port.

### 3. Run the Python logger

From the project folder:

```bash
python python/arduino_python.py
```

The Python program waits for Arduino messages.

### 4. Use the keypad

Enter:

```text
111
```

Then press:

```text
4
```

For a correct PIN, the Arduino sends `ACCESS_GRANTED` and starts sending sensor readings.

For a wrong PIN, it sends `ACCESS_DENIED`.

### 5. Check the CSV

Python saves the data to:

```text
data/arduino_data.csv
```

### 6. Check the Excel dashboard

After a complete record is saved, Python automatically runs `update_dashboard.py` and updates the dashboard workbook.

## Arduino serial messages

The Arduino sends messages such as:

```text
SYSTEM_STARTED
ACCESS_GRANTED
TEMPERATURE:27.3
HUMIDITY:48.3
DISTANCE:7.8
```

For a distance reading that fails:

```text
DISTANCE:ERROR
```

Python waits for a complete granted record containing temperature, humidity and distance before saving it as one CSV row.

## Project structure

```text
Info-Excel_dashboard/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── arduino/
│   ├── Smart_Security_System.ino
│   └── README.md
│
├── python/
│   ├── arduino_python.py
│   └── update_dashboard.py
│
├── data/
│   └── arduino_data.csv
│
├── dashboard/
│   └── README.md
│
├── docs/
│   └── pinout.md
│
└── images/
    └── README.md
```

## What I learned

This project helped me work with both hardware and software instead of only writing Arduino code.

I worked with:

- Arduino sensor readings
- Keypad input and access logic
- Serial communication
- Python file handling
- Serial data parsing
- CSV data storage
- `pyserial`
- `openpyxl`
- Excel charts
- Automatic dashboard updates
- Debugging hardware and software together

## Future improvements

Possible future improvements include:

- Move keypad Serial-conflicting pins away from D0/D1
- Add the LCD again as an optional local display
- Add more dashboard filters
- Add more sensor charts
- Add a better event history section
- Add alerts for unusual readings
- Store larger datasets in a database
- Build a web dashboard in a future version

These are future ideas and are not claimed as completed features.

## Images and dashboard file

The project photos and screenshots will be added to `images/` from the actual project. The planned screenshots are:

- Full Arduino setup
- Arduino close-up
- Access granted
- Access denied
- Python serial output
- CSV data
- Excel dashboard
- Full Arduino → Python → CSV → Excel pipeline

The actual `.xlsx` dashboard is also part of the local working project. The current GitHub connector can write UTF-8 text files, but it cannot upload binary `.xlsx` files or image files. Therefore the workbook and screenshots still need to be uploaded through the normal GitHub web interface.

## Status

**Working prototype:** Arduino → Python → CSV → Excel dashboard has been tested with real project data.

The hardware repository and this data/dashboard repository are intentionally kept separate.
