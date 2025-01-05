import configparser
import logging
import sqlite3
from pathlib import Path

# Ielādē konfigurācijas failu
config = configparser.ConfigParser()
config.read('config.ini')

# Iegūst iestatījumus
database = config['settings']['database']
log_level = config['settings']['log_level']

# Iestata žurnalēšanu
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Funkcija datubāzes izveidei
def initialize_database():
    db_path = Path(database)
    if not db_path.exists():
        logger.info(f'Izveido datubāzi: {database}')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # Izpilda migrācijas
        with open('migrations/001_create_contacts_table.sql', 'r') as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()
    else:
        logger.info(f'Datubāze {database} jau pastāv.')

# Funkcijas kontaktu pievienošanai, skatīšanai, rediģēšanai un dzēšanai
def add_contact(name, email, phone=None):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, phone)
            VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        logger.info(f'Pievienots kontakts: {name}')
    except sqlite3.IntegrityError:
        logger.error(f'Kontakts ar e-pastu {email} jau pastāv.')
    finally:
        conn.close()

def view_contacts():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def update_contact(contact_id, name=None, email=None, phone=None):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if name:
        cursor.execute('UPDATE contacts SET name = ? WHERE id = ?', (name, contact_id))
    if email:
        cursor.execute('UPDATE contacts SET email = ? WHERE id = ?', (email, contact_id))
    if phone:
        cursor.execute('UPDATE contacts SET phone = ? WHERE id = ?', (phone, contact_id))
    conn.commit()
    logger.info(f'Atjaunināts kontakts ar ID: {contact_id}')
    conn.close()

def delete_contact(contact_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    logger.info(f'Dzēsts kontakts ar ID: {contact_id}')
    conn.close()

# Galvenā funkcija
if __name__ == '__main__':
    initialize_database()
    # Piemēra izsaukumi
    add_contact('Ilze Bērziņa', 'ilzeb@example.com', '+37112345678')
    view_contacts()
