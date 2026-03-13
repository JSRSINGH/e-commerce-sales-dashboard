import pandas as pd
import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
SQL_DIR = os.path.join(BASE_DIR, 'sql')
DB_PATH = os.path.join(PROCESSED_DIR, 'ecommerce.db')

def load_csv_to_db():
    """Loads the cleaned CSV into a SQLite database."""
    csv_path = os.path.join(PROCESSED_DIR, 'ecommerce_cleaned.csv')
    
    if not os.path.exists(csv_path):
        logging.error(f"Cleaned CSV not found at {csv_path}. Run data_prep.py first.")
        return False
        
    logging.info("Reading cleaned CSV...")
    df = pd.read_csv(csv_path)
    
    logging.info(f"Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    logging.info("Writing data to SQLite table 'sales'...")
    # Write the dataframe to a SQLite table; replace it if it exists
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count FROM sales")
    count = cursor.fetchone()['count']
    logging.info(f"Successfully loaded {count} rows into 'sales' table.")
    
    conn.close()
    return True

def run_sql_file():
    """Executes the queries in queries.sql to verify the data."""
    if not os.path.exists(DB_PATH):
        logging.error("Database not found. Run load_csv_to_db first.")
        return
        
    query_file = os.path.join(SQL_DIR, 'queries.sql')
    if not os.path.exists(query_file):
        logging.error(f"SQL file not found at {query_file}")
        return
        
    with open(query_file, 'r') as f:
        sql_script = f.read()
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    logging.info("Executing sample SQL queries...")
    
    # SQLite executing script gets tricky with returning results for multiple statements, 
    # so we'll just demonstrate executing one by one if they are separated by semicolon.
    # For now, let's just run them and print the first few rows of the first query to verify.
    # Or to make it robust, we execute each statement individually using pandas:
    
    statements = [s.strip() for s in sql_script.split(';') if s.strip()]
    
    for i, statement in enumerate(statements):
        try:
            # We use pandas to easily display the result of the query
            result_df = pd.read_sql_query(statement, conn)
            logging.info(f"\n--- Query {i+1} Result (Top 5 Rows) ---")
            print(result_df.head(5))
            print("-" * 40)
        except Exception as e:
            logging.error(f"Error executing query {i+1}: {e}")
            logging.error(f"Query: {statement[:100]}...")
            
    conn.close()

def main():
    if load_csv_to_db():
        run_sql_file()

if __name__ == "__main__":
    main()
