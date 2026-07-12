import sqlite3


def create_db():

    conn = sqlite3.connect("movies.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_name TEXT
    )
    """)

    conn.commit()
    conn.close()



def add_favorite(user_id, movie_name):

    conn = sqlite3.connect("movies.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO favorites(user_id, movie_name) VALUES (?,?)",
        (user_id, movie_name)
    )

    conn.commit()
    conn.close()



def get_favorites(user_id):

    conn = sqlite3.connect("movies.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT movie_name FROM favorites WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data