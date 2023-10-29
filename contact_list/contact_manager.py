import sqlite3
import csv
import json
import os
from datetime import datetime

class ContactManager:
    def __init__(self):
        self.check_directories()
        connection = sqlite3.connect("data/sqlite3/database.sqlite3")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS persons (
                       id INTEGER PRIMARY KEY,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       phone_number INTEGER,
                       email TEXT,
                       created_at DATE,
                       updated_at DATE
                       )''')
        connection.commit()
        connection.close()

    def check_directories(self):
        if not os.path.exists("data/csv_files"):
            os.makedirs("data/csv_files")
        if not os.path.exists("data/json_files"):
            os.makedirs("data/json_files")
        if not os.path.exists("data/ismetify"):
            os.makedirs("data/ismetify")
        if not os.path.exists("data/sqlite3"):
            os.makedirs("data/sqlite3")

    def add_person(self, person_id, first_name, last_name, phone_number, email):
        print("Kişi Ekle işlemi seçildi.")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_at = created_at
        connection = sqlite3.connect("data/sqlite3/database.sqlite3")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO persons (id, first_name, last_name, phone_number, email, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (person_id, first_name, last_name, phone_number, email, created_at, updated_at))
        connection.commit()
        connection.close()

        with open("data/csv_files/persons.csv", mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([person_id, first_name, last_name, phone_number, email, created_at, updated_at])
            print("")

        data = {
            "id": person_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email,
            "created_at": created_at,
            "updated_at": updated_at
        }
        try:
            with open("data/json_files/persons.json", "r") as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = []

        if isinstance(existing_data, list):
            existing_data.append(data)
        else:
            existing_data = [data]

        with open("data/json_files/persons.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=2)

        with open('data/ismetify/ismetify.file', 'a') as ismetify_file:
            ismetify_file.write(f"{person_id}|{first_name}|{last_name}|{phone_number}|{email}|{created_at}|{updated_at}\n")

        print("Kişi başarıyla eklendi!")

    def delete_person(self, person_id):
        print("Kişi Sil işlemi seçildi.")
        connection = sqlite3.connect("data/sqlite3/database.sqlite3")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM persons WHERE id=?", (person_id,))
        connection.commit()
        connection.close()

        temp_csv = "data/csv_files/temp.csv"
        with open("data/csv_files/persons.csv", mode="r") as csv_file, open(temp_csv, mode="w", newline="") as temp_file:
            csv_reader = csv.reader(csv_file)
            csv_writer = csv.writer(temp_file)
            for row in csv_reader:
                if str(person_id) not in row[0]:
                    csv_writer.writerow(row)
            csv_file.close()
            temp_file.close()
        os.remove("data/csv_files/persons.csv")
        os.rename(temp_csv, "data/csv_files/persons.csv")

        temp_json = "data/json_files/temp.json"
        with open("data/json_files/persons.json", "r") as json_file, open(temp_json, "w") as temp_file:
            data_list = json.load(json_file)
            updated_data_list = [data for data in data_list if data["id"] != person_id]
            json.dump(updated_data_list, temp_file, indent=2)
        os.remove("data/json_files/persons.json")
        os.rename(temp_json, "data/json_files/persons.json")

        with open('data/ismetify/ismetify.file', 'r') as ismetify_file:
            lines = ismetify_file.readlines()
        with open('data/ismetify/ismetify.file', 'w') as ismetify_file:
            for line in lines:
                parts = line.strip().split('|')
                if int(parts[0]) != person_id:
                    ismetify_file.write(line)

        print("Kişi başarıyla silindi!")

    def list_persons(self, keyword):
        print("Kişileri Listele işlemi seçildi.")
        connection = sqlite3.connect("data/sqlite3/database.sqlite3")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM persons WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?",
                            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()
        connection.commit()
        connection.close()

        found = False

        if results:
            print("Arama Sonuçları:")
            for row in results:
                print(row)

            with open("data/csv_files/persons.csv", mode="r") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                founded_datas = []
                for row in csv_reader:
                    person_id, first_name, last_name, phone_number, email, created_at, updated_at = row
                    if keyword.lower() in (first_name + last_name + email).lower():
                        found = True
                        founded_datas.append({
                            "id": person_id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "phone_number": phone_number,
                            "email": email,
                            "created_at": created_at,
                            "updated_at": updated_at
                        })
                return founded_datas

        if not found:
            with open("data/json_files/persons.json", "r") as json_file:
                data = json.load(json_file)
            founded_datas = []
            
            for i in data:
                name = i.get("first_name")
                last_name = i.get("last_name")
                email = i.get("email")
                if keyword.lower() in name.lower() or keyword.lower() in last_name.lower() or keyword.lower() in email.lower():
                    found = True
                    founded_datas.append(i)
            return founded_datas
        
        if not found:
            with open('data/ismetify/ismetify.file', "r") as file:
                lines = file.readlines()
                founded_datas = []
                
                for line in lines:
                    row = line.strip().split('|')
                    first_name, last_name, email = row[1], row[2], row[4]
                    if keyword.lower() in first_name.lower() or keyword.lower() in last_name.lower() or keyword.lower() in email.lower():
                        found = True
                        founded_datas.append(row)
                return founded_datas
                
    def edit_person(self, person_id, new_first_name, new_last_name, new_phone_number, new_email):
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Kişi Düzenle işlemi seçildi.")
        connection = sqlite3.connect("data/sqlite3/database.sqlite3")
        cursor = connection.cursor()
        cursor.execute("UPDATE persons SET first_name=?, last_name=?, phone_number=?, email=?, updated_at=? WHERE id=?",
                            (new_first_name, new_last_name, new_phone_number, new_email, updated_at, person_id))
        connection.commit()
        connection.close()

        temp_csv = "data/csv_files/temp.csv"
        with open("data/csv_files/persons.csv", mode="r") as csv_file, open(temp_csv, mode="w", newline="") as temp_file:
            csv_reader = csv.reader(csv_file)
            csv_reader = list(csv_reader)
            csv_writer = csv.writer(temp_file)
            for row in csv_reader:
                if str(person_id) in row[0]:
                    created_at = row[5]
                    csv_writer.writerow([person_id, new_first_name, new_last_name, new_phone_number, new_email, created_at, updated_at])
                else:
                    csv_writer.writerow(row)
            csv_file.close()
            temp_file.close()
        os.remove("data/csv_files/persons.csv")
        os.rename(temp_csv, "data/csv_files/persons.csv")

        temp_json = "data/json_files/temp.json"
        with open("data/json_files/persons.json", "r") as json_file, open(temp_json, "w") as temp_file:
            data = json.load(json_file)
            for i in data:
                    if i["id"] == person_id:
                        i["first_name"] = new_first_name
                        i["last_name"] = new_last_name
                        i["phone_number"] = new_phone_number
                        i["email"] = new_email
                        i["updated_at"] = updated_at

            json.dump(data, temp_file, indent=2)
        os.remove("data/json_files/persons.json")
        os.rename(temp_json, "data/json_files/persons.json")

        temp_file = "data/ismetify/temp.ismetify"
        with open('data/ismetify/ismetify.file', 'r', encoding='utf-8') as ismetify_file, open(temp_file, 'w', encoding='utf-8') as temp_temp_file:
            for line in ismetify_file:
                parts = line.strip().split('|')
                if parts[0] == str(person_id):
                    parts[1] = new_first_name
                    parts[2] = new_last_name
                    parts[3] = new_phone_number
                    parts[4] = new_email
                    parts[6] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    line = '|'.join(parts) + '\n'
                temp_temp_file.write(line)

        os.remove('data/ismetify/ismetify.file')
        os.rename(temp_file, 'data/ismetify/ismetify.file')

        print("Kişi başarıyla güncellendi!")

if __name__ == "__main__":
    manager = ContactManager()
    manager.list_persons("emre")