from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    soup = BeautifulSoup(data, 'html.parser')

    with open('page.html', 'w') as file:
        file.write(soup.prettify())
    
    # TODO parse page data
    
    return jsonify({'msg': "Page was parsed!"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)