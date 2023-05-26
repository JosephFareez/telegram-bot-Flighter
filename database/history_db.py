import sqlite3
import datetime


def db_create(user_id, message, retrieve=False):
    try:
        # Convert user_id to integer
        user_id = int(user_id)

        conn = sqlite3.connect('users_db.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS login_id (user_id INTEGER, login_count INTEGER, timestamp DATETIME, message TEXT);")
        # Check if user_id already exists in table
        cursor.execute("SELECT * FROM login_id WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        if result:
            # User already exists in table
            messages = result[3].split("\n")[-21:]
            if not retrieve:
                # Append new message to existing messages and update row
                messages.append(message)
                messages_str = "\n".join(messages)
                login_count = result[1] + 1
                cursor.execute("UPDATE login_id SET login_count=?, timestamp=?, message=? WHERE user_id=?", (login_count, datetime.datetime.now(), messages_str, user_id))
            else:
                # Return last 21 messages to user
                messages_str = "\n".join(messages)
                return messages_str
        else:
            # User does not exist in table, insert new data with login count of 1 and new message
            cursor.execute("INSERT INTO login_id (user_id, login_count, timestamp, message) VALUES (?, ?, ?, ?)", (user_id, 1, datetime.datetime.now(), message))
        conn.commit()
    except Exception as e:
        print("Error inserting data into database:", e)
    finally:
        conn.close()