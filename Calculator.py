from flask import Flask,request
from flask import jsonify
import psycopg2
import math
import os
app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL") or "dbname=calculator"

conn = psycopg2.connect(database_url)


def save_data(operation, first_number, second_number, result):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO calculations (operation, first_number, second_number, result, created_at) VALUES (%s, %s, %s, %s, NOW())", (operation, first_number, second_number, result))
        conn.commit()
    except:
        conn.rollback()
    finally:
        cur.close()


def entered_number(a, b):

    if a is not None:
        return a

    if b is not None:
        return b


def convert_to_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def square_root(a):
    return math.sqrt(a)


def divide(a, b):
    return a / b


def subtract(a, b):
    return a - b


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def perform_operation(operation, operation_name, uses_single_number = False):
    a = convert_to_int(request.args.get('a'))
    b = convert_to_int(request.args.get('b'))
    if (b is None or a is None) and not uses_single_number:
        return 'A NUMBER', 400
    else:
        result = None
        if uses_single_number:
            single_number = entered_number(a, b)
            if a is not None and b is not None:
                return 'Please enter one number.', 400

            if single_number is None:
                return 'Enter a number please', 400

            result = operation(single_number)
        else:
            result = operation(a, b)

        output = {'result': result,
                        'a': a,
                        'b': b
                        }
        print(output['result'])
        if uses_single_number:
            save_data(operation_name, entered_number(a, b), None, output['result'])
        else:
            save_data(operation_name, a, b, output['result'])
        return jsonify(output)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/square_root')
def square_root_endpoint():
    a = convert_to_int(request.args.get('a'))
    b = convert_to_int(request.args.get('b'))
    number = entered_number(a, b)

    if number is not None and number < 0:
        return 'Please don\'t enter a negative number', 400
    return perform_operation(square_root, 'square_root', True)

@app.route('/divide')
def divide_endpoint():
    b = convert_to_int(request.args.get('b'))
    if b == 0:
        return 'Please don\'t enter 0 for b!', 400
    return perform_operation(divide, 'divide')

@app.route('/subtract')
def subract_endpoint():
    return perform_operation(subtract, 'subtract')

@app.route('/multiply')
def multiply_endpoint():
    return perform_operation(multiply, 'multiply')

@app.route('/add')
def add_endpoint():
    return perform_operation(add, 'add')

if __name__ == '__main__':
    app.run(use_reloader=True, port=8000)

