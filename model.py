import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    # Checks to see if connection is already established
    if DB == None:
        CONN = sqlite3.connect("thewall.db")
        DB = CONN.cursor()

def authenticate(username, password):
    connect_to_db()
    query = """SELECT username, password, id 
               FROM users 
               WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    if username == row[0] and hash(password) == int(row[1]):
        return row[2] # userid
    else:
        return None

def get_userid_by_name(username):
    connect_to_db()
    query = """SELECT id 
               FROM users 
               WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row[0] # userid

def get_username_by_id(user_id):
    connect_to_db()
    query = """ SELECT username
                FROM users
                WHERE id = ?"""
    DB.execute(query, (user_id,))
    row = DB.fetchone()
    return str(row[0]) # username

def get_wall_posts_by_user(user_id):
    connect_to_db()
    query = """SELECT users.username, content, created_at 
               FROM wall_posts 
               JOIN users ON (users.id=wall_posts.author_id) 
               WHERE owner_id=?"""
    DB.execute(query, (user_id,))
    row = DB.fetchall()
    return row

def create_wall_post(owner_id, author_id, content):
    connect_to_db()
    query = """INSERT INTO wall_posts (owner_id, author_id, created_at, content) 
               VALUES (?, ?, datetime('now'), ?)"""
    print "This is the query %r" %(query)
    DB.execute(query, (owner_id, author_id, content))
    CONN.commit()            

    # author_id being the user_id associated with the username


