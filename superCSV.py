import os
import csv
from enum import Enum

contacts = []
filename = "Contact.csv"

class Selection(Enum):
    ADD = 1
    DELETE = 2
    SHOW = 3
    EXIT = 4
    CLEAR = 5
    EDIT = 6
    SEARCH = 7

def menu():
    """Display the menu options and return the user's selection."""
    for item in Selection:
        print(f'{item.value} - {item.name}')
    return Selection(int(input("Your selection? ")))

def search(action):
    """Search for a contact by first name."""
    contact_to_search = input(f"Contact to {action}? ")
    for i, contact in enumerate(contacts):
        if contact["fName"].lower() == contact_to_search.lower():
            print(f'{contact} found at index {i}')
            return i
    print("Contact not found.")
    return -1

def delete_contact(search_index):
    """Delete a contact by index."""
    if 0 <= search_index < len(contacts):
        del contacts[search_index]
        print("Contact deleted.")
        save_contacts_to_file(filename, contacts)  # Save changes to the file
    else:
        print("Invalid index. Contact not deleted.")

def edit_contact(search_index):
    """Edit a contact's details."""
    if 0 <= search_index < len(contacts):
        print("Current contact details:", contacts[search_index])
        new_fName = input("Enter new first name (leave empty to keep current): ")
        new_age = input("Enter new age (leave empty to keep current): ")
        if new_fName:
            contacts[search_index]['fName'] = new_fName
        if new_age:
            contacts[search_index]['age'] = int(new_age)
        print("Contact updated:", contacts[search_index])
        save_contacts_to_file(filename, contacts)  # Save changes to the file
    else:
        print("Invalid index. Contact not edited.")

def save_contacts_to_file(filename, contacts):
    """Save contacts to a CSV file."""
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["fName", "age"])
        writer.writeheader()
        writer.writerows(contacts)
    print(f"CSV file '{filename}' saved with contacts.")

def load_contacts_from_file(filename):
    """Load contacts from a CSV file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)  # Convert reader object to list of dictionaries
    return []  # Return an empty list if the file does not exist

def exit_app():
    """Save contacts and exit the application."""
    save_contacts_to_file(filename, contacts)
    print("Contacts saved. Exiting...")
    exit()

if __name__ == "__main__":
    contacts = load_contacts_from_file(filename)
    while True:
        user_selection = menu()
        if user_selection == Selection.EXIT:
            exit_app()
        elif user_selection == Selection.SHOW:
            print(contacts)
        elif user_selection == Selection.CLEAR:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif user_selection == Selection.ADD:
            fName = input("Enter name: ")
            age = int(input("Enter age: "))
            contacts.append({'fName': fName, 'age': age})
            save_contacts_to_file(filename, contacts)  # Save changes to the file
        elif user_selection == Selection.SEARCH:
            search_index = search('search')
        elif user_selection == Selection.DELETE:
            search_index = search('delete')
            delete_contact(search_index)
        elif user_selection == Selection.EDIT:
            search_index = search('edit')
            edit_contact(search_index)
