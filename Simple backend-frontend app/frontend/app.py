import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BACKEND_URL = 'http://backend-service:5000'

@app.route('/', methods=['POST'])
def forward_request():
    data = request.json
    try:
        response = requests.post(BACKEND_URL, json=data)
        return jsonify({
            'frontend_response': "Frontend successfully forwarded",
            'backend_response': response.json()
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
