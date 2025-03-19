# Tejz AutoMetrics 

## Overview
Tejz AutoMetrics is a Python automation tool for IT systems—processes Excel/CSV/TXT files, calculates key metrics (e.g., totals, averages), stores data in SQLite, and generates Excel/PDF reports. Reports are emailed with "TejzAutoMetrics Analysis Report" and "Attached: Data report with key metrics."

## Features
- **Dynamic Schema**: Adapts SQLite to any dataset.
- **Metrics**: Numeric stats and key insights.
- **Reports**: Excel and PDF outputs.
- **Integration**: SMTP email and folder save.
- **GUI**: Tkinter interface.

## Requirements
- Python 3.x
- Dependencies: `pandas`, `numpy`, `sqlite3`, `fpdf`, `tkinter` , `logging` , `os` , `shutil`

## Installation
1. Unzip `Tejz_AutoMetrics`.
2. Install dependencies:
   ```bash
   pip install pandas numpy fpdf logging
3. In config.json , please write your credintials (sender email , App passwords of gmail and reciever email)

# To get app passwords for gmail , please open your gmail account , select profile and manage account , search for app passwords and generate one password.

4. After installation, run script in bash
   python main.py
5. Graphical Interface will open , select excel file that is provided in dataset folder or any other excel file
6. Click on Analyze Data
7. In terminal , you can see email sent you can view reports in your email now.