from flask import Flask, request, jsonify
from query_templates import generate_sql_query, validate_sql_query, optimize_sql_query
import sqlite3
import os

app = Flask(__name__)

# Initialize in-memory database for demonstration
DATABASE = 'example.db'

# Create the SQLite database if it doesn't exist
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Example schema
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product TEXT NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        conn.close()

# Initialize database
init_db()

# Helper function to execute SQL queries
def execute_query(query):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        results = cursor.fetchall()
        conn.close()
        return results, None
    except Exception as e:
        return None, str(e)

# Endpoint to handle SQL query generation
@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.json.get('input')
    sql_query = generate_sql_query(user_input)
    return jsonify({"query": sql_query})

# Endpoint to handle SQL query validation
@app.route('/validate', methods=['POST'])
def validate():
    query = request.json.get('query')
    is_valid, error = validate_sql_query(query)
    return jsonify({"is_valid": is_valid, "error": error})

# Endpoint to handle SQL query execution
@app.route('/execute', methods=['POST'])
def execute():
    query = request.json.get('query')
    results, error = execute_query(query)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"results": results})

# Endpoint to handle SQL query optimization
@app.route('/optimize', methods=['POST'])
def optimize():
    query = request.json.get('query')
    optimized_query = optimize_sql_query(query)
    return jsonify({"optimized_query": optimized_query})

# Endpoint to explore database schema
@app.route('/schema', methods=['GET'])
def schema():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Retrieve table information
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema_info[table_name] = [{"column": col[1], "type": col[2]} for col in columns]
    
    conn.close()
    return jsonify(schema_info)

if __name__ == '__main__':
    app.run(debug=True)
