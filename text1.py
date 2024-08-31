import os
from enum import Enum

contacts = []
filename = "my2Contact.txt"

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
        if contact.split(',')[0].strip().lower() == contact_to_search.lower():
            print(f'{contact.strip()} found at index {i}')
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
        print("Current contact details:", contacts[search_index].strip())
        new_fName = input("Enter new first name (leave empty to keep current): ")
        new_age = input("Enter new age (leave empty to keep current): ")
        current_contact = contacts[search_index].split(',')
        if new_fName:
            current_contact[0] = new_fName
        if new_age:
            current_contact[1] = new_age
        contacts[search_index] = ','.join(current_contact)
        print("Contact updated:", contacts[search_index].strip())
        save_contacts_to_file(filename, contacts)  # Save changes to the file
    else:
        print("Invalid index. Contact not edited.")

def save_contacts_to_file(filename, contacts):
    """Save contacts to a text file."""
    with open(filename, 'w') as file:
        for contact in contacts:
            file.write(contact + '\n')
    print(f"Text file '{filename}' saved with contacts.")

def load_contacts_from_file(filename):
    """Load contacts from a text file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
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
            age = input("Enter age: ")
            contacts.append(f'{fName},{age}')
            save_contacts_to_file(filename, contacts)  # Save changes to the file
        elif user_selection == Selection.SEARCH:
            search_index = search('search')
        elif user_selection == Selection.DELETE:
            search_index = search('delete')
            delete_contact(search_index)
        elif user_selection == Selection.EDIT:
            search_index = search('edit')
            edit_contact(search_index)
