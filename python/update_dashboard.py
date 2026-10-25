import csv
import os

from openpyxl import Workbook
from openpyxl.chart import LineChart, PieChart, Reference
from openpyxl.styles import Font, PatternFill

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "arduino_data.csv")
DASHBOARD_FILE = os.path.join(
    BASE_DIR,
    "dashboard",
    "Smart_Security_Auto_Dashboard.xlsx",
)


HEADERS = [
    "Date",
    "Time",
    "Access",
    "Temperature_C",
    "Humidity_percent",
    "Distance_cm",
]


def read_csv():
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def number(value):
    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_dashboard():
    rows = read_csv()

    os.makedirs(os.path.dirname(DASHBOARD_FILE), exist_ok=True)

    workbook = Workbook()
    data_sheet = workbook.active
    data_sheet.title = "Data"

    dashboard = workbook.create_sheet("Dashboard")
    charts_data = workbook.create_sheet("ChartsData")

    # ---------------- Data sheet ----------------
    data_sheet.append(HEADERS)

    for row in rows:
        data_sheet.append([
            row.get("Date", ""),
            row.get("Time", ""),
            row.get("Access", ""),
            number(row.get("Temperature_C")),
            number(row.get("Humidity_percent")),
            number(row.get("Distance_cm")),
        ])

    for cell in data_sheet[1]:
        cell.font = Font(bold=True)

    data_sheet.freeze_panes = "A2"
    data_sheet.auto_filter.ref = data_sheet.dimensions

    # ---------------- Summary values ----------------
    granted = sum(1 for row in rows if row.get("Access") == "GRANTED")
    denied = sum(1 for row in rows if row.get("Access") == "DENIED")

    latest_temperature = None
    latest_humidity = None
    latest_distance = None

    for row in reversed(rows):
        if latest_temperature is None:
            latest_temperature = number(row.get("Temperature_C"))
        if latest_humidity is None:
            latest_humidity = number(row.get("Humidity_percent"))
        if latest_distance is None:
            latest_distance = number(row.get("Distance_cm"))

        if (
            latest_temperature is not None
            and latest_humidity is not None
            and latest_distance is not None
        ):
            break

    # ---------------- Dashboard ----------------
    dashboard["A1"] = "Smart Security Monitoring Dashboard"
    dashboard["A1"].font = Font(size=18, bold=True)

    metrics = [
        ("A3", "Total Records", len(rows)),
        ("A4", "Access Granted", granted),
        ("A5", "Access Denied", denied),
        ("D3", "Latest Temperature (C)", latest_temperature),
        ("D4", "Latest Humidity (%)", latest_humidity),
        ("D5", "Latest Distance (cm)", latest_distance),
    ]

    for label_cell, label, value in metrics:
        dashboard[label_cell] = label
        dashboard[label_cell].font = Font(bold=True)
        value_cell = dashboard.cell(
            row=dashboard[label_cell].row,
            column=dashboard[label_cell].column + 1,
        )
        value_cell.value = value if value is not None else "-"

    # ---------------- Chart data ----------------
    charts_data.append(["Access", "Count"])
    charts_data.append(["GRANTED", granted])
    charts_data.append(["DENIED", denied])

    pie = PieChart()
    pie.title = "Access Results"
    pie_labels = Reference(charts_data, min_col=1, min_row=2, max_row=3)
    pie_values = Reference(charts_data, min_col=2, min_row=1, max_row=3)
    pie.add_data(pie_values, titles_from_data=True)
    pie.set_categories(pie_labels)
    dashboard.add_chart(pie, "A8")

    # Sensor chart data starts in column D.
    charts_data["D1"] = "Record"
    charts_data["E1"] = "Temperature (C)"
    charts_data["F1"] = "Humidity (%)"
    charts_data["G1"] = "Distance (cm)"

    for index, row in enumerate(rows, start=2):
        charts_data.cell(index, 4).value = index - 1
        charts_data.cell(index, 5).value = number(row.get("Temperature_C"))
        charts_data.cell(index, 6).value = number(row.get("Humidity_percent"))
        charts_data.cell(index, 7).value = number(row.get("Distance_cm"))

    if rows:
        line = LineChart()
        line.title = "Sensor Readings"
        line.y_axis.title = "Value"
        line.x_axis.title = "Record"

        data = Reference(charts_data, min_col=5, max_col=7, min_row=1, max_row=len(rows) + 1)
        categories = Reference(charts_data, min_col=4, min_row=2, max_row=len(rows) + 1)
        line.add_data(data, titles_from_data=True)
        line.set_categories(categories)
        dashboard.add_chart(line, "J8")

    # Keep helper sheet available for the charts but hide it from normal view.
    charts_data.sheet_state = "hidden"

    for sheet in (data_sheet, dashboard):
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))

            sheet.column_dimensions[column_letter].width = min(max_length + 2, 35)

    workbook.save(DASHBOARD_FILE)
    print(f"Dashboard saved to: {DASHBOARD_FILE}")


if __name__ == "__main__":
    build_dashboard()
