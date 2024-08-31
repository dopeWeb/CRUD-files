import os
import xml.etree.ElementTree as ET
from enum import Enum

contacts = []
filename = "Contact21.xml"

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
        if contact.find('fName').text.lower() == contact_to_search.lower():
            print(f'{ET.tostring(contact, encoding="unicode").strip()} found at index {i}')
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
        print("Current contact details:", ET.tostring(contact, encoding="unicode").strip())
        new_fName = input("Enter new first name (leave empty to keep current): ")
        new_age = input("Enter new age (leave empty to keep current): ")
        if new_fName:
            contact.find('fName').text = new_fName
        if new_age:
            contact.find('age').text = new_age
        print("Contact updated:", ET.tostring(contact, encoding="unicode").strip())
        save_contacts_to_file(filename, contacts)
    else:
        print("Invalid index. Contact not edited.")

def save_contacts_to_file(filename, contacts):
    """Save contacts to an XML file."""
    root = ET.Element("contacts")
    for contact in contacts:
        root.append(contact)
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"XML file '{filename}' saved with contacts.")

def load_contacts_from_file(filename):
    """Load contacts from an XML file."""
    if os.path.exists(filename):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            return list(root)
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
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
                print(ET.tostring(contact, encoding="unicode").strip())
        elif user_selection == Selection.CLEAR:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif user_selection == Selection.ADD:
            fName = input("Enter name: ")
            age = input("Enter age: ")
            contact = ET.Element('contact')
            fName_elem = ET.SubElement(contact, 'fName')
            age_elem = ET.SubElement(contact, 'age')
            fName_elem.text = fName
            age_elem.text = age
            contacts.append(contact)
            save_contacts_to_file(filename, contacts)
        elif user_selection == Selection.SEARCH:
            search_index = search('search')
        elif user_selection == Selection.DELETE:
            search_index = search('delete')
            delete_contact(search_index)
        elif user_selection == Selection.EDIT:
            search_index = search('edit')
            edit_contact(search_index)
