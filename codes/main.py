import functions
import personalized
from colorama import Fore, Style 

def colored(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def show_options():
    print("")
    print(colored("$$ =========================== MENU =========================== $$\n", Fore.CYAN + Style.BRIGHT))
    print(colored("(1) Add new event", Fore.BLUE))
    print(colored("(2) Display all events in database", Fore.BLUE))
    print(colored("(3) Display specific event(s) data in detail", Fore.BLUE))
    print(colored("(4) Display all data chunks", Fore.BLUE))
    print(colored("(5) Make new data chunk", Fore.BLUE))
    print(colored("(6) Make file output", Fore.BLUE))
    print(colored("(7) Send Personalized Certs", Fore.BLUE))
    print(colored("(8) Exit", Fore.BLUE))
    print("")

def main():
    show_options()
    while True:
        try:
            user_input = int(input("(:) Choose Your Option: "))

            if user_input == 0:
                show_options()
                continue
            
            elif user_input == 1:
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
                print(colored("[!] Invalid Input.", Fore.YELLOW))

        except ValueError:
            print(colored("[!] Enter only integers.", Fore.YELLOW))
            continue

        except KeyboardInterrupt:
            print("")
            print(colored("[!] Keyboard Interruption Detected.", Fore.YELLOW))
            break

if __name__ == "__main__":
    main()