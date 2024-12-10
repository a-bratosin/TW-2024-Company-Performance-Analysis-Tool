from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# model = joblib.load('../Model/model_obj.pkl')
prediction = None

@app.route('/')
def home():
    return render_template('index.html')

def screener(data):
    print("PING")
    return render_template('screener.html', data=data)

@app.route('/post/<string:company>')
def get_by_name(company):
    # prediction = model.predict(model.find(company))
    return screener(prediction)

@app.route('/post/<int:cui>')
def get_by_id(cui):
    # prediction = model.predict(cui)
    return screener(prediction)

if __name__ == '__main__':
    app.run(debug=True)