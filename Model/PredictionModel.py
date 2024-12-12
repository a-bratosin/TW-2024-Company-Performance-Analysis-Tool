import joblib
import numpy as np

model = None # TODO train the model

# Dump the trained model into the model_obj.pkl file. It will conserve it as binary data.
joblib.dump(model, 'model_obj.pkl')