import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint vulnerável a SQL injection
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    
    cursor.execute(query)
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return "Login successful!"
    else:
        return "Invalid credentials!"


@app.route('/search', methods=['GET'])
def search_user():
    """
    Outro endpoint vulnerável a SQL injection
    """
    search_term = request.args.get('q')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = f"SELECT id, name, email FROM users WHERE name LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.close()
    
    return str(results)


@app.route('/delete_user', methods=['POST'])
def delete_user():
    """
    Endpoint vulnerável com comando DELETE
    """
    user_id = request.form.get('user_id')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = "DELETE FROM users WHERE id = " + str(user_id)
    
    cursor.execute(query)
    conn.commit()
    conn.close()
    
    return "User deleted!"


if __name__ == '__main__':
    app.run(debug=True)
