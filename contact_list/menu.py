from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from contact_manager import ContactManager
import random

def generate_random_person_id():
    return random.randint(1, 1000)

def add_person(contact_manager):
    person_id = generate_random_person_id()
    first_name = input("Adınız: ")
    last_name = input("Soyadınız: ")
    phone_number = input("Telefon Numarası: ")
    email = input("E-posta Adresi: ")
    contact_manager.add_person(person_id, first_name, last_name, phone_number, email)

def delete_person(contact_manager):
    person_id = int(input("Silmek istediğiniz kişinin ID'sini girin: "))
    contact_manager.delete_person(person_id)

def list_persons(contact_manager):
    keyword = input("Aranacak kelimeyi girin: ")
    result = contact_manager.list_persons(keyword)
    print(result)

def edit_person(contact_manager):
    person_id = int(input("Düzenlemek istediğiniz kişinin ID'sini girin: "))
    new_first_name = input("Yeni Ad: ")
    new_last_name = input("Yeni Soyad: ")
    new_phone_number = input("Yeni Telefon Numarası: ")
    new_email = input("Yeni E-posta Adresi: ")
    contact_manager.edit_person(person_id, new_first_name, new_last_name, new_phone_number, new_email)

def restore_data(contact_manager):
    print("Veriler yedekten geri yükleniyor...")
    contact_manager.restore_data()
    print("Veriler başarıyla geri yüklendi!")

contact_manager = ContactManager()

def create_main_menu(contact_manager):
    menu = ConsoleMenu(title="Kişi Yönetimi Menüsü", exit_option_text="Menüden Çık", clear_screen=False)

    add_person_item = FunctionItem("Kişi Ekle", add_person, [contact_manager])
    delete_person_item = FunctionItem("Kişi Sil", delete_person, [contact_manager])
    list_persons_item = FunctionItem("Kişileri Listele", list_persons, [contact_manager], should_exit=True)
    edit_person_item = FunctionItem("Kişi Düzenle", edit_person, [contact_manager])
    restore_data_item = FunctionItem("Yedekten Geri Yükle", restore_data, [contact_manager])
    menu.append_item(add_person_item)
    menu.append_item(delete_person_item)
    menu.append_item(list_persons_item)
    menu.append_item(edit_person_item)
    menu.append_item(restore_data_item)
    
    menu.show()