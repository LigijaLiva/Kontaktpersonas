import os
import sqlite3
import pytest
from main import add_contact, view_contacts, update_contact, delete_contact

# Testa datubāzes nosaukums
TEST_DB = 'test_contacts.db'

@pytest.fixture(scope='module')
def db():
    # Izveido testa datubāzi
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT
        )
    ''')
    conn.commit()
    yield conn
    conn.close()
    os.remove(TEST_DB)

def test_add_contact(db):
    add_contact('Anna Liepa', 'anna@example.com', '+37198765432')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contacts WHERE email = ?', ('anna@example.com',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'Anna Liepkalna'
    assert result[2] == 'annaliep@example.com'
    assert result[3] == '+37128765432'

def test_view_contacts(db, capsys):
    view_contacts()
    captured = capsys.readouterr()
    assert 'Anna Liepkalna' in captured.out
    assert 'annaliep@example.com' in captured.out
    assert '+37128765432' in captured.out

def test_update_contact(db):
    cursor = db.cursor()
    cursor.execute('SELECT id FROM contacts WHERE email = ?', ('annaliep@example.com',))
    contact_id = cursor.fetchone()[0]
    update_contact(contact_id, name='Anna Koriņa', phone='+37122312345')
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    result = cursor.fetchone()
    assert result[1] == 'Anna Koriņa'
    assert result[3] == '+37122312345'

def test_delete_contact(db):
    cursor = db.cursor()
    cursor.execute('SELECT id FROM contacts WHERE email = ?', ('annaliep@example.com',))
    contact_id = cursor.fetchone()[0]
    delete_contact(contact_id)
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    result = cursor.fetchone()
    assert result is None
