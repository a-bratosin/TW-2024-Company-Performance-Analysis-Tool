from flask import Flask, render_template
import numpy as np
from predictors import PredictionModel
import scraper
import csv

app = Flask(__name__)

model = PredictionModel()

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/predict/<string:company>')
# def get_by_name(company: str):
#     cui = model.find(company)
#     return get_by_id(cui, company)

@app.route('/predict/<company>')
def get_by_id(company: str):
    url = scraper.get_url_by_search(company)
    raw_data = scraper.scrape_data(url)[0]

    file = open('data_cache.csv','w', newline='')
    writer = csv.writer(file)
    writer.writerow(raw_data[0].keys())
    for row in raw_data:
        writer.writerow(row.values())
    file.close()
    scraper.parse_employees_cache()

    data = model.predict(0)
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('screener.j.html', name=company, labels=labels, values=values, data=data)

if __name__ == '__main__':
    app.run(debug=True)