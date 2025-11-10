import sqlite3

def initialize_database():
    """Creates the database and all necessary tables with their full schema."""
    conn = None
    try:
        conn = sqlite3.connect('calorie_tracker.db')
        cursor = conn.cursor()

        # Create 'users' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                daily_calorie_goal INTEGER NOT NULL,
                daily_protein_goal INTEGER,
                daily_carbs_goal INTEGER,
                daily_fat_goal INTEGER
            )
        ''')
        print("Table 'users' is ready.")

        # Create 'food_log' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_date TEXT NOT NULL,
                quantity REAL NOT NULL, 
                food_name TEXT NOT NULL,
                calories INTEGER NOT NULL,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL
            )
        ''')
        print("Table 'food_log' is ready.")

        # Create 'food_library' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_library (
                food_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                food_name TEXT NOT NULL,
                calories INTEGER NOT NULL,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                UNIQUE (user_id, food_name)
            )
        ''')
        print("Table 'food_library' is ready.")
        
        # Add a default user IF one doesn't exist
        cursor.execute("SELECT * FROM users WHERE user_id = 1")
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (user_id, username, daily_calorie_goal) 
                VALUES (1, 'default_user', 2000)
            ''')
            print("Default user with a 2000 calorie goal has been added.")

        conn.commit()
        print("Database has been successfully initialized.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    initialize_database()