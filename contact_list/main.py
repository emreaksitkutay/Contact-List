from menu import create_main_menu
from contact_manager import ContactManager

def main():
    contact_manager = ContactManager()
    main_menu = create_main_menu(contact_manager)

if __name__ == "__main__":
    main()