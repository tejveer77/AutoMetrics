import tkinter as tk
from ui import TejzAutometricsUI
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    
    root = tk.Tk()
    app = TejzAutometricsUI(root, config)
    root.mainloop()