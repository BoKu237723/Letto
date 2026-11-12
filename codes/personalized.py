from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import smtplib
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)

from dotenv import load_dotenv
load_dotenv()

def colored(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def personalized_mails():
    print("")
    print(colored("[#] Make sure to enter certificates in the 'personalized/certificates' folder inside", Fore.CYAN + Style.DIM))
    print(colored("[#] Make sure to fill up and match data in personalized/emails.json", Fore.CYAN + Style.DIM))

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    YOUR_EMAIL = os.getenv("MYEMAIL")
    YOUR_APP_PASS = os.getenv("MYPASSWORD")

    CERTIFICATES_FOLDER = "personalized/certificates"
    EMAILS_JSON = "personalized/emails.json"

    EMAIL_SUBJECT = "Your Certificate is Here!"

    #TODO: Change This Part!!!
    EMAIL_BODY = r"""Dear Participant,

I hope this message finds you well.
Please find attached your certificate, which recognizes your "achievement, e.g., successful completion of the recent training program" with our organization. 
We hope you will proudly display this certificate as a testament to your hard work and dedication. Congratulations on your accomplishment!

Best regards,
"Your Organization Name"
"Your Contact Information"
"""

    try:
        with open(EMAILS_JSON, 'r') as f:
            email_data = json.load(f)
    except FileNotFoundError:
        print(colored(f"[!] Error: {EMAILS_JSON} file not found!", Fore.YELLOW))
        return
    except json.JSONDecodeError:
        print(colored(f"[!] Error: {EMAILS_JSON} contains invalid JSON!", Fore.YELLOW))
        return

    # MAIL SMTP SERVER CONNECTION
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_APP_PASS)
        print("")
        print(colored("[$] Successfully connected to Gmail SMTP server", Fore.GREEN))
    except Exception as e:
        print(colored(f"[$] Failed to connect to Gmail: {e}\n", Fore.RED))
        return

    successful_emails = 0
    failed_emails = 0

    for entry in email_data:
        recipient_email = entry.get('email')
        file_name = entry.get('file')

        if not recipient_email or not file_name:
            print(colored(f"[!] Skipping Invalid Entry: {entry}", Fore.YELLOW))
            failed_emails += 1
            continue

        file_path = os.path.join(CERTIFICATES_FOLDER, file_name)

        if not os.path.exists(file_path):
            print(colored(f"[!] Certificate Path not found: {file_path}", Fore.RED))
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
            print(colored(f"[$] Sent certificate to: {recipient_email} ({file_name})", Fore.GREEN))
            successful_emails += 1

        except Exception as e:
            print(colored(f"[!] Failed to send to {recipient_email}.", Fore.RED))
            failed_emails += 1

    server.quit()

    print("")
    print(colored(f"[$] Successful sent emails: {successful_emails}", Fore.GREEN))
    print(colored(f"[$] Failed to send emails : {failed_emails}", Fore.YELLOW))
    print(colored(f"[#] Total processed emails: {successful_emails + failed_emails}", Fore.CYAN + Style.DIM))
