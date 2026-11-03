from colorama import Fore, Back, Style, init
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import smtplib
import json
import time
import sys
import os

from dotenv import load_dotenv, dotenv_values
load_dotenv()

from personalized_files import personalized_mails

print ("""
[0;34m▄▄▄[0;34;47m▀▀▀[0;34m█[0;37m                [0;34m▄▄▄[0;34;47m▀▀▀[0;34m█[0;37m    [0;34m▄▄▄[0;34;47m▀▀▀[0;34m█[0;37m                 [0m
[0;37m [0;34m█[0;34;47m   [0;34m█[0;37m                  [0;34m█[0;34;47m   [0;34m█[0;37m      [0;34m█[0;34;47m   [0;34m█[0;37m                  [0m
[0;37m [0;34m█[0;34;47m ░ [0;34m█[0;37m    [0;34m▄[0;34;47m▀▀[0;37;44m█▀▀█[0;34;47m▀[0;37;44m▄[0;34m▄[0;37m    [0;34m█[0;34;47m ░ [0;34m█▄[0;37;44m▄[0;34m▄[0;37m   [0;34m█[0;34;47m ░ [0;34m█▄[0;37;44m▄[0;34m▄[0;37m    [0;30;44m▀[0;37;44m▄▄▄▄▄▄▄[0;30;44m▀[0;37m  [0m
[0;37m [0;34m█[0;34;47m░▒░[0;34m█[0;37m   [0;34m█[0;34;47m ░[0;37;44m▒[0;34m█[0;37m  [0;37;44m▒█▓█[0;35;44m░[0;37m   [0;34m█[0;34;47m░▒░[0;37;44m▀▓█▀[0;34m▀[0;37m  [0;34m█[0;34;47m░▒░[0;37;44m▀▓█▀[0;34m▀[0;37m  [0;34m█[0;37;44m█▓█[0;34m█▀█[0;37;44m█▓█[0;34m█[0;37m [0m
[0;37m [0;34m█[0;34;47m▒▓▒[0;34m█[0;37m  [0;34m█[0;34;47m▒░▒[0;37;44m░[0;37m   [0;37;44m░▓▀▀[0;34m▀[0;37m   [0;34m█[0;34;47m▒▓▒[0;34m██[0;37;44m░[0;34m█[0;37m   [0;34m█[0;34;47m▒▓▒[0;34m██[0;37;44m░[0;34m█[0;37m  [0;34m█[0;37;44m▓▒▓ [0;37m   [0;37;44m ▓▒▓[0;34m█[0m
[0;37m [0;34m█[0;34;47m▓█▓[0;35;44m░[0;37m  [0;34m█[0;34;47m▒▓▒[0;34m█▀■▀▀▀[0;37m      [0;34m█[0;34;47m▓█▓[0;35;44m░[0;34m▒▀[0;37m    [0;34m█[0;34;47m▓█▓[0;35;44m░[0;34m▒▀[0;37m   [0;34m█[0;37;44m▒░▒[0;34m▓[0;37m   [0;34m▓[0;37;44m▒░▒[0;34m█[0m
[0;37m [0;34m█[0;34;44m [0;94;44m░ [0;35;44m▒[0;37m  [0;34m█[0;34;47m▓█▓[0;35;44m░[0;37m    [0;34m▄▄■▄[0;37m   [0;34m█[0;34;44m [0;94;44m░ [0;35;44m▒[0;34m░[0;37m     [0;34m█[0;34;44m [0;94;44m░ [0;35;44m▒[0;34m░[0;37m    [0;34m█[0;37;44m░ ░[0;34m▓[0;37m   [0;34m▓[0;37;44m░ ░[0;34m█[0m
[0;37m [0;34m█[0;94;44m░▒░[0;35;44m▓[0;37m   [0;34m█[0;34;44m [0;94;44m░[0;35;44m▒[0;34m▄[0;37m [0;34m▄[0;94;44m▒░░▒[0;35;44m▓[0;35m▌[0;37m  [0;34m█[0;94;44m░▒░[0;35;44m▓[0;34m▓[0;35;44m▄■▄[0;37m  [0;34m█[0;94;44m░▒░[0;35;44m▓[0;34m▓[0;35;44m▄■▄[0;37m  [0;34m█[0;34;44m [0;94;44m░▒ [0;34m▄[0;94;44m ▒░[0;34;44m [0;34m█[0;37m [0m
[0;37m [0;34m█[0;34;45m▀▀▀ [0;37m     [0;35m▀[0;35;44m▄▄▄▄[0;35m▀▀▀▀[0;37m    [0;35;44m■[0;34;45m▀▀▀[0;35;44m▄▀[0;34m▀▀▀[0;37m  [0;35;44m■[0;34;45m▀▀▀[0;35;44m▄▀[0;34m▀▀▀[0;37m   [0;35m▀[0;35;44m▄▄▄[0;35m■[0;35;44m▄▄▄[0;35m▀[0;37m  [0m           Developed by BoKu~
[0;34m▀▀[0;37m                     [0;34m▀▀[0;37m         [0;34m▀▀[0;37m                      [0m
""")

ALLOWED_DOMAINS = {
    '@gmail.com',
    '@outlook.com',
    '@hotmail.com',
    '@proton.me',
    '@icloud.com',
    '@yahoo.com'
}

total_mails = []
unique_mails = []
valid_mails = []

def show_options():
    print(Fore.BLUE + "\n[01]  Process emails\n[02]  Remove Duplicate emails\n[03]  Remove Invalid emails\n[04]  Remove both Duplicate and Invalid emails\n[05]  See total amount of processed mails\n[06]  Line up emails to send (chunks.txt)\n[07]  Personalized Email Sender Automation\n[08]  Show Options\n[09]  Help\n[10]  Exit\n")

def process_mails(email_files):
    for i in email_files:
        with open(i, "r", encoding="utf-8") as file:
            for line in file:
                total_mails.append(line.strip().lower())
    print(Fore.CYAN + f"[=]   Processed Mails (uncleaned): {len(total_mails)}\n" + Style.RESET_ALL)

def unique_mails():
    try:
        global total_mails
        if not total_mails:
            print(Fore.YELLOW + "[-]   Emails not found. Enter emails with [01] to process first.\n")
        else:
            unique_emails = list(dict.fromkeys(total_mails))
            print(Fore.CYAN + f"[=]   Unique Mails (Final): {len(unique_emails)}")
            print(Fore.CYAN + f"[=]   Duplicate Mails (Removed): {len(total_mails) - len(unique_emails)}\n")
            total_mails = unique_emails

    except Exception as e:
        print(Fore.RED + f"[-]   Error: {e}")

    except KeyboardInterrupt:
        print(Fore.RED + "\n[-]   Keyboard Interrupt Detected. Quitting..." + Style.RESET_ALL)
        sys.exit()

def is_valid_email():
    global valid_mails, total_mails
    if not total_mails:
        print(Fore.YELLOW + "[-]   Emails not found. Enter emails with [01] to process first.\n")
    else:
        for domain in ALLOWED_DOMAINS:
            for mail in total_mails:
                if mail.endswith(domain):
                    local_part = mail[:-len(domain)]
                    if local_part and '@' not in local_part and ' ' not in local_part:
                        valid_mails.append(mail)

        print(Fore.CYAN + f"[=]   Valid Mails (Final): {len(valid_mails)}")
        print(Fore.CYAN + f"[=]   Invalid Mails (Removed): {len(total_mails) - len(valid_mails)}\n")    

    total_mails = valid_mails
    valid_mails = []

def email_chunking(amount):
    # Let's send 300bcc per mail
    with open('chunks.txt', 'w', encoding='utf-8') as f:
        total_lines = 0
        for i in range(0, len(total_mails), amount):
            chunk = total_mails[i:i+amount]
            # Join with space (for email sending)
            line = ' '.join(chunk)
            f.write(line + '\n')
            total_lines += 1

    print(Fore.CYAN + f"[=]   Amount of Lines: {total_lines}")
    print(Fore.CYAN + f"[=]   The Data is Generated in 'chunks.txt' \n")

def help_function():
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*70)
    print(" " * 22 + "HELP & DOCUMENTATION")
    print("="*70 + Style.RESET_ALL)

    print(Fore.YELLOW + "\n[!] How to input commands:" + Style.RESET_ALL)
    print("    Type the 2-digit option number at the start of your input.")
    print("    Example: " + Fore.GREEN + "01 emails.txt" + Style.RESET_ALL)

    # ----- 01 -----
    print(Fore.CYAN + "\n[01] Process Emails" + Style.RESET_ALL)
    print("     Loads emails from one or more .txt files (one email per line).")
    print("     All emails are combined into a single list for later use.")
    print("     " + Fore.YELLOW + "Usage:" + Style.RESET_ALL +
          " 01 file1.txt, file2.txt, file3.txt")
    print("     " + Fore.YELLOW + "Note:" + Style.RESET_ALL +
          " Separate multiple files with a comma + space (', ').")
    print("     " + Fore.YELLOW + "Required before:" + Style.RESET_ALL +
          " 02, 03, 04, 05")

    # ----- 02 -----
    print(Fore.CYAN + "\n[02] Remove Duplicate Emails" + Style.RESET_ALL)
    print("     Removes duplicate entries from the processed list.")
    print("     " + Fore.YELLOW + "Requires:" + Style.RESET_ALL + " 01 to be run first.")

    # ----- 03 -----
    print(Fore.CYAN + "\n[03] Remove Invalid Emails" + Style.RESET_ALL)
    print("     Filters out emails whose domains are not in the allowed list.")
    print("     " + Fore.YELLOW + "Allowed domains:" + Style.RESET_ALL)
    for domain in sorted(ALLOWED_DOMAINS):
        print(f"       - {domain}")
    print("     " + Fore.YELLOW + "Requires:" + Style.RESET_ALL + " 01 to be run first.")

    # ----- 04 -----
    print(Fore.CYAN + "\n[04] Remove Duplicates + Invalid Emails" + Style.RESET_ALL)
    print("     Combines options 02 and 03 in a single step.")
    print("     " + Fore.YELLOW + "Requires:" + Style.RESET_ALL + " 01 to be run first.")

    # ----- 05 -----
    print(Fore.CYAN + "\n[05] See total amount of processed mails" + Style.RESET_ALL)
    print("     See current total amount of processed emails.")


    # ----- 06 -----
    print(Fore.CYAN + "\n[06] Line Up Emails (Chunking)" + Style.RESET_ALL)
    print("     Groups emails into space-separated chunks for BCC sending.")
    print("     " + Fore.YELLOW + "Usage:" + Style.RESET_ALL +
          " 05 <amount>   (e.g. 05 300)")
    print("     " + Fore.YELLOW + "Output:" + Style.RESET_ALL +
          " Writes results to 'chunks.txt'.")
    print("     " + Fore.YELLOW + "Requires:" + Style.RESET_ALL + " 01 to be run first.")

    # ----- 07 -----
    print(Fore.CYAN + "\n[07] Personalized Email Sender" + Style.RESET_ALL)
    print("     Sends personalized emails with attachments (e.g. certificates).")
    print("     " + Fore.YELLOW + "Setup:" + Style.RESET_ALL)
    print("       1. Place attachment files in the 'certificates' folder.")
    print("       2. Edit 'emails.json' with entries like:")
    print(Fore.WHITE + '          { "email": "user@example.com", "file": "cert.pdf" }' + Style.RESET_ALL)
    print("       3. Set MYEMAIL and MYPASSWORD in your .env file.")
    print("     " + Fore.YELLOW + "Note:" + Style.RESET_ALL +
          " Does NOT require option 01. Can be used standalone.")

    # ----- 08 -----
    print(Fore.CYAN + "\n[08] Show Options" + Style.RESET_ALL)
    print("     Displays the main menu.")

    # ----- 09 -----
    print(Fore.CYAN + "\n[09] Help" + Style.RESET_ALL)
    print("     Displays this help documentation.")

    # ----- 10 -----
    print(Fore.CYAN + "\n[10] Exit" + Style.RESET_ALL)
    print("     Quits the program. (Ctrl+C also works.)")

    print(Fore.CYAN + "\n" + "="*70)
    print(" " * 18 + "(Letto) Developed by BoKu~")
    print("="*70 + "\n" + Style.RESET_ALL)

def main():
    show_options()
    while True:
        try:
            userInput = input(Fore.GREEN + "[+]   Your Input: ")
            if userInput[:2] == "01":
                try:
                    email_files = userInput[3:].split(", ")
                    process_mails(email_files)
                except FileNotFoundError:
                    print(Fore.YELLOW + f"[-]   Please enter correct file(s) to process. Use ', ' to seperate files. (eg. 01 list1.txt, list2.txt.)\n")
                except Exception as e:
                    print(Fore.RED + f"[-]   Error: {e}\n" + Style.RESET_ALL)
        
            elif userInput[:2] == "02":
                unique_mails()
        
            elif userInput[:2] == "03":
                is_valid_email()
        
            elif userInput[:2] == "04":
                if not total_mails:
                    print(Fore.YELLOW + "[-]   Emails not found. Enter emails with [01] to process first.\n")
                else:
                    unique_mails()
                    is_valid_email()

            elif userInput[:2] == "05":
                if not total_mails:
                    print(Fore.YELLOW + "[-]   Emails not found. Enter emails with [01] to process first.\n")
                else:
                    print(Fore.CYAN + f"[=]   Currently processing emails: {len(total_mails)}\n")
        
            elif userInput[:2] == "06":
                amount = userInput[2:].split(" ")
                try:
                    if not total_mails:
                        print(Fore.YELLOW + "[-]   Emails not found. Enter emails with [01] to process first.\n")
                    else:
                        email_chunking(int(amount[1]))
                except IndexError:
                    print(Fore.YELLOW + "[-]   Enter chunk size amount. eg. [06 300]\n")
                except Exception as e:
                    print(Fore.RED + f"[-]   Error: {e}\n" + Style.RESET_ALL)
                    
            elif userInput[:2] == "07":
                personalized_mails()
        
            elif userInput[:2] == "08":
                show_options()
                continue
    
            elif userInput[:2] == "09":
                help_function()
                continue
        
            elif userInput[:2] == "10":
                print("[=]   Existing..." + Style.RESET_ALL)
                break
        
            else:
                print(Fore.RED + "[-]   Invalid Input. Enter [06] to see options.\n")
                continue
    
        except KeyboardInterrupt:
            print(Fore.RED + "\n[-]   Keyboard Interrupt Detected. Quitting..." + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()