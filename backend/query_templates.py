import re
import random
from collections import defaultdict

# Example SQL templates for various user intents
SQL_TEMPLATES = {
    'select': "SELECT {columns} FROM {table} WHERE {condition};",
    'insert': "INSERT INTO {table} ({columns}) VALUES ({values});",
    'update': "UPDATE {table} SET {column_value_pairs} WHERE {condition};",
    'delete': "DELETE FROM {table} WHERE {condition};"
}

# Example columns and tables for demo purposes
COLUMNS = {
    'users': ['id', 'name', 'email'],
    'orders': ['id', 'user_id', 'product', 'amount']
}

# Example conditions for WHERE clauses
CONDITIONS = [
    "name = 'John'",
    "amount > 100",
    "email LIKE '%@example.com%'"
]

# Generate SQL query based on user input
def generate_sql_query(user_input):
    intent = identify_intent(user_input)
    table = identify_table(user_input)
    
    if intent in SQL_TEMPLATES and table:
        if intent == 'select':
            columns = ', '.join(random.choice(COLUMNS[table]))
            condition = random.choice(CONDITIONS)
            return SQL_TEMPLATES[intent].format(columns=columns, table=table, condition=condition)
        elif intent == 'insert':
            columns = ', '.join(COLUMNS[table])
            values = ', '.join(f"'{value}'" for value in random.sample(['John', 'Doe', 'johndoe@example.com', '100', 'Product A'], len(COLUMNS[table])))
            return SQL_TEMPLATES[intent].format(table=table, columns=columns, values=values)
        elif intent == 'update':
            column_value_pairs = ', '.join(f"{column} = '{random.choice(['John', 'Doe', 'Product A'])}'" for column in COLUMNS[table])
            condition = random.choice(CONDITIONS)
            return SQL_TEMPLATES[intent].format(table=table, column_value_pairs=column_value_pairs, condition=condition)
        elif intent == 'delete':
            condition = random.choice(CONDITIONS)
            return SQL_TEMPLATES[intent].format(table=table, condition=condition)
    return "Unable to generate query."

# Identify user intent (e.g., SELECT, INSERT)
def identify_intent(user_input):
    if 'select' in user_input.lower():
        return 'select'
    elif 'insert' in user_input.lower():
        return 'insert'
    elif 'update' in user_input.lower():
        return 'update'
    elif 'delete' in user_input.lower():
        return 'delete'
    return None

# Identify table based on user input
def identify_table(user_input):
    for table in COLUMNS:
        if table in user_input.lower():
            return table
    return None

# Validate SQL query syntax
def validate_sql_query(query):
    # Basic validation for common SQL keywords
    if re.match(r'^\s*(SELECT|INSERT|UPDATE|DELETE)\s+', query, re.IGNORECASE):
        return True, None
    return False, "Invalid SQL syntax."

# Optimize SQL query (basic optimization examples)
def optimize_sql_query(query):
    # Replace SELECT * with specific columns
    if "SELECT *" in query:
        table = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if table and table.group(1) in COLUMNS:
            columns = ', '.join(COLUMNS[table.group(1)])
            query = re.sub(r'SELECT \*', f'SELECT {columns}', query)
    
    # Remove unnecessary whitespaces
    query = re.sub(r'\s+', ' ', query).strip()
    return query
