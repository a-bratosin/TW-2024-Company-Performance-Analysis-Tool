from flask import Flask, render_template
import numpy as np
from predictors import PredictionModel

app = Flask(__name__)

model = PredictionModel()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict/<string:company>')
def get_by_name(company: str):
    cui = model.find(company)
    if cui:
        return get_by_id(cui, company)
    else:
        return home()

@app.route('/predict/<int:cui>')
def get_by_id(cui: int, name: str = None):
    if name == None:
        name = model.name_of(cui)
    data = model.predict(cui)
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('screener.j.html', name=name, labels=labels, values=values, data=data)

if __name__ == '__main__':
    app.run(debug=True)