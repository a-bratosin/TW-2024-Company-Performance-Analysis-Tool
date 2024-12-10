from flask import Flask, request, jsonify
import requests
import json

target_url = ''
parser_url = ''

app = Flask(__name__)

@app.route('/get_page', methods=['POST'])
def get_page():
    req = request.json
    # page = requests.get(target_url)
    # req = requests.post(parser_url)
    return jsonify({"msg": "Page successfully scrapped!"})

@app.route('/start', methods=['GET'])
def start():
    # TODO parse requests
    return jsonify({"msg": "Scraping successfully finished!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)