import sqlite3
import hashlib
import os

# Database file path
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
    """Initialiserer database tabeller"""
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
        
        # Lag orders-tabell
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

def add_cart_item(user_id, product_id, quantity):
    """Legg til produkt i handlekurv"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Sjekk om produktet allerede er i kurven
        cursor.execute(
            'SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        item = cursor.fetchone()
        
        if item:
            # Oppdater antall
            new_quantity = item['quantity'] + quantity
            cursor.execute(
                'UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?',
                (new_quantity, user_id, product_id)
            )
        else:
            # Legg til nytt produkt
            cursor.execute(
                'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
                (user_id, product_id, quantity)
            )
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Add cart item error: {e}")
        return False
    finally:
        conn.close()

def get_cart_items_for_user(user_id):
    """Hent handlekurv for bruker"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT product_id, quantity FROM cart WHERE user_id = ?',
            (user_id,)
        )
        items = cursor.fetchall()
        return items
        
    except Exception as e:
        print(f"Get cart items error: {e}")
        return []
    finally:
        conn.close()

def remove_cart_item_for_user(user_id, product_id):
    """Fjern produkt fra handlekurv"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM cart WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Remove cart item error: {e}")
        return False
    finally:
        conn.close()

def clear_cart_for_user(user_id):
    """Tøm hele handlekurven"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Clear cart error: {e}")
        return False
    finally:
        conn.close()

def create_order(user_id, cart_items, products_dict):
    """Lag en ordre fra handlekurv"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Beregn total pris
        total_price = 0
        for item in cart_items:
            product = products_dict.get(item['product_id'])
            if product:
                total_price += product['price'] * item['quantity']
        
        # Opprett ordre
        cursor.execute(
            'INSERT INTO orders (user_id, total_price) VALUES (?, ?)',
            (user_id, total_price)
        )
        order_id = cursor.lastrowid
        
        # Legg til order items
        for item in cart_items:
            product = products_dict.get(item['product_id'])
            if product:
                cursor.execute(
                    'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                    (order_id, item['product_id'], item['quantity'], product['price'])
                )
        
        conn.commit()
        return order_id
        
    except Exception as e:
        print(f"Create order error: {e}")
        return None
    finally:
        conn.close()

# Initialiserer database når modulen importeres
init_db()
