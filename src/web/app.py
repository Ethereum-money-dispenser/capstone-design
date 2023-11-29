# app.py

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder="templates")

def get_db_connection():
    conn = sqlite3.connect('../crawling/contract_addresses.db')
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT network, address, contract_name FROM contract_addresses')
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

@app.errorhandler(404)
def handing404(error):
    return render_template('404.html')

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
    