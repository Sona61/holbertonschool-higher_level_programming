from flask import Flask, render_template, request
import json
import csv
import sqlite3

app = Flask(__name__)


def read_json_file():
    with open('products.json', 'r') as file:
        return json.load(file)


def read_csv_file():
    products = []
    with open('products.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['price'] = float(row['price'])
            products.append(row)
    return products


def read_sql_database():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, price FROM Products')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.route('/products')
def products():
    source = request.args.get('source')
    product_id = request.args.get('id')

    try:
        if source == 'json':
            products = read_json_file()
        elif source == 'csv':
            products = read_csv_file()
        elif source == 'sql':
            products = read_sql_database()
        else:
            return render_template('product_display.html', error='Wrong source')

        if product_id:
            product_id = int(product_id)
            products = [p for p in products if p['id'] == product_id]

            if not products:
                return render_template(
                    'product_display.html',
                    error='Product not found'
                )

        return render_template('product_display.html', products=products)

    except Exception:
        return render_template('product_display.html', error='Database error')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
