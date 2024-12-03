from mysql.connector import connect, Error
from time import sleep

DB_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': 'password',
    'database': 'mydatabase',
    'port': 3306
}

def wait_for_db():
    while True:
        try:
            conn = connect(**DB_CONFIG)
            conn.close()
            print('Connected to MySQL database')
            break
        except Error as e:
            print(f'Waiting... {e}')
            sleep(2)

def query_users():
    conn = connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    conn.close()
    return rows


def add_user(name, age):
    conn = connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, age) VALUES (%s, %s)', (name, age))
    conn.commit()
    cur.close()


if __name__ == '__main__':
    wait_for_db()

    # comment rows below after first start
    add_user('Diana', 28)
    add_user('Alice', 30)
    add_user('Bob', 25)
    add_user('Charlie', 35)
    ######################################
    # uncomment rows below after first start
    # add_user('Oliver', 8)
    # add_user('Megan', 95)
    # add_user('Michael', 51)
    # add_user('Vladimir', 39)
    ######################################

    users = query_users()
    print('Users:')
    for row in users:
        print(row)
