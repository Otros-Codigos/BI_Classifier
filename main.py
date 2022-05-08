
from fastapi import FastAPI, Request, File, UploadFile
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from Data.Model import ListDataModel, all_name
from Data.Words import preprocessing, stem_and_lemmatize
from Model.model import Model

import nltk
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from nltk import word_tokenize
import pandas as pd
import contractions
import numpy as np
from pathlib import Path
import json



app = FastAPI()
templates = Jinja2Templates(directory="Html")

app.mount(
    "/Html",
    StaticFiles(directory=Path(__file__).parent.absolute() / "Html"),
    name="static",
)

# incializar el PipeLine
model = Model()

# Por defecto siempre intentar cargar si ya hay un modelo
try:
   model.charge()

# En dado caso de que no exista, se crea un nuevo modelo (pipeline)
except Exception:
   model.create()


# -------------------------------------------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def write_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------------------------------------------------------------------------------

@app.post("/train")
def make_training(data: ListDataModel):
   
   # Crea un DataFrame vacio con los nombres de la columnas en el orden en el que le van a llegar Y y X.
   df = pd.DataFrame(columns=data.data[0].dict().keys())

   # Del Body que llega por HTTP se cargan todos los registros en la tabla.
   for d in data.data:
      new_row = pd.DataFrame(d.dict(), columns=d.dict().keys(), index=[0])
      df = pd.concat([new_row, df]).reset_index(drop = True)

   # Se ajustan los nombres de las columnas.
   df.columns = all_name()
   data = df

   X = data.drop(['problems_described'], axis=1)
   Y = data['problems_described']
   Y = Y.astype('int')

   rus = RandomUnderSampler(random_state=42)
   data['medical_abstracts'], data['problems_described'] = rus.fit_resample(X, Y)
   data.dropna(inplace = True)

   # Se separan las variables de respuesta Y y las explicativas X
   data['medical_abstracts'] = data['medical_abstracts'].astype(object)
   data['problems_described'] = data['problems_described'].astype(int)

   data['medical_abstracts'] = data['medical_abstracts'].apply(contractions.fix)
   data['medical_abstracts'] = data['medical_abstracts'].apply(word_tokenize).apply(preprocessing)
   data['medical_abstracts'] = data['medical_abstracts'].apply(stem_and_lemmatize)
   data['medical_abstracts'] = data['medical_abstracts'].apply(lambda x: ' '.join(map(str, x)))

   X_data, y_data = data['medical_abstracts'], data['problems_described']
   X_train, X_test, Y_train, Y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)

   # Se ajusta el modelo.
   model.fit(X_train, Y_train)
   model.save()

   # Se calcula las metricas.
   y = model.make_predictions(X_test)
   r = np.mean(Y_test == y)

   d = {'Words': X_test, 'PredictedClass': y, 'ActualClass':Y_test}
   respuesta = pd.DataFrame(data=d)

   respuesta.loc[respuesta.PredictedClass != respuesta.ActualClass, "ActualClass"] = np.nan
   respuesta.dropna(inplace = True)

   wordsByClass = {i: {} for i in range(1,6)}
   #for i in range(len(respuesta['Words'])):
   for i in respuesta.index:
     auxWords = respuesta['Words'][i].split(" ")
     diagnose = respuesta['PredictedClass'][i]
     for word in auxWords:
       wordsByClass[diagnose][word] = 0

     for word in auxWords:
       wordsByClass[diagnose][word] += 1

   diagnoseList = []
   wordList = []
   valuesList = []

   for diagnose in wordsByClass:
     for word in wordsByClass[diagnose]:
       diagnoseList.append(diagnose)
       wordList.append(word)
       valuesList.append(wordsByClass[diagnose][word])

   results = {'Diagnose': diagnoseList, 'Word': wordList, 'Occurrences':valuesList}
   resultsDf = pd.DataFrame(data=results)
   resultsDf.sort_values(by=['Occurrences'])

   resultsDf.to_json("Data/results.json", orient="records")
   return json.loads(resultsDf.to_json(orient="records"))

# -----------------------------------------------------------------------------------------------------------------------

@app.get("/data")
def write_home():
   data = pd.read_json("Data/results.json")
   return json.loads(data.to_json(orient="records"))

# -----------------------------------------------------------------------------------------------------------------------

@app.post("/predict")
async def handle_form(request: Request, assignment_file: UploadFile = File(...), response_class=HTMLResponse):

    data = await assignment_file.read()
    info = {"medical_abstracts": data.decode("utf-8")}
    data = pd.DataFrame(info, index=[0])
    
    data['medical_abstracts'] = data['medical_abstracts'].apply(contractions.fix)
    data['medical_abstracts'] = data['medical_abstracts'].apply(word_tokenize).apply(preprocessing)
    data['medical_abstracts'] = data['medical_abstracts'].apply(stem_and_lemmatize)
    data['medical_abstracts'] = data['medical_abstracts'].apply(lambda x: ' '.join(map(str, x)))

    try:
      return templates.TemplateResponse("index.html", {"request": request, "message": sickness(int(model.make_predictions(data)[0]))})


    except Exception:

      df = pd.read_json("Data/data.json")
      df.columns = all_name()

      X = df.drop(['problems_described'], axis=1)
      Y = df['problems_described']
      Y = Y.astype('int')
   
      rus = RandomUnderSampler(random_state=42)
      df['medical_abstracts'], df['problems_described'] = rus.fit_resample(X, Y)
      df.dropna(inplace = True)
   
      # Se separan las variables de respuesta Y y las explicativas X
      df['medical_abstracts'] = df['medical_abstracts'].astype(object)
      df['problems_described'] = df['problems_described'].astype(int)
   
      df['medical_abstracts'] = df['medical_abstracts'].apply(contractions.fix)
      df['medical_abstracts'] = df['medical_abstracts'].apply(word_tokenize).apply(preprocessing)
      df['medical_abstracts'] = df['medical_abstracts'].apply(stem_and_lemmatize)
      df['medical_abstracts'] = df['medical_abstracts'].apply(lambda x: ' '.join(map(str, x)))
   
      X_data, y_data = df['medical_abstracts'], df['problems_described']
      X_train, X_test, Y_train, Y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)
   
      # Se ajusta el modelo.
      model.fit(X_train, Y_train)
      model.save()
      print("Model Pre-Update")

      return templates.TemplateResponse("index.html", {"request": request, "message": sickness(int(model.make_predictions(data)[0]))})


# ------------------------------------------------

def sickness(id):

   if id == 1: return "Neoplasias"
   elif id == 2: return "Sistema Digestivo"
   elif id == 3: return "Sistema Nervioso"
   elif id == 4: return "Cardiovasculares"
   else: return "Patológicas Generales"