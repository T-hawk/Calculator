from flask import Flask,request
from flask import jsonify
app = Flask(__name__)

def convert_to_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

def divide(a, b):
    return a / b

def subtract(a, b):
    return a - b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def perform_operation(operation):
    a = convert_to_int(request.args.get('a'))
    b = convert_to_int(request.args.get('b'))
    if a is None or b is None:
        return 'A NUMBER', 400
    else:
        output = {'result': operation(a, b),
                        'a': a,
                        'b': b
                        }
        print(output['result'])
        return jsonify(output)

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

