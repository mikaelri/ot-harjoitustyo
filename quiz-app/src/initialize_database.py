from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("DROP TABLE if exists users;")
    cursor.execute("DROP TABLE if exists questions;")
    cursor.execute("DROP TABLE if exists user_stats;")

    connection.commit()


def create_table_users(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL
            );
    """)

    connection.commit()


def create_table_user_stats(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE user_stats(
            username INTEGER NOT NULL,
            quiz_points INTEGER DEFAULT 0,
            FOREIGN KEY(username) REFERENCES users(username)
            );
    """)

    connection.commit()


def create_table_questions(connection):

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_1 TEXT NOT NULL,
            option_2 TEXT NOT NULL,
            option_3 TEXT NOT NULL,
            option_4 TEXT NOT NULL,
            correct_option INTEGER NOT NULL CHECK (correct_option BETWEEN 1 AND 4)
            );
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_table_users(connection)
    create_table_questions(connection)
    create_table_user_stats(connection)


if __name__ == "__main__":
    initialize_database()
