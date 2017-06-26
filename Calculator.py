from flask import Flask,request
from flask import jsonify
import math
app = Flask(__name__)

def convert_to_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

def sqaure_root(a, _):
    return math.sqrt(a)

def divide(a, b):
    return a / b

def subtract(a, b):
    return a - b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def perform_operation(operation, uses_single_number = False):
    a = convert_to_int(request.args.get('a'))
    b = convert_to_int(request.args.get('b'))
    if a is None or (b is None and not uses_single_number):
        return 'A NUMBER', 400
    else:
        output = {'result': operation(a, b),
                        'a': a,
                        'b': b
                        }
        print(output['result'])
        return jsonify(output)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/square_root')
def square_root():
    a = convert_to_int(request.args.get('a'))
    if a < 0:
        return 'Please don\'t enter a negative number', 400
    return perform_operation(sqaure_root, True)



@app.route('/divide')
def divide_endpoint():
    b = convert_to_int(request.args.get('b'))
    if b == 0:
        return 'Please don\'t enter 0 for b!', 400
    return perform_operation(divide)

@app.route('/subtract')
def subract_endpoint():
    return perform_operation(subtract)

@app.route('/multiply')
def multiply_endpoint():
    return perform_operation(multiply)

@app.route('/add')
def add_endpoint():
    return perform_operation(add)

if __name__ == '__main__':
    app.run(use_reloader=True, port=8000)

