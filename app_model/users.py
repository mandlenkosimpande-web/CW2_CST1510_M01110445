def add_user(conn, username, password_hash, role = 'user'):
    cur = conn.cursor()
    sql = '''INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)'''
    param = (username, password_hash, role)
    cur.execute(sql, param)
    conn.commit()   

def migrate_users_to_db(conn):
    with open(TXT_FILE, 'r') as f:
        users = f.readlines()
#the following lines of code allow me to skip the header row so it is not passed as an actuall user
    for user in users[1:]:  
        parts = user.strip().split(',')
        if len(parts) < 3:
            continue  # skipping blank or malformed lines 
        username, password_hash, role = parts[0], parts[1], parts[2]
        add_user(conn, username, password_hash, role)


def get_all_users(conn):
    cur = conn.cursor()
    create_users_table(conn)
    migrate_users_to_db(conn)
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    users = cur.fetchall()
    conn.close()
    return(users)   

#read just one user based of name 

def get_user(conn, name ):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql, param)
    user = cur.fetchone()
    conn.close()
    return(user)

def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    param = (new_name,old_name)
    cur.execute(sql, param)
    conn.commit()
    conn.close

def delete_user(conn, user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (user_name,)
    cur.execute(sql, param)
    conn.commit()