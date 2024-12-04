from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_request():
    data = request.json
    message = data.get('message', 'No message received')
    return jsonify({'response': f'Backend received: {message}'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
