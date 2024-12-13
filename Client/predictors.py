import numpy as np
import pandas as pd
import math
import seaborn as sns
import matplotlib.pyplot as plt

class PredictionModel:
    def __generate_coeficients__(self, data_file):
        company_data = pd.read_csv(data_file).to_numpy()

        self.previous_data = []
        for row in company_data:
            self.previous_data.append([int(x) for x in row])
        self.previous_data.reverse()
        self.final_year = int(company_data[0, 0])

        df = pd.read_csv(data_file)
        plt.figure(figsize=(8,5))
        sns.heatmap(df.corr(), cbar = False, annot = True)

        middle_year_index = math.floor((company_data.shape[0]) / 2)
        middle_year = int(company_data[middle_year_index][0])

        for i in range(company_data.shape[0]):
            company_data[i][0] = company_data[i][0] - middle_year

        data_points = company_data[:, 1:]
        training_data_count = data_points.shape[0]
        
        data_points = data_points.astype(np.float32)
        data_points[:, 0:-1] = data_points[:, 0:-1] / 1000.0

        years = company_data[:,0]

        A = np.ones((training_data_count, 2))
        A[:,0] = years

        self.coeficients = np.linalg.pinv(A) @ data_points
        self.middle_year = middle_year

    def predict(self, id: int):
        #data_file = '../data_' + f'{id:02}' + '.csv'
        data_file = 'data_cache.csv'
        self.__generate_coeficients__(data_file)

        data = self.previous_data
        for i in range(1, 4):
            desired_year = self.final_year - self.middle_year + i
            estimated_result = self.coeficients[0,:] * desired_year + self.coeficients[1,:]
            estimated_result[0:-1] = estimated_result[0:-1] * 1000.0
            estimated_result = [int(num) for num in estimated_result]
            estimated_result.insert(0, self.final_year + i)
            data.append(estimated_result)

        return data

if __name__ == '__main__':
    model = PredictionModel()
    data = model.predict(9)
    for row in data:
        print(row[0], row[1])