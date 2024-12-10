from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# model = joblib.load('')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post/<company>')
def get_by_name(company):
    # TODO return company data by name
    return

@app.route('/post/<int:cui>')
def get_by_id(cui):
    # TODO return company data by cui
    return

if __name__ == '__main__':
    app.run(debug=True)