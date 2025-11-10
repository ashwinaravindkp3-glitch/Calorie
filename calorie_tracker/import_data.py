import pandas as pd
import sqlite3

# Define file paths
DB_FILE = 'calorie_tracker.db'
INDIAN_FOOD_CSV = 'D:\calorie_tracker\Indian_Food_Nutrition_Processed.csv'

def populate_food_library():
    """
    Reads the Indian Food CSV and inserts the data into the food_library table.
    """
    conn = None
    try:
        # 1. Read the CSV file
        df = pd.read_csv(INDIAN_FOOD_CSV)
        print(f"Loaded '{INDIAN_FOOD_CSV}'. Found {len(df)} records to import.")

        # 2. Define the mapping from CSV columns to our database columns
        column_mapping = {
            'Dish Name': 'food_name',
            'Calories (kcal)': 'calories',
            'Protein (g)': 'protein_g',
            'Carbohydrates (g)': 'carbs_g',
            'Fats (g)': 'fat_g'
        }

        # 3. Select and rename the columns we need
        df_to_insert = df[list(column_mapping.keys())].rename(columns=column_mapping)
        
        # Add the user_id for all these initial records
        df_to_insert['user_id'] = 1

        # 4. Connect to the SQLite database
        conn = sqlite3.connect(DB_FILE)
        
        # 5. Use pandas' to_sql() function for an efficient bulk insert
        df_to_insert.to_sql('food_library', conn, if_exists='append', index=False)
        
        print(f"Successfully imported {len(df_to_insert)} records into the 'food_library' table.")

    except FileNotFoundError:
        print(f"Error: The file '{INDIAN_FOOD_CSV}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    populate_food_library()