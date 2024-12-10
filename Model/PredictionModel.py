import joblib
import numpy as np

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