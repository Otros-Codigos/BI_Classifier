"""
    Santiago Bobadilla
    Juan José Beltrán
    PIPELINE
"""

# Librerias
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from joblib import load, dump

# PIPELINE COMPLETO
class Model:

    # Contructor ~ Inicialmente no existe modelo. 
    # Es decir, se debe o cargar o crear.
    def __init__(self):
        self.model = None


    # Crear el modelo.
    def create(self):

        # TODO PARAMETES

        # Creación del PipeLine
        self.model = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                            ])

        # Guardar el modelo para futuras ocaciones.
        dump(self.model, 'Model/modelo.joblib')

        # Reportar que el modelo fue creado.
        print("PipeLine Creado")


    # Cargar el modelo.
    def charge(self):

        # Si ya se creo uno en una ocación pasada, este se carga.
        self.model = load("Model/modelo.joblib")

        # Se reporta que el modelo fue cargado y NO creado.
        print("PipeLine Cargado")


    # Ajustar el modelo
    def fit(self, X, Y):
        self.model.fit(X,Y)


    # Predecir Y
    def make_predictions(self, data):
        return self.model.predict(data)

    
    # Guardar el modelo
    def save(self):
        dump(self.model, 'Model/modelo.joblib')