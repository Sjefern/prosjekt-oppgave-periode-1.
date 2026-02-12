import sqlite3
import hashlib
import os

DB_FILE = 'tyggis.db'

def dict_factory(cursor, row):
    """Konverter SQLite rows til dictionaries"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    """Åpne database tilkobling"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = dict_factory
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def hash_password(password):
    """Hash passord med SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """utfører database tabeller"""
    conn = get_db_connection()
    if not conn:
        print("Kunne ikke koble til database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Lag users tabell
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Lag cart tabell
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, product_id)
            )
        ''')
        
        # Lag orders tabell
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Lag order items tabell
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        print("Database tabeller opprettet/sjekket OK")
        return True
        
    except Exception as e:
        print(f"Database init error: {e}")
        return False
    finally:
        conn.close()

def create_user(username, email, password):
    """Registrer ny bruker"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        print(f"Bruker {email} opprettet")
        return True
        
    except sqlite3.IntegrityError:
        print(f"Epost {email} finnes allerede")
        return False
    except Exception as e:
        print(f"Create user error: {e}")
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    """Hent bruker fra epost"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Get user error: {e}")
        return None
    finally:
        conn.close()

def verify_user(email, password):
    """Sjekk om passord er riktig"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute(
            'SELECT id FROM users WHERE email = ? AND password_hash = ?',
            (email, password_hash)
        )
        user = cursor.fetchone()
        return user is not None
        
    except Exception as e:
        print(f"Verify user error: {e}")
        return False
    finally:
        conn.close()

