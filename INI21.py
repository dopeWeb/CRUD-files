import os
import configparser
from enum import Enum

contacts = []
filename = "Contact21.ini"

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
        if contact.get('fName', '').lower() == contact_to_search.lower():
            print(f'{contact} found at index {i}')
            return i
    print("Contact not found.")
    return -1

def delete_contact(search_index):
    """Delete a contact by index."""
    if 0 <= search_index < len(contacts):
        del contacts[search_index]
        print("Contact deleted.")
        save_contacts_to_file(filename, contacts)
    else:
        print("Invalid index. Contact not deleted.")

def edit_contact(search_index):
    """Edit a contact's details."""
    if 0 <= search_index < len(contacts):
        contact = contacts[search_index]
        print("Current contact details:", contact)
        new_fName = input("Enter new first name (leave empty to keep current): ")
        new_age = input("Enter new age (leave empty to keep current): ")
        if new_fName:
            contact['fName'] = new_fName
        if new_age:
            contact['age'] = int(new_age)
        print("Contact updated:", contact)
        save_contacts_to_file(filename, contacts)
    else:
        print("Invalid index. Contact not edited.")

def save_contacts_to_file(filename, contacts):
    """Save contacts to an INI file."""
    config = configparser.ConfigParser()
    config.read_dict({'contacts': {f'contact_{i}': f"fName = {contact['fName']}\nage = {contact['age']}" 
                                   for i, contact in enumerate(contacts)}})
    with open(filename, 'w') as file:
        config.write(file)
    print(f"INI file '{filename}' saved with contacts.")

def load_contacts_from_file(filename):
    """Load contacts from an INI file."""
    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename)
        contacts = []
        for section in config.sections():
            if section == 'contacts':
                for key in config[section]:
                    contact_data = config[section][key].split('\n')
                    contact = {
                        'fName': contact_data[0].split('=')[1].strip(),
                        'age': int(contact_data[1].split('=')[1].strip())
                    }
                    contacts.append(contact)
        return contacts
    else:
        print(f"File '{filename}' does not exist.")
    return []

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
            for contact in contacts:
                print(contact)
        elif user_selection == Selection.CLEAR:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif user_selection == Selection.ADD:
            fName = input("Enter name: ")
            age = int(input("Enter age: "))
            contacts.append({'fName': fName, 'age': age})
            save_contacts_to_file(filename, contacts)
        elif user_selection == Selection.SEARCH:
            search_index = search('search')
        elif user_selection == Selection.DELETE:
            search_index = search('delete')
            delete_contact(search_index)
        elif user_selection == Selection.EDIT:
            search_index = search('edit')
            edit_contact(search_index)
