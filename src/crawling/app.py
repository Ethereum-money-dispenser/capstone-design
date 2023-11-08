from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder="templates")
app.debug = True

def get_db_connection():
    conn = sqlite3.connect('contract_addresses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def show_contract_addresses():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT network, address, contract_name FROM contract_addresses')
    rows = cursor.fetchall()
    
    conn.close()
    
    # 번호 할당
    rows_with_number = [(index + 1, row) for index, row in enumerate(rows)]
    
    return render_template('main.html', rows_with_number=rows_with_number)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
