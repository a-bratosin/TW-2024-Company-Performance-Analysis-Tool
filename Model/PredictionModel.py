import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import math

data_file = 'Model/data_sample.csv'

# Interface used by client to fetch predictions. Feel free to add any other members, don't remove find and predict.
class PredictionModel:
    def find(name: str):
        # Find company's CUI by name, if possible
        pass
    
    def predict(cui: int):
        # Return a packet with all relevant data about the company. Any datastructure you want.
        pass

model = PredictionModel() # TODO train the model

# Dump the trained model into the model_obj.pkl file. It will conserve it as binary data.
joblib.dump(model, 'model_obj.pkl')


# citesc datele cu pandas, apoi le convertesc în numpy ptc îmi este mult mai ușor așa să lucrez cu linii și coloane
company_data = pd.read_csv(data_file).to_numpy()
#primul lucru pe care îl fac este să centrez anii în jurul valorii de mijloc
middle_year_index = math.floor((company_data.shape[0])/2)
middle_year = int(company_data[middle_year_index][0])
print(middle_year)

# TODO: să normalizez restul datelor
# (dacă acuratețea este mică, ăsta e primul lucru pe care îl fac
for i in range(company_data.shape[0]):
    #print(x)
    company_data[i][0] = company_data[i][0] - middle_year

print(company_data[:,1:])
print(company_data[:,1:].shape)
X = company_data[:,1:]

print(company_data[:,0])
print(company_data[:,0].shape)
y = company_data[:,0]

reg = LinearRegression().fit(X,y)
print(reg.coef_)
#print(date_firma.head())
#print(date_firma["Year"][3])