import os
import mysql.connector
import pytest
import configparser
from mysql.connector import errorcode
from main import add_contact, view_contacts, update_contact, delete_contact

# Ielādē konfigurācijas failu
config = configparser.ConfigParser()
config.read('config.ini')

# Iegūst iestatījumus
host = config['settings']['host']
user = config['settings']['user']
password = config['settings']['password']
database = config['settings']['database']

# Testa datubāzes nosaukums
TEST_DB = 'test_contacts_db'

@pytest.fixture(scope='module')
def db():
    # Izveido testa datubāzi
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TEST_DB}")
    conn.database = TEST_DB
    cursor.execute(f"USE {TEST_DB}")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(20)
        )
    ''')
    conn.commit()
    yield conn
    cursor.execute(f"DROP DATABASE {TEST_DB}")
    conn.close()

def test_add_contact(db):
    add_contact('Anna Liepkalna', 'annali@example.com', '+37128765432')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contacts WHERE email = %s', ('annali@example.com',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'Anna Liepkalna'
    assert result[2] == 'annali@example.com'
    assert result[3] == '+37128765432'

def test_view_contacts(db, capsys):
    view_contacts()
    captured = capsys.readouterr()
    assert 'Anna Liepkalna' in captured.out
    assert 'annali@example.com' in captured.out
    assert '+37128765432' in captured.out

def test_update_contact(db):
    cursor = db.cursor()
    cursor.execute('SELECT id FROM contacts WHERE email = %s', ('annali@example.com',))
    contact_id = cursor.fetchone()[0]
    update_contact(contact_id, name='Anna Koriņa', phone='+37122312345')
    cursor.execute('SELECT * FROM contacts WHERE id = %s', (contact_id,))
    result = cursor.fetchone()
    assert result[1] == 'Anna Koriņa'
    assert result[3] == '+37122312345'

def test_delete_contact(db):
    cursor = db.cursor()
    cursor.execute('SELECT id FROM contacts WHERE email = %s', ('annali@example.com',))
    contact_id = cursor.fetchone()[0]
    delete_contact(contact_id)
    cursor.execute('SELECT * FROM contacts WHERE id = %s', (contact_id,))
    result = cursor.fetchone()
    assert result is None
