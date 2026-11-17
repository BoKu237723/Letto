from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os
import re
from collections import Counter
from colorama import Fore, Style 
import questionary

from dotenv import load_dotenv
load_dotenv()

# ========================================================================================================

""" Support Functions """

def get_current_time():
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time

def colored(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

# ========================================================================================================

""" Atlas Connection """

uri = os.getenv("ATLAS_URI")
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("\nConnected successfully")
except Exception as e:
    print(f"Error Occured: {e}")

def mongo_collection(collection_name):
    db = client["Letto"]
    return db[collection_name]

# ========================================================================================================

""" Mail Cleaning (Invalids and Duplicates) """

ALLOWED_DOMAINS = {
    '@gmail.com',
    '@outlook.com',
    '@hotmail.com',
    '@proton.me',
    '@icloud.com',
    '@yahoo.com'
}

def f_unique_mails(raw_mails):
    unique_mails = list(dict.fromkeys(raw_mails))

    duplicates = [
        mail for mail, count in Counter(raw_mails).items()
        if count > 1
    ]

    return unique_mails, duplicates

def f_valid_mails(raw_mails):
    valid_mails = []
    invalid_mails = []
    pattern = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

    for mail in raw_mails:
        mail = mail.strip().lower()

        if not pattern.fullmatch(mail):
            invalid_mails.append(mail)
            continue
        if '..' in mail or mail.startswith('.') or '@.' in mail: # Invalid Inclusions
            invalid_mails.append(mail)
            continue
        if not any(mail.endswith(domain) for domain in ALLOWED_DOMAINS):
            invalid_mails.append(mail)
            continue

        valid_mails.append(mail)

    return valid_mails, invalid_mails

# ========================================================================================================

""" Add New Event ( Raw & Clean ) """

def clean_mails(raw_mails): # Return Valid & Invalid & Unique & Duplicate & Final mails as list # TODO
    valid_mails, invalid_mails = f_valid_mails(raw_mails)
    unique_mails, duplicates_mails = f_unique_mails(valid_mails)
    # Duplicate Mails are integers, not list.
    # Unique Mails are the final mails

    print(f"[$] Processed Raw Mails: {Fore.YELLOW + Style.BRIGHT}{len(raw_mails)}{Style.RESET_ALL}")
    print(f"[$] Valid Mails: {Fore.YELLOW + Style.BRIGHT}{len(valid_mails)}{Style.RESET_ALL}")
    print(f"[$] Invalid Mails: {Fore.YELLOW + Style.BRIGHT}{len(invalid_mails)}{Style.RESET_ALL}")
    print(f"[$] Unique Mails: {Fore.YELLOW + Style.BRIGHT}{len(unique_mails)}{Style.RESET_ALL}")
    print(f"[$] Duplicate Mails: {Fore.YELLOW + Style.BRIGHT}{len(duplicates_mails)}{Style.RESET_ALL}")
    print(f"[$] Final Cleaned Mails: {Fore.YELLOW + Style.BRIGHT}{len(unique_mails)}{Style.RESET_ALL}")

    return valid_mails, invalid_mails, unique_mails, duplicates_mails, unique_mails

def save_to_past_raw(event_name, mails):
    collection = mongo_collection("Past-Raw")
    time = get_current_time()

    data = {
        event_name: {
            "datetime": time,
            "mails": mails
        }
    }

    collection.insert_one(data)

def save_to_past_cleaned(event_name, raw_mails):
    collection = mongo_collection("Past-Cleaned")
    time = get_current_time()
    valid_mails, invalid_mails, unique_mails, duplicate_mails, final_mails = clean_mails(raw_mails)

    data = {
        event_name: {
            "datetime": time,                   # String
            "valid_mails": valid_mails,         # List
            "invalid_mails": invalid_mails,     # List
            "unique_mails": unique_mails,       # List
            "duplicate_mails": duplicate_mails, # List
            "final_mails": final_mails          # List
        }
    }

    try:
        collection.insert_one(data)
        print(f"[$] {Fore.GREEN + Style.BRIGHT}Raw data inserted successfully to (Past-Raw) collection {Style.RESET_ALL}")
        print(f"[$] {Fore.GREEN + Style.BRIGHT}Clean data inserted successfully to (Past-Cleaned) collection {Style.RESET_ALL}")
        print("")
    except Exception as e:
        print(f"Error: {e}")

def add_new_event():
    v_event_name = questionary.text("Enter your event name:").ask()
    v_file_name = questionary.text("Enter file (.xlsx) name to process:").ask()
    v_column = questionary.text("Enter column index for mails (0 for first column):").ask()
    v_column = int(v_column)

    try:
        v_read_data = pd.read_excel(v_file_name)
        v_extracted_mails = v_read_data.iloc[:, v_column].tolist()
        save_to_past_raw(v_event_name, v_extracted_mails)
        save_to_past_cleaned(v_event_name, v_extracted_mails)
    except Exception as e:
        print(f"Error Occured: {e}\n")


# ========================================================================================================

""" Display Data """

def pullout_event_names():

    # No return for "Show all events in database"
    # Return event_names list to find out how many events are there for certain functions

    collection = mongo_collection("Past-Cleaned")
    events = collection.find({}, {"_id": 0})
    event_names = []

    for event in events:
        event_names.extend(event.keys())

    for event in event_names:
        print(f"[{event_names.index(event)}] {event}")

    return event_names # List ["Event-1", "Event-2", "Evet-3"]

def display_events_detail():
    db = client["Letto"]
    collection = db["Past-Cleaned"]
    cursor = collection.find({})
    docs = list(cursor)
    
    input_range = pull_data() # List

    for event in input_range:
        doc = next(
            (
                doc for doc in docs
                if event in doc and event != "_id"
            ),
            None
        )

        event_name = event
        event_data = doc[event_name]

        created_time     =   event_data["datetime"]
        valid_mails      =   event_data["valid_mails"]
        invalid_mails    =   event_data["invalid_mails"]
        unique_mails     =   event_data["unique_mails"]
        duplicate_mails  =   event_data["duplicate_mails"]
        final_mails      =   event_data["final_mails"]

        print("")
        print(f"[$] Event Name: {Fore.YELLOW + Style.BRIGHT}{event_name}{Fore.RESET}")
        print(f"[$] Created Time: {Fore.YELLOW + Style.BRIGHT}{created_time}{Fore.RESET}")
        print(f"[$] Valid Mails: {Fore.YELLOW + Style.BRIGHT}{len(valid_mails)}{Fore.RESET}")
        print(f"[$] Invalid Mails: {Fore.YELLOW + Style.BRIGHT}{len(invalid_mails)}{Fore.RESET}")
        print(f"[$] Unique Mails: {Fore.YELLOW + Style.BRIGHT}{len(unique_mails)}{Fore.RESET}")
        print(f"[$] Duplicate Mails: {Fore.YELLOW + Style.BRIGHT}{len(duplicate_mails)}{Fore.RESET}")
        print(f"[$] Ready to Use Mails: {Fore.YELLOW + Style.BRIGHT}{len(final_mails)}{Fore.RESET}")

    print("")

# ========================================================================================================

# Return all event names | No Display

def return_all_event_names():
    collection = mongo_collection("Past-Cleaned")
    events = collection.find({}, {"_id": 0})
    event_names = []

    for event in events:
        event_names.extend(event.keys())

    return event_names

def pull_data():
    event_names = return_all_event_names() # List
    selected_events = []

    selected_events = questionary.checkbox(
        "Select toppings", event_names
    ).ask()
    return selected_events

# ========================================================================================================

""" Data Range """

def range_help():
    print("")
    print("[#] These are Sample Formats")
    print("[#] (All Events except 8 and 10) 0-7 9 11-12")
    print("[#] (All Events) * || 0-12 || 0 1 2 3 4 5 6 7 8 9 10 11 12")

# def data_range(): # Example: 0-4 6 8-9 11 # Output a list of index of chosen events
#     total_events = pullout_event_names()
#     while True:
#         numbers = []
#         user_range = input("\n(:) Select Your Range (? for help): ").strip() # String

#         if user_range == "?":
#             range_help()
#             continue

#         elif user_range == "*":
#             index = 0
#             for i in range(len(total_events)):
#                 numbers.append(index)
#                 index += 1
#             break

#         else:
#             for i in user_range.split(" "):
#                 if "-" in i:
#                     start, end = map(int, i.split("-"))
#                     numbers.extend(range(start, end+1))
#                 else:
#                     numbers.append(int(i))

#                 greater_check = any(x > (len(total_events)) for x in numbers)

#             if greater_check == True:
#                 print(f"Only {len(total_events)} exists.")
#                 continue
#             break

#     return numbers

# ========================================================================================================

""" Data Chunks ( Read & Create ) """

def create_chunk_mails(event_list):
    db = client["Letto"]
    collection = db["Past-Cleaned"]
    data = collection.find({}, {"_id": 0})

    total_mails = []

    try:
        for i in data:
            for event in event_list:
                if event in i:
                    mails = i[event]["final_mails"]
                    total_mails.extend(mails)

        final_mails, duplicates  = f_unique_mails(total_mails)

        return final_mails, duplicates

    except Exception as e:
        print(f"Error Occured: {e}")

def create_chunk():
    collection = mongo_collection("Processed-Chunks")
    chosen_events = pull_data() # List
    total_events = return_all_event_names()

    final_data, duplicates = create_chunk_mails(chosen_events)

    unique_name = questionary.text("Enter unique name for this chunk:").ask() # TODO: Need validation
    description = questionary.text("Enter description for this chunk:").ask()
    time = get_current_time()

    data = {
        "Unique Name": unique_name,
        "Description": description,
        "Created Date": time,
        "Included Events": chosen_events,
        "Cleaned Mails": final_data,
        "Duplicate Mails": duplicates
    }

    collection.insert_one(data)
    print("")
    print(f"[$] {Fore.GREEN + Style.BRIGHT}Successfully created the chunk and pushed to Atlas! {Style.RESET_ALL}")
    print(f"[$] Created Data Chunk Name: {Fore.YELLOW + Style.BRIGHT}{unique_name}{Style.RESET_ALL}")
    print(f"[$] Created Data Chunk Description: {Fore.YELLOW + Style.BRIGHT}{description}{Style.RESET_ALL}")
    print(f"[$] Created Time: {Fore.YELLOW + Style.BRIGHT}{time}{Style.RESET_ALL}")
    print(f"[$] Included Events: {Fore.YELLOW + Style.BRIGHT}{chosen_events}{Style.RESET_ALL}")
    print(f"[$] Duplicates Found: {Fore.YELLOW + Style.BRIGHT}{len(duplicates)}{Style.RESET_ALL}")
    print(f"[$] Cleaned Mails (Final): {Fore.YELLOW + Style.BRIGHT}{len(final_data)}{Style.RESET_ALL}")
    print("")

def show_chunks():
    collection = mongo_collection("Processed-Chunks")
    cursor = collection.find({})
    for index, doc in enumerate(cursor):
        print("")
        print(f"[$] Index: {Fore.YELLOW + Style.BRIGHT}{index}{Style.RESET_ALL}")
        print(f"[$] Unique Name: {Fore.YELLOW + Style.BRIGHT}{doc["Unique Name"]}{Style.RESET_ALL}")
        print(f"[$] Description: {Fore.YELLOW + Style.BRIGHT}{doc["Description"]}{Style.RESET_ALL}")
        print(f"[$] Created Data: {Fore.YELLOW + Style.BRIGHT}{doc["Created Date"]}{Style.RESET_ALL}")
        print(f"[$] Included Events: {Fore.YELLOW + Style.BRIGHT}{doc["Included Events"]}{Style.RESET_ALL}")
        print(f"[$] Cleaned Mails: {Fore.YELLOW + Style.BRIGHT}{len(doc["Cleaned Mails"])}{Style.RESET_ALL}")
        print(f"[$] Removed Duplicates: {Fore.YELLOW + Style.BRIGHT}{len(doc["Duplicate Mails"])}{Style.RESET_ALL}")

    print("")

def show_chunk_info():
    collection = mongo_collection("Processed-Chunks")
    cursor = collection.find({})
    print("\n")
    for index, doc in enumerate(cursor):
        # print(f"[$] Index: {Fore.YELLOW + Style.BRIGHT}{index}{Style.RESET_ALL}")
        print(f"[$] Unique Name: {Fore.YELLOW + Style.BRIGHT}{doc["Unique Name"]}{Style.RESET_ALL}")
        print(f"[$] Description: {Fore.YELLOW + Style.BRIGHT}{doc["Description"]}{Style.RESET_ALL}")
        print(f"[$] Cleaned Mails: {Fore.YELLOW + Style.BRIGHT}{len(doc["Cleaned Mails"])}{Style.RESET_ALL}")
        print("")

def return_chunk_names():
    collection = mongo_collection("Processed-Chunks")
    chunks = collection.find({}, {"Unique Name": 1 ,"_id":0})
    chunk_names = []
    
    for chunk in chunks:
        chunk_names.append(chunk["Unique Name"])
    print("")

    return chunk_names

def pull_data_chunk():
    chunk_names = return_chunk_names() # List

    selected_chunks = questionary.select(
        "Select the chunk to process", chunk_names
    ).ask()

    return selected_chunks

# ========================================================================================================

""" File Output """

def file_output():
    show_chunk_info()
    collection = mongo_collection("Processed-Chunks")
    cursor = collection.find()
    selected_chunk = pull_data_chunk()
    file_name = questionary.text("Enter file name:").ask()
    amount = int(questionary.text("How many mails per line?:").ask())

    for doc in cursor:
        if doc["Unique Name"] == selected_chunk:
            total_lines = 0
    
            with open(file_name, "w", encoding="utf-8") as f:
                for i in range(0, len(doc["Cleaned Mails"]), amount):
                    chunk = doc["Cleaned Mails"][i:i + amount]
    
                    line = ' '.join(chunk)
                    f.write(line + '\n')
                    total_lines += 1
            print("")
            print(
                f"{Fore.GREEN + Style.BRIGHT}[$] Exported {total_lines} line(s) in {file_name}{Style.RESET_ALL}.\n"
            )
            break

    else:
        print("[!] Error: Chunk not found!")

# ========================================================================================================

def main():
    pass

if __name__ == "__main__":
    main()