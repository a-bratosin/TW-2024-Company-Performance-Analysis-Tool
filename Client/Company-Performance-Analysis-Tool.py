from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import scipy as sp

app = Flask(__name__)

class PredictionModel:
    def find(self, name: str) -> int:
        return 0

    def predict(self, id: int):
        data = {
            'name': 'Enel'
        }
        return data

model = PredictionModel()

# model = joblib.load('../Model/model_obj.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict/<string:company>')
def get_by_name(company: str):
    cui = model.find(company)
    return get_by_id(cui)

@app.route('/predict/<int:cui>')
def get_by_id(cui: int):
    prediction = model.predict(cui)
    return render_template('screener.html', **prediction)

if __name__ == '__main__':
    app.run(debug=True)