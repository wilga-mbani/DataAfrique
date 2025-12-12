from fastapi import FastAPI 
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


# creation de l'API

app= FastAPI()

# importation du model

def load():
    model_path = "./defautCredit.joblib"
    model = joblib.load(model_path)
        
    return model

# lecture du model
model= load()


# First root
@app.get("/")
def api_info():
    return {"info": "Bienvenue"}

# second root
class ChurnInput(BaseModel):
    Time:float
    V1:float
    V2:float
    V3:float
    V4:float
    V5:float
    V6:float
    V7:float
    V8:float
    V9:float
    V10:float
    V12:float
    V14:float
    V16:float
    V17:float
    V18:float
    V19:float
    V20:float
    V21:float
    V23:float
    V24:float
    V25:float
    V26:float
    V27:float
    V28:float
    Amount:float
    

#
@app.post("/predict")
async def predict(input_data: ChurnInput):
   
    data_df = pd.DataFrame([input_data.model_dump()])
    
    #Prédiction
    pred = int(model.predict(data_df)[0])
    
    return {
        "prediction":pred
    }
   



    
    