# Info-Excel_dashboard

## Overview

This project is an extension of my Arduino Smart Security System. The original project works mainly as an Arduino-based security and environmental monitoring system. In this version, I added a Python data pipeline and an Excel dashboard so that the readings and access results can be saved and viewed as data.

The main idea is:

**Arduino → Serial Communication → Python → CSV File → Excel Dashboard**

The Arduino still handles the hardware side of the project. Python receives the serial messages, processes them and saves complete records into a CSV file. The Excel dashboard then uses that data to show access results and sensor information.

This is a separate project from my original Arduino-only repository. The original repository is kept separate because this repository focuses on the data logging and dashboard part.

## What the Project Does

The system has two main parts.

### 1. Arduino security and monitoring

The Arduino system uses:

- 4x4 keypad for PIN entry
- 16x2 parallel LCD
- DHT11 for temperature and humidity
- HC-SR04 for distance
- Green LED for successful access
- Red LED for denied access
- 5V buzzer for access feedback

The user enters a PIN. The Arduino checks the PIN and then gives the correct LED and buzzer response. After successful access, the sensor values are shown on the LCD.

### 2. Python and Excel data system

The Python part listens to the Arduino through the serial port. It reads messages such as:

- `SYSTEM_STARTED`
- `ACCESS_GRANTED`
- `ACCESS_DENIED`
- `TEMPERATURE:<value>`
- `HUMIDITY:<value>`
- `DISTANCE:<value>`

Python combines the related readings into one record and saves them in `arduino_data.csv`.

The dashboard updater then reads the CSV file and creates/updates an Excel workbook with:

- Total records
- Granted access count
- Denied access count
- Latest temperature
- Latest humidity
- Latest distance
- Access result chart
- Sensor reading chart

## Project Workflow

```text
+----------------------+
|      Arduino Uno     |
|                      |
| Keypad + LCD         |
| DHT11 + HC-SR04      |
| LEDs + Buzzer         |
+----------+-----------+
           |
           | Serial data
           v
+----------------------+
|   arduino_python.py  |
|                      |
| Reads and processes  |
| Arduino messages     |
+----------+-----------+
           |
           | CSV record
           v
+----------------------+
|  arduino_data.csv    |
+----------+-----------+
           |
           | Python updater
           v
+------------------------------+
| Smart_Security_Auto_Dashboard|
|          .xlsx                |
|                              |
| Data + Dashboard + Charts    |
+------------------------------+
```

## Hardware

| Component | Purpose |
|---|---|
| Arduino Uno | Main controller |
| 4x4 Keypad | PIN input |
| 16x2 LCD | User interface and sensor display |
| DHT11 | Temperature and humidity |
| HC-SR04 | Distance measurement |
| Green LED | Access granted indication |
| Red LED | Access denied indication |
| 5V Buzzer | Sound feedback |

## Current Pin Setup

The hardware setup used for the extended project is documented here so that the Python/data part can be understood together with the Arduino system.

| Component | Arduino pin |
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

> Note: D0 and D1 are the Arduino hardware serial pins. Because the exact working Arduino serial/keypad code is not stored in this new repository yet, the final `.ino` file should be added from the tested local version rather than using a different pin arrangement. I am keeping this repository from silently changing the working hardware setup.

## Python Part

### `arduino_python.py`

This program connects Python to the Arduino using `pyserial`.

The current local setup uses:

- Port: `COM4`
- Baud rate: `9600`

The program creates the CSV file if it does not already exist. It waits for Arduino messages and builds complete sensor records.

For a denied access event, it saves the access result directly because there are no sensor values needed for that event.

For a granted event, it waits until temperature, humidity and distance have all been received. Then it saves one complete record.

After saving a record, the program runs `update_dashboard.py` so that the Excel dashboard can be updated automatically.

## CSV Data

The CSV file uses these columns:

```text
Date,Time,Access,Temperature_C,Humidity_percent,Distance_cm
```

Example structure:

```text
2026-10-24,23:52:09,GRANTED,24.3,55.3,11.7
```

The CSV file is useful because it keeps the raw project data in a simple format that can be opened by Excel, Python or other data tools.

## Excel Dashboard

The Excel workbook is designed to make the collected data easier to understand.

The updater creates three sheets:

- `Data` — the collected records
- `Dashboard` — summary values and charts
- `ChartsData` — helper data used by the charts

The dashboard is updated from the CSV file instead of requiring every value to be entered manually.

The workbook currently includes an access result chart and a sensor readings chart. The dashboard can be improved later with more charts or filters if needed.

## Automatic Update Flow

The important part of this project is that the dashboard does not depend on manually copying every Arduino reading into Excel.

When a complete Arduino event is received:

1. Python reads the serial messages.
2. Python stores the temperature, humidity and distance values.
3. Python writes one row into the CSV file.
4. Python starts `update_dashboard.py`.
5. The updater reads the latest CSV data.
6. The Excel workbook is recreated/updated.
7. The dashboard contains the latest project data.

## Software Used

- Arduino IDE
- Arduino C/C++
- Python 3.14.2
- VS Code
- `pyserial`
- `openpyxl`
- Microsoft Excel
- Git and GitHub

## Python Installation

Install the required Python libraries with:

```bash
pip install -r requirements.txt
```

Then make sure the Arduino is connected to the correct COM port.

For this setup the port is:

```text
COM4
```

The Arduino Serial Monitor should be closed while `arduino_python.py` is using the same serial connection.

## Running the Project

### Step 1 — Start the Arduino

Upload the tested Arduino program and connect the Arduino Uno to the computer.

### Step 2 — Check the COM port

Make sure the Python file is using the correct port. The current setup uses `COM4`.

### Step 3 — Start Python

From the `python` folder, run:

```bash
python arduino_python.py
```

Python should connect to the Arduino and wait for serial messages.

### Step 4 — Use the security system

Enter the PIN on the keypad. The Arduino will handle the access result and sensor readings.

### Step 5 — Check the data

The new record will be added to:

```text
data/arduino_data.csv
```

### Step 6 — Check the dashboard

The Excel dashboard will be updated by the Python script.

## Project Structure

```text
Info-Excel_dashboard/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── arduino/
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

The Excel workbook is a binary `.xlsx` file, so it cannot be created through the text-only GitHub file interface used here. I will add it to the repository when the actual workbook file is available for upload. The same applies to project photos and videos.

## Testing and Debugging

During development, the main difficulty was getting all parts of the Arduino project to work together at the same time. The LCD, keypad, DHT11, ultrasonic sensor, LEDs and buzzer could work individually but combining them required repeated wiring and code testing.

The Python side also needed testing because serial messages arrive separately. A granted access event is not one single message. The access message, temperature, humidity and distance messages have to be connected into one complete record before writing the row to the CSV file.

Another issue was making sure that the Python scripts used the correct absolute/project paths. After fixing the paths and the duplicate workbook issue, the Arduino-to-CSV-to-Excel pipeline was successfully tested.

## What I Learned

This project helped me understand more than just Arduino sensor code. I worked with a complete small data pipeline.

I learned how to:

- Read sensor data from Arduino
- Send structured information through serial communication
- Read serial data in Python
- Parse different message types
- Store data in CSV format
- Work with files and project paths in Python
- Use `openpyxl` to create and update Excel workbooks
- Create charts from collected data
- Connect hardware data with software and data analysis
- Debug a project where hardware and software depend on each other
- Organize a project into separate hardware, Python, data and dashboard sections

## Future Improvements

Some possible future improvements are:

- Add more detailed access logs
- Add date and time filters to the dashboard
- Add more sensor charts
- Add a better event history view
- Add a cleaner dashboard layout
- Add automatic alerts for unusual distance or environmental readings
- Move from CSV storage to a database for a larger project
- Build a web dashboard in a future version
- Add more security features to the Arduino system

These are future ideas. They are not part of the current project unless they are added later.

## Images

Project photos and screenshots will be added later in the `images` folder. I want the repository to show the real hardware, the serial output and the Excel dashboard instead of using unrelated stock images.

## Status

**Current status: Working prototype with Arduino → Python → CSV → Excel data flow tested.**

The hardware project and the data/dashboard project are intentionally kept as separate GitHub repositories.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
