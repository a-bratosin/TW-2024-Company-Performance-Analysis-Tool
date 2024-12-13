from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import scipy as sp

app = Flask(__name__)

class PredictionModel:
    def find(self, name: str) -> int:
        return 0

    def predict(self, id: int):
        data = [
            (2016, 123),
            (2017, 293),
            (2018, 141)
        ]
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
    name = 'Enel'
    data = model.predict(cui)
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('screener.j.html', name=name, labels=labels, values=values)

if __name__ == '__main__':
    app.run(debug=True)