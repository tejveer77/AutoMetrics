import tkinter as tk
from tkinter import filedialog, ttk
import logging
from analyzer import analyze_data, store_data
from reports import generate_excel_report, generate_pdf_report
from integrator import send_email, save_to_shared_folder
import json

class TejzAutometricsUI:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Tejz Autometrics")
        self.config = config

        tk.Label(root, text="Tejz Autometrics ").pack(pady=10)
        tk.Button(root, text="Select File", command=self.select_file).pack(pady=5)
        
        self.notes = tk.Text(root, height=3, width=50)
        self.notes.pack(pady=5)
        self.notes.insert(tk.END, "Enter notes here...")

        self.progress = ttk.Progressbar(root, length=200, mode="determinate")
        self.progress.pack(pady=10)

        tk.Button(root, text="Analyze Data", command=self.run_analysis).pack(pady=5)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv"), ("Text", "*.txt")])
        if self.file_path:
            logging.info(f"Selected: {self.file_path}")

    def run_analysis(self):
        if not hasattr(self, "file_path"):
            logging.error("No file selected!")
            return

        self.progress["value"] = 0
        self.root.update()

        # Analyze data
        self.progress["value"] = 20
        df, summary = analyze_data(self.file_path)
        if df is None:
            return

        # Store
        self.progress["value"] = 40
        store_data(df, self.config["db_name"], self.config["table_name"])

        # Reports
        self.progress["value"] = 60
        excel_file = generate_excel_report(df, summary, self.config["report_file_excel"])
        pdf_file = generate_pdf_report(df, summary, self.config["report_file_pdf"])

        # Integrate
        self.progress["value"] = 80
        for report in [excel_file, pdf_file]:
            if report:
                send_email(report, self.config["sender_email"], self.config["sender_password"], self.config["recipient_email"])
                save_to_shared_folder(report, self.config["report_folder"])

        self.progress["value"] = 100
        logging.info("Analysis complete!")