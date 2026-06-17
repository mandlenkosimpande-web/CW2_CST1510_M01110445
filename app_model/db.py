def create_users_table(conn):
    cur = conn.cursor()
    sql =  '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        );'''    
    cur.execute(sql)
    conn.commit()


def add_user(conn, username, password_hash, role='user'):
    cur = conn.cursor()
    sql = '''INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)'''
    cur.execute(sql, (username, password_hash, role))
    conn.commit()   

def migrate_users_to_db():
    """Migrate users from TXT/CSV file into SQLite database."""
    conn = sqlite3.connect('DATA/project_data.db')
    create_users_table(conn)


    with open(TXT_FILE, 'r') as f:
        reader = csv.DictReader(f, fieldnames=['username', 'password_hash', 'role'])
        for row in reader:
            #if the role column is missing, it will default to 'user'
                add_user(conn, row['username'], row['password_hash'], row.get('role', 'user'))
    conn.close()
    print("User data migrated to database successfully.")