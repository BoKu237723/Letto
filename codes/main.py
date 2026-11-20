import functions
import personalized
import questionary
from colorama import Fore, Style 

def colored(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def main():
    print("")
    while True:
        print(colored("$$ =========================== MENU =========================== $$\n", Fore.BLUE + Style.BRIGHT))
        choice = questionary.select(
            "What do you want to do?",
            choices=["(1) Add new event", "(2) Display specific event(s) data in detail", "(3) Delete Specific Event(s)", "(4) Make new data chunk", "(5) Display specific data chunk(s) in detail", "(6) Delete Specific Chunk(s)" , "(7) Make file output", "(8) Send Personalized Certs", "(9) Exit"],
        ).ask()

        if choice == "(1) Add new event":
            functions.add_new_event()
            continue
        elif choice == "(2) Display specific event(s) data in detail":
            functions.display_events_detail()
            continue
        elif choice == "(3) Delete Specific Event(s)":
            functions.delete_events()
            continue
        elif choice == "(4) Make new data chunk":
            functions.create_chunk()
            continue
        elif choice == "(5) Display specific data chunk(s) in detail":
            functions.show_chunks()
            continue
        elif choice == "(6) Delete Specific Chunk(s)":
            functions.delete_chunks()
            continue
        elif choice == "(7) Make file output":
            functions.file_output()
            continue
        elif choice == "(8) Send Personalized Certs":
            personalized.personalized_mails()
            continue
        elif choice == "(9) Exit":
            break

if __name__ == "__main__":
    main()