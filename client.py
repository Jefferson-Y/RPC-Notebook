import xmlrpc.client
import datetime

SERVER_URL = "http://localhost:8000"

try:
    server = xmlrpc.client.ServerProxy(SERVER_URL)
except ConnectionRefusedError:
    print("Error: Unable to connect to the server. Please check if the server is running.")

def add_note():
    try:
        topic = input("Enter topic: ")
        note_name = input("Enter note title: ")
        text = input("Enter note text: ")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = server.add_note(topic, note_name, text, timestamp)
        print(response)
    except ConnectionRefusedError:
        print("Error: Server is not responding. Please restart the server and try again.")

def get_notes():
    try:
        topic = input("Enter topic to retrieve notes: ")
        response = server.get_notes(topic)
        print("Notes:\n", response)
    except ConnectionRefusedError:
        print("Error: Server is not responding. Please restart the server and try again.")

def search_wikipedia():
    try:
        topic = input("Enter topic to search on Wikipedia: ")
        response = server.search_wikipedia(topic)
        print("Wikipedia result:\n", response)
    except ConnectionRefusedError:
        print("Error: Server is not responding. Please restart the server and try again.")

def main():
    while True:
        print("\nOptions:")
        print("1. Add Note")
        print("2. Get Notes")
        print("3. Search Wikipedia")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            get_notes()
        elif choice == "3":
            search_wikipedia()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()