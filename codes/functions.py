from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import os
import re
from collections import Counter

from dotenv import load_dotenv
load_dotenv()

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

""" Support Functions """

def get_current_time():
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return time

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

    print(f"$$ Processed Raw Mails: {len(raw_mails)}")
    print(f"$$ Valid Mails: {len(valid_mails)}")
    print(f"$$ Invalid Mails: {len(invalid_mails)}")
    print(f"$$ Unique Mails: {len(unique_mails)}")
    print(f"$$ Duplicate Mails: {len(duplicates_mails)}")
    print(f"$$ Final Cleaned Mails: {len(unique_mails)}")

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
    print("")
    print("$$ Raw data inserted successfully to (Past-Raw) collection")

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
        print("$$ Clean data inserted successfully to (Past-Cleaned) collection")
    except Exception as e:
        print(f"Error: {e}")

def add_new_event():
    v_event_name = input("\nEnter your event name: ")
    v_file_name = input("Enter file (.xlsx) name to process: ")
    v_column = int(input("Enter column index for mails (0 for first column): "))

    try:
        v_read_data = pd.read_excel(v_file_name)
        v_extracted_mails = v_read_data.iloc[:, v_column].tolist()
        save_to_past_raw(v_event_name, v_extracted_mails)
        save_to_past_cleaned(v_event_name, v_extracted_mails)
    except Exception as e:
        print(f"Error Occured: {e}")


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

    print("\n$$ ================== All Events In Database ================== $$\n")

    for event in event_names:
        print(f"[{event_names.index(event)}] {event}")

    return event_names # List ["Event-1", "Event-2", "Evet-3"]

def display_events_detail():
    db = client["Letto"]
    collection = db["Past-Cleaned"]
    cursor = collection.find({})
    docs = list(cursor)
    
    input_range = data_range() # List

    print("\n$$ ============= Displaying Event Data in Detail ============== $$")

    for i in input_range:
        doc = docs[i]
        event_name, event_data = next(
            (key, value) for key, value in doc.items() if key != "_id"
        )

        created_time     =   event_data["datetime"]
        valid_mails      =   event_data["valid_mails"]
        invalid_mails    =   event_data["invalid_mails"]
        unique_mails     =   event_data["unique_mails"]
        duplicate_mails  =   event_data["duplicate_mails"]
        final_mails      =   event_data["final_mails"]

        print("")
        print(f">>>> {event_name} <<<<")
        print(f"Created Time: {created_time}")
        print(f"Valid Mails: {len(valid_mails)}")
        print(f"Invalid Mails: {len(invalid_mails)}")
        print(f"Unique Mails: {len(unique_mails)}")
        print(f"Duplicate Mails: {len(duplicate_mails)}")
        print(f"Ready to Use Mails: {len(final_mails)}")

# ========================================================================================================

# Return all event names | No Display

def return_all_event_names():
    collection = mongo_collection("Past-Cleaned")
    events = collection.find({}, {"_id": 0})
    event_names = []

    for event in events:
        event_names.extend(event.keys())

    return event_names

# ========================================================================================================

""" Data Range """

def range_help():
    print("")
    print("## These are Sample Formats")
    print("## (All Events except 8 and 10) 0-7 9 11-12")
    print("## (All Events) * || 0-12 || 0 1 2 3 4 5 6 7 8 9 10 11 12")

def data_range(): # Example: 0-4 6 8-9 11 # Output a list of index of chosen events
    total_events = pullout_event_names()
    while True:
        numbers = []
        user_range = input("\nSelect Your Range (? for help): ").strip() # String

        if user_range == "?":
            range_help()
            continue

        elif user_range == "*":
            index = 0
            for i in range(len(total_events)):
                numbers.append(index)
                index += 1
            break

        else:
            for i in user_range.split(" "):
                if "-" in i:
                    start, end = map(int, i.split("-"))
                    numbers.extend(range(start, end+1))
                else:
                    numbers.append(int(i))

                greater_check = any(x > (len(total_events)) for x in numbers)

            if greater_check == True:
                print(f"Only {len(total_events)} exists.")
                continue
            break

    return numbers

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
        print(f"Removed {len(duplicates)} duplicate mails.")

        return final_mails, duplicates

    except Exception as e:
        print(f"Error Occured: {e}")

def create_chunk():
    collection = mongo_collection("Processed-Chunks")
    events_index_to_chunk = data_range() # List
    total_events = return_all_event_names()

    events_to_process = [] # Sample: ["Event-0", "Event-2", "Event-3", "Event-5"]

    for i in events_index_to_chunk:
        events_to_process.append(total_events[i])

    final_data, duplicates = create_chunk_mails(events_to_process)

    unique_name = input("Enter unique name for this chunk: ") # TODO: Need validation
    description = input("Enter a description for this chunk: ")
    time = get_current_time()

    data = {
        "Unique Name": unique_name,
        "Description": description,
        "Created Date": time,
        "Included Events": events_to_process,
        "Cleaned Mails": final_data,
        "Duplicate Mails": duplicates
    }

    collection.insert_one(data)
    print("")
    print(f"$$ Data Chunk '{unique_name}' created with {len(final_data)} cleaned mails from {len(events_to_process)} events.")

def show_chunks():

    print("\n$$ ============= All Available Chunks in Database ============= $$")
    
    collection = mongo_collection("Processed-Chunks")
    cursor = collection.find({})
    for index, doc in enumerate(cursor):
        print("")
        print(f"Index: {index}")
        print(f">>>>>> {doc["Unique Name"]} <<<<<<")
        print(f"Description: {doc["Description"]}")
        print(f"Created Data: {doc["Created Date"]}")
        print(f"Included Events: {doc["Included Events"]}")
        print(f"Cleaned Mails: {len(doc["Cleaned Mails"])}")
        print(f"Removed Duplicates: {len(doc["Duplicate Mails"])}")

    pass

# ========================================================================================================

""" File Output """

def file_output():
    show_chunks()
    collection = mongo_collection("Processed-Chunks")
    cursor = collection.find()
    selected_chunk = int(input("\nEnter Index of chunk to process: "))
    file_name= input("Enter file name: ")
    amount = int(input("How many mails per line?: "))

    for index, doc in enumerate(cursor):
        if index == selected_chunk:
            total_lines = 0

            with open (file_name, "w", encoding="utf-8") as f:
                for i in range(0, len(doc["Cleaned Mails"]), amount):
                    chunk = doc["Cleaned Mails"][i:i+amount]
    
                    line = ' '.join(chunk)
                    f.write(line + '\n')
                    total_lines += 1

            print(f"Exported {total_lines} line(s) in {file_name}.")
            break

    else:
        print("Chunk ID not found!")

# ========================================================================================================

def main():
    pass

if __name__ == "__main__":
    main()