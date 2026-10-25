# Smart Security & Environment Monitoring Dashboard

An Arduino-based security and environment monitor connected to a Python data logger and an Excel dashboard.

**Main data flow:** Arduino Uno → USB Serial → Python → CSV → Excel dashboard

## Project walkthrough

[Open the project walkthrough video on Google Drive](https://drive.google.com/file/d/1Qj_1bu2bIDUAIvxpoCSPEvIi8YaIgc9X/view?usp=drivesdk)

The shared video is linked here as the project walkthrough. If the Drive file is not publicly viewable, viewers may need permission from the owner.

## Project evidence

The evidence belongs in the `images/` folder. The file names and their intended purpose are listed in [images/README.md](images/README.md). The actual image files must be committed before a gallery can render in GitHub.

## What it does

- Takes a PIN through a 4×4 keypad.
- Uses a green LED and short buzzer beep for accepted access.
- Uses a red LED and longer buzzer sound for rejected access.
- Reads temperature and humidity with a DHT11.
- Measures distance with an HC-SR04 ultrasonic sensor.
- Sends serial messages from Arduino to Python.
- Saves access events and sensor readings to `data/arduino_data.csv`.
- Rebuilds the Excel workbook from the CSV so the summary values and charts reflect the saved records.

## Current security controls

| Control | Value |
|---|---|
| PIN | `111` |
| Enter key | `4` |
| Clear / lock key | `*` |
| Serial baud rate | `9600` |
| Current Arduino port in Python | `COM4` |

Change `PORT` in `python/arduino_python.py` if Windows assigns a different COM port.

## Hardware

| Component | Role |
|---|---|
| Arduino Uno | Main controller |
| 4×4 membrane keypad | PIN input |
| DHT11 | Temperature and humidity |
| HC-SR04 | Distance measurement |
| Green LED | Access granted indicator |
| Red LED | Access denied indicator |
| 5V buzzer | Sound feedback |
| Breadboard and jumper wires | Connections |

The current version is **LCD-free**. Python and the Excel dashboard are the main data display. The LCD may be reintroduced in a later hardware revision.

## Software and libraries

- Arduino IDE
- Arduino C/C++
- Python 3
- VS Code (used during development)
- Python packages: `pyserial`, `openpyxl`
- Arduino libraries: `Keypad` and `DHT sensor library` (plus any dependency requested by the DHT library)
- Microsoft Excel or a compatible spreadsheet application
- Git and GitHub

## Repository structure

```text
Info-Excel_dashboard/
├── arduino/
│   ├── Smart_Security_System.ino
│   └── README.md
├── python/
│   ├── arduino_python.py
│   └── update_dashboard.py
├── data/
│   └── arduino_data.csv
├── dashboard/
│   ├── Smart_Security_Auto_Dashboard.xlsx
│   └── README.md
├── docs/
│   ├── pinout.md
│   ├── software_setup.md
│   └── project_walkthrough.md
├── images/
│   ├── hardware_setup.jpg
│   ├── hardware_closeup.jpg
│   ├── python_terminal.png
│   ├── python_code.png
│   ├── data_records.png
│   ├── excel_dashboard.png
│   └── README.md
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Setup

### 1. Install Python requirements

From the repository root:

```bash
python -m pip install -r requirements.txt
```

### 2. Set up the Arduino

1. Install the `Keypad` and `DHT` Arduino libraries in Arduino IDE.
2. Open `arduino/Smart_Security_System.ino`.
3. Confirm the pin map in [docs/pinout.md](docs/pinout.md).
4. Select the correct Arduino Uno board and COM port, then upload the code.

### 3. Run the logger

Close Arduino IDE's Serial Monitor first, because only one program can normally use the Arduino serial port at a time. Then run:

```bash
python python/arduino_python.py
```

Enter the PIN on the physical keypad. Accepted access should produce `ACCESS_GRANTED`; a wrong PIN should produce `ACCESS_DENIED`. A successful access produces sensor messages that Python combines into one CSV record.

### 4. Check the output

- Raw records: `data/arduino_data.csv`
- Dashboard workbook: `dashboard/Smart_Security_Auto_Dashboard.xlsx`

The logger runs `python/update_dashboard.py` after each saved record. The updater reads the CSV and rebuilds the workbook and charts.

## Data format

The CSV columns are:

```text
Date,Time,Access,Temperature_C,Humidity_percent,Distance_cm
```

A denied attempt is saved without sensor readings. A successful attempt is saved after Python receives temperature, humidity and distance values. If the ultrasonic sensor has no valid reading, distance is recorded as `ERROR`.

## Current test snapshot

The committed sample data currently contains **22 records: 17 granted and 5 denied**. The last sample in that data file is 27.3 °C, 48.3% humidity and 7.8 cm. These numbers describe the saved sample data, not a live dashboard.

## Known limitation

The keypad currently uses Arduino pins D0 and D1 for two columns. On the Uno, D0 and D1 are also the hardware serial RX/TX pins used by Python. This overlap can cause unreliable keypad or Serial behavior. It is documented rather than hidden; a future hardware revision should move those keypad connections to unused pins and update the code together. Do not use the optional LCD pin map at the same time as those pins are assigned to another component.

## What I learned

- Reading physical sensors with Arduino
- Sending serial messages between a microcontroller and a computer
- Parsing messages and grouping sensor values in Python
- Logging structured records to CSV
- Managing project-relative file paths
- Creating Excel summaries and charts using `openpyxl`
- Keeping hardware code, Python scripts, data, documentation and evidence in separate folders
- Debugging issues where hardware behavior affects software data

## Possible next improvements

- Resolve the D0/D1 keypad and Serial overlap and retest the full setup.
- Add a clear access-event timestamp and error status for each sensor.
- Improve chart labels and dashboard layout.
- Add automated tests for message parsing and CSV logging.
- Add a short, publicly viewable demonstration video.
- Consider a database only if the project grows beyond the current CSV workflow.

## Project status

**Prototype:** the Arduino-to-Python-to-CSV-to-Excel workflow has been tested, and sample records are included. The walkthrough is linked externally from Google Drive. The photos and screenshots still need to be committed as binary files in `images/` before GitHub can display them as a repository gallery.
