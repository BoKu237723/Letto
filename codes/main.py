import functions
import personalized

def show_options():
    print("\n$$ =========================== MENU =========================== $$\n")
    print("(1) Add new event")
    print("(2) Display all events in database")
    print("(3) Display specific event(s) data in detail")
    print("(4) Display all data chunks")
    print("(5) Make new data chunk")
    print("(6) Make file output")
    print("(7) Send Personalized Certs")
    print("(8) Exist")

def main():
    while True:
        try:
            show_options()
            user_input = int(input("\n(:) Choose Your Option: "))

            if user_input == 1:
                functions.add_new_event()
                continue

            elif user_input == 2:
                functions.pullout_event_names()
                continue

            elif user_input == 3:
                functions.display_events_detail()
                continue

            elif user_input == 4:
                functions.show_chunks()
                continue

            elif user_input == 5:
                functions.create_chunk()
                continue

            elif user_input == 6:
                functions.file_output()
                continue

            elif user_input == 7:
                personalized.personalized_mails()
                continue

            elif user_input == 8:
                break

            else:
                print("[!] Invalid Input.")

        except ValueError:
            print("[!] Enter only integers.")
            continue

        except KeyboardInterrupt:
            print("\n[!] Keyboard Interruption Detected.")
            break

if __name__ == "__main__":
    main()