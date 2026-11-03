from colorama import Fore, init
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import smtplib
import json
import os

from dotenv import load_dotenv
load_dotenv()

def personalized_mails():
    print(Fore.CYAN + "[=]   Make sure to enter certificates in the 'certificate' folder")
    print(Fore.CYAN + "[=]   Make sure to fill up and match data in emails.json")

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    YOUR_EMAIL = os.getenv("MYEMAIL")
    YOUR_APP_PASS = os.getenv("MYPASSWORD")

    CERTIFICATES_FOLDER = "certificates"
    EMAILS_JSON = "emails.json"

    EMAIL_SUBJECT = "Your Certificate is Here!"
    EMAIL_BODY = r"""Dear Participant,

I hope this message finds you well.
Please find attached your certificate, which recognizes your "achievement, e.g., successful completion of the recent training program" with our organization. 
We hope you will proudly display this certificate as a testament to your hard work and dedication. Congratulations on your accomplishment!
Best regards,
"Test"
"Testing"
"Your Organization Name"
"Your Contact Information"
"""

    try:
        with open(EMAILS_JSON, 'r') as f:
            email_data = json.load(f)
    except FileNotFoundError:
        print(Fore.RED + f"[-]   Error: {EMAILS_JSON} file not found!")
        return
    except json.JSONDecodeError:
        print(Fore.RED + f"[-]   Error: {EMAILS_JSON} contains invalid JSON!")
        return

    # MAIL SMTP SERVER CONNECTION
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_APP_PASS)
        print(Fore.CYAN + "[=]   Successfully connected to Gmail SMTP server")
    except Exception as e:
        print(Fore.RED + f"[-]   Failed to connect to Gmail: {e}\n")
        return

    successful_emails = 0
    failed_emails = 0

    for entry in email_data:
        recipient_email = entry.get('email')
        file_name = entry.get('file')

        if not recipient_email or not file_name:
            print(Fore.RED + f"[-]   Skipping Invalid Entry: {entry} ")
            failed_emails += 1
            continue

        file_path = os.path.join(CERTIFICATES_FOLDER, file_name)

        if not os.path.exists(file_path):
            print(Fore.RED + f"[-]   Certificate Path not found: {file_path}")
            failed_emails += 1
            continue

        try:
            msg = MIMEMultipart()
            msg['From'] = YOUR_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = EMAIL_SUBJECT

            # email body
            msg.attach(MIMEText(EMAIL_BODY, 'plain'))

            # certificate file
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_name}'
            )
            msg.attach(part)

            # Send
            server.send_message(msg)
            print(f"[+]   Sent certificate to: {recipient_email} ({file_name})")
            successful_emails += 1

        except Exception as e:
            print(Fore.RED + f"[-]   Failed to send to {recipient_email}.")
            failed_emails += 1

    server.quit()
    print(Fore.CYAN + f"\n[=]   Successful sent emails: {successful_emails}")
    print(Fore.CYAN + f"[=]   Failed to send emails : {failed_emails}")
    print(Fore.CYAN + f"[=]   Total processed emails: {successful_emails + failed_emails}\n")
