import sqlite3
import os

DATABASE = 'example.db'

class DatabaseManager:
    def __init__(self, db_path=DATABASE):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """Close the connection to the SQLite database."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=None):
        """Execute a SQL query with optional parameters."""
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            results = self.cursor.fetchall()
            return results, None
        except sqlite3.Error as e:
            return None, str(e)
        finally:
            self.disconnect()

    def initialize_database(self):
        """Initialize the database with example tables and data."""
        if not os.path.exists(self.db_path):
            self.connect()
            self._create_tables()
            self._seed_data()
            self.disconnect()

    def _create_tables(self):
        """Create example tables in the SQLite database."""
        users_table = '''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        '''
        orders_table = '''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product TEXT NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''
        self.cursor.execute(users_table)
        self.cursor.execute(orders_table)

    def _seed_data(self):
        """Insert example data into the SQLite database."""
        users_data = [
            ('Alice', 'alice@example.com'),
            ('Bob', 'bob@example.com'),
            ('Charlie', 'charlie@example.com')
        ]
        orders_data = [
            (1, 'Laptop', 1200),
            (2, 'Smartphone', 800),
            (3, 'Headphones', 150),
            (1, 'Monitor', 300)
        ]
        self.cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)
        self.cursor.executemany("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)", orders_data)

    def fetch_all_users(self):
        """Fetch all users from the database."""
        query = "SELECT * FROM users"
        return self.execute_query(query)

    def fetch_orders_by_user(self, user_id):
        """Fetch all orders for a specific user."""
        query = "SELECT * FROM orders WHERE user_id = ?"
        return self.execute_query(query, (user_id,))

    def fetch_schema(self):
        """Fetch the database schema."""
        self.connect()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        schema = {}
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            schema[table_name] = [{"column": col[1], "type": col[2]} for col in columns]
        self.disconnect()
        return schema

    def drop_database(self):
        """Drop the database by deleting the file."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def reset_database(self):
        """Reset the database by re-initializing it."""
        self.drop_database()
        self.initialize_database()

# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager()

    # Initialize the database
    db_manager.initialize_database()

    # Fetch all users
    users, error = db_manager.fetch_all_users()
    if error:
        print(f"Error fetching users: {error}")
    else:
        print("Users:", users)

    # Fetch orders by user ID
    orders, error = db_manager.fetch_orders_by_user(1)
    if error:
        print(f"Error fetching orders: {error}")
    else:
        print("Orders for user 1:", orders)

    # Fetch the database schema
    schema = db_manager.fetch_schema()
    print("Database Schema:", schema)
