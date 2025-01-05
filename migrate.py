import configparser
import logging
import mysql.connector
from pathlib import Path

# Ielādē konfigurācijas failu
config = configparser.ConfigParser()
config.read('config.ini')

# Iegūst iestatījumus
host = config['settings']['host']
user = config['settings']['user']
password = config['settings']['password']
database = config['settings']['database']
log_level = config['settings']['log_level']
migrations_path = config['settings']['migrations_path']

# Iestata žurnalēšanu
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Funkcija migrāciju izpildei
def run_migrations():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        for migration_file in sorted(Path(migrations_path).glob('*.sql')):
            with open(migration_file, 'r') as f:
                cursor.execute(f.read(), multi=True)
                logger.info(f'Izpildīta migrācija: {migration_file}')
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        logger.error(err)

if __name__ == '__main__':
    run_migrations()
