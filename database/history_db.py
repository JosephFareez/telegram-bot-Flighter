import sqlite3
import datetime


def db_create(user_id, message, retrieve=False):
    """Функция для создания базы данных"""
    try:
        # Преобразовать user_id в integer
        user_id = int(user_id)

        conn = sqlite3.connect('users_db.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS login_id (user_id INTEGER, login_count INTEGER, timestamp DATETIME, message TEXT);")
        # Проверьте, существует ли user_id уже в таблице
        cursor.execute("SELECT * FROM login_id WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        if result:
            # Пользователь уже существует в таблице
            messages = result[3].split("\n")[-21:]
            if not retrieve:
                # Добавьте новое сообщение к существующим сообщениям и обновите строку
                messages.append(message)
                messages_str = "\n".join(messages)
                login_count = result[1] + 1
                cursor.execute("UPDATE login_id SET login_count=?, timestamp=?, message=? WHERE user_id=?", (login_count, datetime.datetime.now(), messages_str, user_id))
            else:
                # Возвращает пользователю последние 21 сообщение
                messages_str = "\n".join(messages)
                return messages_str
        else:
            # Пользователь не существует в таблице, вставьте новые данные с количеством входов в систему, равным 1, и новое сообщение
            cursor.execute("INSERT INTO login_id (user_id, login_count, timestamp, message) VALUES (?, ?, ?, ?)", (user_id, 1, datetime.datetime.now(), message))
        conn.commit()
    except Exception as e:
        print("Error inserting data into database:", e)
    finally:
        conn.close()
