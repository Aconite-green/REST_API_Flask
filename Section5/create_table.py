import sqlite3
# DB생성 또는 연결
connection = sqlite3.connect('data.db')
# DB에서 SQL 작업을 위한 cursor 생성
cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# create table
create_table = "CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)"
cursor.execute(create_table)

#변경사항을 DB에 반영
connection.commit()

#DB제어 종료
connection.close()