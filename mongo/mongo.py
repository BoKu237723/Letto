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

def clean_data(raw_data): # Return Cleaned Data (List) / Invalid Data (Int)
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

    print("[+] Total Events in Database\n")

    for event in event_names:
        print(f"[{event_names.index(event)}] {event}")

    return event_names # List

def cleaned_emails_from_each_event(event_names): # Only pull out cleaned data, combine them and remove duplicates
    print("\n")
    db = client["Letto"]
    collection = db["Past-Cleaned"]

    total_mails = []

    data = collection.find({}, {"_id": 0})

    try:
        for data in collection.find({}, {"_id": 0}):
            for event in event_names:
                if event in data:
                    mails = data[event]["cleaned_mails"]
                    total_mails.extend(mails)
    except Exception as e:
        print(f"Error: {e}")

    print(f"Total Mails: {len(total_mails)}")

    total_mails = unique_mails(total_mails)
    print(f"Total Mails (Removed Dups): {len(total_mails)}")

    return total_mails # This is a List

def process_data(numbers, total_events):

    rdy_to_process = [] # 1 2 3 4 5
    if "*" in numbers:
        for i in range(total_events):
            rdy_to_process.extend(i)
    else:
        rdy_to_process = numbers

    # Index to event name
    events_to_process = [] # Sample: ["Event-0", "Event-2", "Event-3", "Event-5"]
    
    for i in rdy_to_process:
        events_to_process.append(total_events[i])

    final_data = cleaned_emails_from_each_event(events_to_process)

    # Current Problem: The format we want is 
    # This won't work because there are dups

    db = client["Letto"]
    collection = db["Processed-Chunks"]

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    unique_name = input("[+] Enter Unique Name: ")
    description = input("[+] Enter Description: ")

    data = {
        "Name": unique_name,
        "Description": description,
        "Processed Events": total_events,
        "Created Date": time,
        "Mails": final_data
    }

    collection.insert_one(data)
    print("Data Inserted Successfully to Processed Chunks.")

def create_data_chunk(): # Only cleaned data

    def help_fun(): # Maybe add more in the future?
        print("\n[+] These are Sample Formats\n[+] Index starts at 0\n[+] (All Events except 8 and 10) 0-7 9 11-12\n[+] (All Events) * || 0-12 || 0 1 2 3 4 5 6 7 8 9 10 11 12")

    total_events = show_cleaned_events() # Returns List

    while True:
        try:
            user_range = input("\n[=] Select Your Range (? for help): ").strip() # String
            numbers = []

            if user_range == "?":
                help_fun()
                continue

            elif user_range == "*":
                numbers.extend("*")
                process_data(numbers)
                break

            else:
                for i in user_range.split(" "):
                    if "-" in i:
                        start, end = map(int, i.split("-"))
                        numbers.extend(range(start, end + 1))
                    else:
                        numbers.append(int(i))

                    greater_check = any(x > (len(total_events)-1) for x in numbers)

                if greater_check == True:
                    print(f"Only {len(total_events) - 1} exists.")
                    continue

                process_data(numbers, total_events)
                break

        except Exception as e:
            print(f"Input Error: {e}")

    print("")

def show_all_data_chunks():
    db = client["Letto"]
    collection = db["Processed-Chunks"]
    projection = { "Name": 1, "Description": 1, "_id": 0 }

    cursor = collection.find({}, projection)
    index = 0
    try:
        for doc in cursor:
            print(f"{index}: {doc["Name"]} : {doc["Description"]}")
            index += 1
    except Exception as e:
        print(f"Error: {e}")

def file_output():
    db = client["Letto"]
    collection = db["Processed-Chunks"]
    cursor = collection.find()
    selected_chunk = int(input("Enter ID of chunk to process: "))
    file_name = input("Enter file name: ")
    amount = int(input("How many mails per line?: "))

    for index, doc in enumerate(cursor):
        if index == selected_chunk:
            total_lines = 0

            with open (file_name, "w", encoding="utf-8") as f:
                for i in range(0, len(doc["Mails"]), amount):
                    chunk = doc["Mails"][i:i+amount]
                    
                    line = ' '.join(chunk)
                    f.write(line + '\n')
                    total_lines += 1

            print(f"Exported {total_lines} line/s in {file_name}.")
            break

    print("Chunk ID not found!")
    
def main():
    print("1. Process new event data \n2. Show current Events' data from Database")
    print("3. Show Specific Event Data \n4. Show all data chunks \n5. Make new data chunk\n6. File Output")

    while True:
        try:
            user_input = int(input("Your Input: "))
            if user_input == 1:
                file_processing()
            elif user_input == 2: # TODO
                pass
            elif user_input == 3: # TODO
                pass
            elif user_input == 4:
                show_all_data_chunks()
                continue
            elif user_input == 5:
                create_data_chunk()
                continue
            elif user_input == 6: # TODO
                show_all_data_chunks()
                file_output()
                continue
            else:
                print("Invalid input.")
                continue

            break
        except ValueError:
            print("Enter only integers.")
            continue
    client.close()

if __name__ == "__main__":
    main()