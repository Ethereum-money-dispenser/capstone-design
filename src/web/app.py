# app.py

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder="templates")

def get_db_connection():
    conn = sqlite3.connect('../crawling/contract_addresses.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_total_pages(rows_per_page, total_rows):
    return (total_rows + rows_per_page - 1) // rows_per_page

@app.route('/', methods=['GET', 'POST'])
def show_contract_addresses():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT network, address, contract_name FROM contract_addresses')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Number assignment
    rows_with_number = [(index + 1, row) for index, row in enumerate(rows)]
    
    keyword = ''
    network = 'all'
    
    # keyword search
    keyword = request.form.get('keyword', '', type=str).lower()
    rows_with_number = [row for row in rows_with_number if keyword in row[1]['contract_name'].lower()]
    
    # network filtering
    network = request.form.get('network', 'all', type=str)
    rows_with_number = [row for row in rows_with_number if network == 'all' or row[1]['network'] == network]
    
    # Pagination
    page = request.form.get('page', 1, type=int)
    rows_per_page = 20
    total_pages = get_total_pages(rows_per_page, len(rows_with_number))
    
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    paginated_rows = rows_with_number[start_index:end_index]
    
    return render_template('main.html', rows_with_number=paginated_rows, total_pages=total_pages, current_page=page, network=network, keyword=keyword)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
    