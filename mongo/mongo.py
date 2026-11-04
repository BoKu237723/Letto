from pymongo import MongoClient
import pandas as pd
import os

# from pandas import DataFrame
from datetime import datetime
from clean import unique_mails, valid_email

from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("ATLAS_URI")

client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

def clean_data(raw_data): # Return Cleaned Data / Invalid Data
    c_valid_mails = valid_email(raw_data)
    c_unique_mails = unique_mails(c_valid_mails) # This is final

    # print(f"[=]   Final Mails: {len(c_unique_mails)}")
    removed_mails = len(raw_data) - len(c_unique_mails)
    
    return c_unique_mails, removed_mails # List / int

def save_to_past_raw(event_name, raw_data):
    db = client["Letto"]
    collection = db["Past-Raw"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        event_name: {
            "time": time,
            "mails": raw_data
        }
    }

    collection.insert_one(data)
    print("Data Inserted Successfully.")

def save_to_past_cleaned(event_name, raw_data):
    db = client["Letto"]
    collection = db["Past-Cleaned"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cleaned_data, invalid_data = clean_data(raw_data)
    # print(len(cleaned_data), invalid_data)

    data = {
        event_name: {
            "time": time,
            "invalid_mails": invalid_data,
            "cleaned_mails": cleaned_data
        }
    }

    collection.insert_one(data)
    print("Data Inserted Successfully.")

def file_processing():
    event_name = input("Put your event name: ")
    file_name = input("Put your file name: ")
    mail_index = int(input("Enter column index for mails (0 for first column): "))

    try:
        read_data = pd.read_excel(file_name)
        raw_data = read_data.iloc[:, mail_index].tolist()
        save_to_past_raw(event_name, raw_data)
        save_to_past_cleaned(event_name, raw_data)

    except Exception as e:
        print(e)

def show_cleaned_events():
    db = client["Letto"]
    collection = db["Past-Cleaned"]

    events = collection.find({}, {"_id": 0})
    event_names = []
    for event in events:
        event_names.extend(event.keys())

    print(event_names)

def current_data(): # Only cleaned data
    print("[+] Current Available Events")

    user_range = input("[=] Select Your Range: ") # String

# file_processing()
show_cleaned_events()
client.close()