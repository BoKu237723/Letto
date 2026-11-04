import re

ALLOWED_DOMAINS = {
    '@gmail.com',
    '@outlook.com',
    '@hotmail.com',
    '@proton.me',
    '@icloud.com',
    '@yahoo.com'
}

def unique_mails(raw_data):

    unique_emails = list(dict.fromkeys(raw_data))

    print(f"[=]   Unique Mails (Final): {len(unique_emails)}")
    print(f"[=]   Duplicate Mails (Removed): {len(raw_data) - len(unique_emails)}\n")
    
    return unique_emails

def valid_email(raw_data):

    valid_mails = []

    pattern = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    )
    
    for mail in raw_data:
        mail = mail.strip().lower()
    
        if not pattern.fullmatch(mail):
            continue
    
        if '..' in mail or mail.startswith('.') or '@.' in mail:
            continue
    
        if not any(mail.endswith(domain) for domain in ALLOWED_DOMAINS):
            continue
    
        valid_mails.append(mail)
    
    valid_mails = list(dict.fromkeys(valid_mails))

    print(f"[=]   Valid Mails (Final): {len(valid_mails)}")
    print(f"[=]   Invalid Mails (Removed): {len(raw_data) - len(valid_mails)}\n")    

    return valid_mails

def main():
    pass

if __name__ == "__main__":
    main()