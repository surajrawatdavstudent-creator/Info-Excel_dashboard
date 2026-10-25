# Excel Dashboard

The workbook is generated from `data/arduino_data.csv` by `python/update_dashboard.py`.

Expected workbook path:

```text
dashboard/Smart_Security_Auto_Dashboard.xlsx
```

The updater builds these sheets:

- `Data` — saved records
- `Dashboard` — totals, latest sensor readings and charts
- `ChartsData` — hidden chart-source data

The logger calls the updater after saving a new record. Running the updater manually from the repository root is also supported:

```bash
python python/update_dashboard.py
```

The workbook is an output file and can be regenerated from the CSV. Keep the CSV sample data in the repository so anyone can reproduce the dashboard without hardware.
