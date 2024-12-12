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
original_data = company_data.copy()

company_data = company_data[1:,:]
print(company_data)


# algoritmul practic îmi face regresie liniară pt ani și restul datelor: pt un anumit an, îmi dă statisticile prezise

#primul lucru pe care îl fac este să centrez anii în jurul valorii de mijloc
middle_year_index = math.floor((company_data.shape[0])/2)
middle_year = int(company_data[middle_year_index][0])
print(middle_year)

np.set_printoptions(formatter={'float_kind':'{:f}'.format})

# TODO: să normalizez restul datelor
# (dacă acuratețea este mică, ăsta e primul lucru pe care îl fac
for i in range(company_data.shape[0]):
    #print(x)
    company_data[i][0] = company_data[i][0] - middle_year


print(company_data[:,1:])
print(company_data[:,1:].shape)
# [:,2:] pt a elimina și income-ul (pe care îl voi estima mai târziu)
# dacă chestia cu val proprii nu merge pt determinarea profitului, atunci o să folosesc direct alg ăsta (poate mai pun un coeficient)
data_points = company_data[:,2:]
types_of_data = data_points.shape[1]
training_data_count = data_points.shape[0]
print(types_of_data)
print(training_data_count)

# PAS DE NORMALIZARE
# pt stabilitate numerică, o să împart toți parametrii, în afară de cel de angajați, la 1000
data_points = data_points.astype(np.float32)
data_points[:, 0:-1] = data_points[:, 0:-1]/1000.0
print(data_points)


print(company_data[:,0])
print(company_data[:,0].shape)
years = company_data[:,0]




# aici trebuie să procesez matricile de input pt regresie liniară astfel încât să obțin o matrice 2xk (k fiind numărul de trăsături ale companiei care ne interesează)
# vezi foaia cu demonstația/documentul pe care o să-l scriu despre algoritm (dacă am timp)
# nu știu dacă îmi permite Scikit să fac un calcul de genul; dacă nu, doar fac pseudoinversa


# A - training data matrix for linear regression
A = np.ones((training_data_count, 2))
A[:,0] = years
print("-----------A matrix-------------------------")
print(A)

reg = LinearRegression().fit(A, data_points)
print("----------cu scikit-------------")
print(reg.coef_)


coeficients = np.linalg.pinv(A)@data_points
print("----------cu pseudoinversa-------------")
print(coeficients)




desired_year = 2023 - middle_year
estimated_result = coeficients[0,:]*desired_year + coeficients[1,:]

estimated_result[0:-1] = estimated_result[0:-1]*1000.0


print("---------rezultatul estimat pt 2023------------")
print(np.floor(estimated_result))

print("\n-------------rezultatul real pt 2023-----------")
print(original_data[0,2:])

print("\n--------------diferența-------------------")
print(np.abs(original_data[0,2:]-np.floor(estimated_result)))

"""
reg = LinearRegression().fit(X,y)
print(reg.coef_)

reg.predict(desired_year)
"""



