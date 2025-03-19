import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import shutil
import logging

def send_email(report_file, sender_email, sender_password, recipient_email):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = "TejzAutoMetrics Analysis Report"  
        msg.attach(MIMEText("Attached: Data report with key metrics", "plain"))  

        with open(report_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(report_file)}")
            msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        logging.info(f"Email sent with {report_file}")
    except Exception as e:
        logging.error(f"Email error: {e}")

def save_to_shared_folder(report_file, folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        dest = os.path.join(folder, os.path.basename(report_file))
        shutil.copy(report_file, dest)
        logging.info(f"Report saved to shared folder: {dest}")
    except Exception as e:
        logging.error(f"Shared folder error: {e}")