from flask import Flask, jsonify, request
from cryptography.fernet import Fernet

app = Flask(__name__)

tokens = {}

@app.route("/")
def index():
    return "Hola Mundo!"

@app.route("/generate_token", methods=['GET'])
def generate_token():
    key = Fernet.generate_key()
    cipher = Fernet(key)
    token = cipher.encrypt(key).decode()
    tokens[token] = {'cipher': cipher, 'active': True}
    return jsonify({'token': token})

@app.route("/validate_token", methods=['POST'])
def validate_token():
    token = request.json.get('token')
    if token in tokens and tokens[token]['active']:
        return jsonify({'valid': True})
    return jsonify({'valid': False})

@app.route("/deactivate_token", methods=['POST'])
def deactivate_token():
    token = request.json.get('token')
    if token in tokens:
        tokens[token]['active'] = False
        return jsonify({'status': 'Token deactivated'})
    return jsonify({'error': 'Invalid token'})

@app.route("/encrypt", methods=['POST'])
def encrypt():
    token = request.json.get('token')
    text = request.json.get('text')
    if token not in tokens or not tokens[token]['active']:
        return jsonify({'error': 'Invalid or inactive token'}), 403
    cipher = tokens[token]['cipher']
    encrypted_text = cipher.encrypt(text.encode()).decode()
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/decrypt", methods=['POST'])
def decrypt():
    token = request.json.get('token')
    encrypted_text = request.json.get('encrypted_message')
    if token not in tokens or not tokens[token]['active']:
        return jsonify({'error': 'Invalid or inactive token'}), 403
    cipher = tokens[token]['cipher']
    decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
    return jsonify({'decrypted_message': decrypted_text})

if __name__ == "__main__":
    app.run(debug=True)
