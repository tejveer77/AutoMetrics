import pandas as pd
import sqlite3
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def analyze_data(file_path):
    try:
        #Data loading is done here.
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".txt"):
            df = pd.read_csv(file_path, delimiter="|", names=["timestamp", "metric", "value"])
        else:
            logging.error("Unsupported format (.xlsx, .csv, .txt only).")
            return None, None

        logging.info(f"Data loaded: {df.shape[0]} rows, columns: {list(df.columns)}")
        logging.info(f"Data preview:\n{df.head().to_string()}")

        #For Data Summart and key metrics
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "unique_counts": df.nunique().to_dict(),
            "numeric_stats": {},
            "key_metrics": {}
        }

        #For Stats
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary["numeric_stats"] = {
                "means": df[numeric_cols].mean().to_dict(),
                "maxes": df[numeric_cols].max().to_dict(),
                "mins": df[numeric_cols].min().to_dict()
            }

        # Key metrics
        for col in df.columns:
            if df[col].dtype in [np.number, "float64", "int64"]:
                top_value = df[col].max()
                summary["key_metrics"][col] = f"Top value: {top_value}"
            else:
                most_frequent = df[col].mode()[0] if not df[col].mode().empty else "N/A"
                summary["key_metrics"][col] = f"Most frequent: {most_frequent}"

        logging.info(f"Analysis complete: {summary}")
        return df, summary
    except Exception as e:
        logging.error(f"Error occurred during data analysis: {str(e)}")
        return None, None

def store_data(df, db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table 
    try:
        df.to_sql(table_name, conn, if_exists="fail", index=False)
    except ValueError:  
        # Get existing columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_cols = [col[1] for col in cursor.fetchall()]
        new_cols = [col for col in df.columns if col not in existing_cols]
        
        # Add new columns
        for col in new_cols:
            col_type = "TEXT" if df[col].dtype == object else "REAL"
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}")
    
    # Append data
    df.to_sql(table_name, conn, if_exists="append", index=False)
    conn.close()
    logging.info(f"Data stored in {db_name}.{table_name}")