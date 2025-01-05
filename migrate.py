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
migrations_path = config['settings']['migrations_path']

# Iestata žurnalēšanu
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Funkcija migrāciju izpildei
def run_migrations():
    db_path = Path(database)
    if db_path.exists():
        logger.info(f'Veic migrācijas datubāzei: {database}')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        for migration_file in sorted(Path(migrations_path).glob('*.sql')):
            with open(migration_file, 'r') as f:
                cursor.executescript(f.read())
                logger.info(f'Izpildīta migrācija: {migration_file}')
        conn.commit()
        conn.close()
    else:
        logger.error(f'Datubāze {database} neeksistē. Vispirms izveidojiet datubāzi.')

if __name__ == '__main__':
    run_migrations()
