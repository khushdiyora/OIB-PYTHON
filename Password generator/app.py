from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password():
    length = int(request.form.get('length', 12))
    complexity = int(request.form.get('complexity', 1))
    password = generate_random_password(length, complexity)
    return jsonify({'password': password})

def generate_random_password(length, complexity):
    characters = string.ascii_letters
    if complexity > 1:
        characters += string.digits
    if complexity > 2:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == '__main__':
    app.run(port=2496, debug=True)
