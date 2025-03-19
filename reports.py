import pandas as pd
from fpdf import FPDF
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_excel_report(df, summary, report_file):
    try:
        if df is None or df.empty:
            df = pd.DataFrame({"Status": ["No data loaded"]})
        df_out = df.copy()
        df_out["Summary"] = f"Rows: {summary['rows']}, Columns: {summary['columns']}"
        df_out["Key_Metrics"] = "; ".join([f"{k}: {v}" for k, v in summary["key_metrics"].items()])
        df_out.to_excel(report_file, index=False)
        logging.info(f"Excel report saved: {report_file}")
        return report_file
    except Exception as e:
        logging.error(f"Excel report error: {e}")
        return None

def generate_pdf_report(df, summary, report_file):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=8)

        
        pdf.cell(200, 10, txt="TejzAutoMetrics Report", ln=True, align="C")

        # Summary
        pdf.cell(200, 10, txt="Data Summary", ln=True)
        pdf.multi_cell(0, 10, txt=f"Rows: {summary['rows']}\nColumns: {summary['columns']}\nColumn Names: {', '.join(summary['column_names'])}")

        # Stats
        pdf.cell(200, 10, txt="Numeric Stats", ln=True)
        if not summary["numeric_stats"]:
            pdf.multi_cell(0, 10, txt="No numeric columns found")
        else:
            for stat, values in summary["numeric_stats"].items():
                pdf.multi_cell(0, 10, txt=f"{stat.capitalize()}: {values}")

        # Key Metrics
        pdf.cell(200, 10, txt="Key Metrics", ln=True)
        for col, metric in summary["key_metrics"].items():
            pdf.multi_cell(0, 10, txt=f"- {col}: {metric}")

        # Full Data
        pdf.cell(200, 10, txt="Full Data", ln=True)
        if df is None or df.empty:
            pdf.multi_cell(0, 10, txt="No data available")
        else:
            col_widths = [max(pdf.get_string_width(str(col)) + 4, 20) for col in df.columns]
            total_width = sum(col_widths)
            if total_width > 190:
                scale = 190 / total_width
                col_widths = [w * scale for w in col_widths]

            for col, width in zip(df.columns, col_widths):
                pdf.cell(width, 8, txt=col, border=1)
            pdf.ln()
            for _, row in df.iterrows():
                if pdf.get_y() > 260:
                    pdf.add_page()
                for col, width in zip(df.columns, col_widths):
                    pdf.cell(width, 8, txt=str(row[col])[:20], border=1)
                pdf.ln()

        pdf.output(report_file)
        logging.info(f"PDF report saved: {report_file}")
        return report_file
    except Exception as e:
        logging.error(f"PDF report error: {e}")
        return None