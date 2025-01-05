import configparser
import logging
import mysql.connector
from mysql.connector import errorcode

# Ielādē konfigurācijas failu
config = configparser.ConfigParser()
config.read('config.ini')

# Iegūst iestatījumus no konfigurācijas faila
host = config['settings']['host']
user = config['settings']['user']
password = config['settings']['password']
database = config['settings']['database']
log_level = config['settings']['log_level']

# Iestata žurnalēšanu
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Funkcija datubāzes izveidei
def initialize_database():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        logger.info(f'Izveido datubāzi: {database}')
        conn.database = database
        cursor.execute(f"USE {database}")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                phone VARCHAR(20)
            )
        ''')
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Nepareizs lietotājvārds vai parole")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error(f'Datubāze {database} neeksistē')
        else:
            logger.error(err)

# Pievieno funkcijas kontaktu pievienošanai, skatīšanai, rediģēšanai un dzēšanai
def add_contact(name, email, phone=None):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, phone)
            VALUES (%s, %s, %s)
        ''', (name, email, phone))
        conn.commit()
        logger.info(f'Pievienots kontakts: {name}')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            logger.error(f'Kontakts ar e-pastu {email} jau pastāv.')
        else:
            logger.error(err)
    finally:
        conn.close()

def view_contacts():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()
    except mysql.connector.Error as err:
        logger.error(err)

def update_contact(contact_id, name=None, email=None, phone=None):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE contacts SET name = %s WHERE id = %s', (name, contact_id))
        if email:
            cursor.execute('UPDATE contacts SET email = %s WHERE id = %s', (email, contact_id))
        if phone:
            cursor.execute('UPDATE contacts SET phone = %s WHERE id = %s', (phone, contact_id))
        conn.commit()
        logger.info(f'Atjaunināts kontakts ar ID: {contact_id}')
        conn.close()
    except mysql.connector.Error as err:
        logger.error(err)

def delete_contact(contact_id):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id = %s', (contact_id,))
        conn.commit()
        logger.info(f'Dzēsts kontakts ar ID: {contact_id}')
        conn.close()
    except mysql.connector.Error as err:
        logger.error(err)

# Galvenā funkcija ar lietotāja ievadi
if __name__ == '__main__':
    initialize_database()
    
    while True:
        print("\nIzvēlieties darbību:")
        print("1. Pievienot kontaktu")
        print("2. Skatīt kontaktus")
        print("3. Atjaunināt kontaktu")
        print("4. Dzēst kontaktu")
        print("5. Iziet")
        choice = input("Ievadiet izvēli (1-5): ")

        if choice == '1':
            name = input("Ievadiet vārdu: ")
            email = input("Ievadiet e-pasta adresi: ")
            phone = input("Ievadiet tālruņa numuru (nav obligāti): ")
            add_contact(name, email, phone)
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            contact_id = input("Ievadiet kontaktpersonas ID, kuru vēlaties atjaunināt: ")
            name = input("Ievadiet jauno vārdu (vai atstājiet tukšu, lai nesamainītu): ")
            email = input("Ievadiet jauno e-pasta adresi (vai atstājiet tukšu, lai nesamainītu): ")
            phone = input("Ievadiet jauno tālruņa numuru (vai atstājiet tukšu, lai nesamainītu): ")
            update_contact(contact_id, name, email, phone)
        elif choice == '4':
            contact_id = input("Ievadiet kontaktpersonas ID, kuru vēlaties dzēst: ")
            delete_contact(contact_id)
        elif choice == '5':
            break
        else:
            print("Nederīga izvēle. Lūdzu, mēģiniet vēlreiz.")
