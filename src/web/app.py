# app.py

from flask import Flask, render_template, request
import sqlite3
import hashlib

def init_vuln_db():
    # initialize vulnerabilities.db
    conn = sqlite3.connect('../databases/vulnerabilities.db')
    cursor = conn.cursor()

    # create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            contract_address TEXT NOT NULL,
            vuln_file BLOB NOT NULL
        )'''
    )

    conn.commit()
    conn.close()
    
init_vuln_db()

app = Flask(__name__, template_folder="templates")
members = []

def get_address_db_connection():
    conn = sqlite3.connect('../databases/contract_addresses.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_vulnerabilities_db_connection():
    conn = sqlite3.connect('../databases/vulnerabilities.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/tables', methods=['GET', 'POST'])
def show_contract_addresses():
    conn = get_address_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT network, address, contract_name, similar FROM contract_addresses')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Number assignment
    rows_with_number = [(index + 1, row) for index, row in enumerate(rows)]
    
    network = 'all'
    if request.method == 'POST':
        # network filtering
        network = request.form.get('network', 'all', type=str)
        rows_with_number = [row for row in rows_with_number if network == 'all' or row[1]['network'] == network]
    
    return render_template('tables.html', rows_with_number=rows_with_number, network=network)

@app.route('/users-receiving', methods=['GET', 'POST'])
def users_receiving():
    if request.method == 'GET':
        return render_template('users-receiving.html')
    else:
        userid: str = request.form.get('userid', type=str)
        # check if userid is valid
        if not userid or userid[:8] != 'capstone':
            return render_template('error.html', error_code='Invalid userid')
        # check if userid is new
        if userid not in members: 
            members.append(userid)
            
        # get list from DB
        conn = get_address_db_connection()
        cursor = conn.cursor()
        number = int(str(int(userid[-3:])))
        # print(number)
        cursor.execute('SELECT network, address, contract_name FROM contract_addresses WHERE network = "etherscan.io" AND similar = address AND id % 40 = ?;',(number,))
        rows = cursor.fetchall()
        # print(rows)
        conn.close()
    
        # Number assignment
        rows_with_number = [(index + 1, row) for index, row in enumerate(rows)]
        rows_with_number = [row for row in rows_with_number if row[0] % len(members) == members.index(userid)]
           
        return render_template('users-receiving.html', rows_with_number=rows_with_number)

@app.route('/users-sending')
def users_sending():
    return render_template('users-sending.html')

@app.errorhandler(404)
def handing404(error):
    return render_template('404.html')

@app.route('/insertion', methods=['POST'])
def insert_row():
    contract_address = request.form.get('contract_address', type=str)
    vuln_file = request.files['vuln-file']
    userid = request.form.get('userid', type=str)
    password = request.form.get('password', type=str)
    
    if not contract_address or not vuln_file or not userid or not password:
        return render_template('error.html', error_code='all fields are required')
    
    contract_address = contract_address.strip()
    userid = userid.strip()
    password = password.strip()
    
    # Check contract address in DB
    conn = get_address_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contract_addresses WHERE address=?', (contract_address,))
    row = cursor.fetchone()
    
    conn.close()
    
    if not row:
        return render_template('error.html', error_code='contract address not found')
    
    # Check userid and password
    if userid[:8] != 'capstone':
        return render_template('error.html', error_code='Invalid userid')
    
    userid_hash = userid + '1234567890'
    userid_hash = hashlib.sha256(userid_hash.encode()).hexdigest()
    
    if userid_hash != password:
        return render_template('error.html', error_code='Invalid password')
    
    # Add row to DB
    conn = get_vulnerabilities_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO vulnerabilities (user_id, contract_address, vuln_file) VALUES (?, ?, ?)', (userid, contract_address, vuln_file))
    
    conn.commit()
    conn.close()
    
    return render_template('success.html')

# @app.route('/<network>/<address>')
# def show_contract(network, address):
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute('SELECT * FROM contract_addresses WHERE network=? AND address=?', (network, address))
#     row = cursor.fetchone()
    
#     conn.close()
    
#     return render_template('contract.html', row=row)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
    