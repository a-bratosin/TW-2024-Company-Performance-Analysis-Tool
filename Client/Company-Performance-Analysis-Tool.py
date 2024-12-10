from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from ..Model.PredictionModel import PredictionModel

app = Flask(__name__)

model: PredictionModel = joblib.load('../Model/model_obj.pkl')
prediction = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post/<string:company>')
def get_by_name(company):
    cui = model.find(company)
    return get_by_id(cui)

@app.route('/post/<int:cui>')
def get_by_id(cui):
    prediction = model.predict(cui)
    return render_template('screener.html', data=prediction)

if __name__ == '__main__':
    app.run(debug=True)