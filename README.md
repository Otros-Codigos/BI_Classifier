# BI - Etapa 2 Proyecto 1

* Santiago Bobadilla - 201820728
* Juan José Beltrán Ruiz - 201819446

---

### Introducción

La Analítica de Textos (AT) es un campo interdisciplinario que conjuga el machine learning (aprendizaje de máquina) y el Procesamiento de Lenguaje Natural, y que tiene como objetivo procesar de manera automática grandes cantidades de textos para la extracción de conocimiento que apoye la toma de decisiones.

La medicina no es la excepción, partiendo de descripciones dispuestas por los médicos se puede establecer de manera automática la categorización de ciertas enfermedades. Con tal fin, buscamos presentar a continuación tecnología de asistencia que puede identificar, con alta precisión, la clase de problemas descritos en la descripción del médico.

### Comprensión del negocio y enfoque analítico

Los resúmenes médicos describen las condiciones actuales de un paciente. Los médicos rutinariamente escanean docenas o cientos de resúmenes cada día mientras hacen sus rondas en un hospital y deben recoger rápidamente la información saliente que apunta a la enfermedad del paciente.

Buscamos automatizar (como herramienta de ayuda en la toma de decisiones) un identificador de alta precisión para la clase de problemas descritos en el resumen. Se cuenta resúmenes de 5 condiciones diferentes: enfermedades del sistema digestivo, enfermedades cardiovasculares, neoplasias, enfermedades del sistema nervioso y condiciones patológicas generales. 

### Usuario

Medico con poco tiempo y bastantes pacientes que necesite una primera herramienta de apoyo a la toma de decisión para empezar a diagnosticas la enfermedad que tiene el paciente. 

### Objetivo general

Ayudar al proceso de diagnóstico médico por medio de algoritmos de clasificación basados en información histórica de resúmenes de diferentes pacientes. 

### Objetivos Específicos

*   Entregar al negocio un modelo que permita clasificar a un nuevo paciente dado el informe del médico que lo trató.
*   Visualizar la información más relevante con la cual se llego a saber que posible enfermedad tiene dicho paciente.  
*   API desplegado de facil uso que las funcionalidades requeridas.

### Importancia

Usar el API en primera mano *SOLO* como herreamienta de apoyo a la decisión. Si la clasificación es 1 a 4, se considera confiable. No obstante, revisar las clasificadas como categoría 5. Dado que al tener una categoria amplia no suele ser muy preciso. 

Si bien será de gran ayuda, de manera general, usar esta modelo solo como recomendaciones y herramienta de apoyo a la decisión. Lo que se sugiere no es verdad absoluta y vale la pena tener una segunda forma de revisión.

---

## Carpetas

1. *Data*: Contiene un archivo **.json** con la información utilizada para hacer *fit* al modelo. Dicha información es la misma que se pasa en *Postman*. Esta información esta definida de manera predeterminada para el caso en que el usuario decida no ejecutar de primera postman, sino inmediatamente un predict. Aparte se cuenta con un archivo **.json** de resultados, usado para armar las nubes de palabras. Dicho archivo se genera automaticamente al correr el *fit*. Por último, se tiene dos archivos **.py** donde se tiene la estructura básica de la información que se va a recibir y el procesamiento de lenguaje natural que se va a hacer.

2. *Html*: Contiene archivos **.html, .css, .js**. Son la interefaz grafica y visual del API que permite navegar sobre las nubes de palabras, así como realizar un *predict*. 

3. *Model*: Contiene un archivo **.py** con el modelo de clasificación adecuado resultante de la étapa 1 del laboratorio, es decir, un Pipeline con Vector Machine Support. Aparte esta un **.joblib** correspondiente al modelo una vez es creado para que en futuros uso solo se deba cargar.

4. *tests*: Contiene el **.txt** y el **.json** de un ejemplo del archivo necesaio para poder realizar un *predict*, así como la colección en Postman que permite realizar el *fit* del modelo.

## Archivos

Todos los archivos explican su funcionamiento internamente por medio de su respectiva documentación:

*   *main.py*: Incliye la ejecusión del **API** que permite realizar las pruebas necesarias por medio de la aplicación de **POSTMAN**: https://www.postman.com/ para el *fit* y por medio de **HTML** para el *predict* y los resultados.
*   *requierments.txt*, *nltk.txt*, *procfile*: Contiene los paquetes de Python necesarios (normalmente no instalados por defecto) que son necesarios para el proyecto, y el despliegue en Heroku.

## Ejecutar

1. Descargar el repositorio e instalar lo necesario con base en la carpeta: **requierments**.

2. Correr el Main por medio del siguiente comando en **terminal**:

```
uvicorn main:app --reload
```

3. Revisar que en consola tenga dos posibles respuestas en texto plano:

```
PipeLine Creado        or        PipeLine Cargado
```

4. Correr las pruebas en **POSTMAN**.

5. Correr las funcionalidades del HTML

## POSTMAN

Para correr las pruebas de manera local se debe usar cualquiera de los siguientes links dependiendo de la necesidad:

*   *Train*:http://127.0.0.1:8000/train

Para correr las pruebas desplegas en el servidor de Heroku se debe usar cualquiera de los siguientes links dependiendo de la necesidad:

*   *Train*: https://medical-test-bi.herokuapp.com/train

Cada uno de dichos links requiere un archivo **json** pasado como **raw** en **body** por medio de Postamn bajo la siguiente estructura: 

***TRAIN***

Es de suma importancia notar que el JSON de la carpeta data es un listado de registros. Para que el API funcione, dicha lista debe estar guardada en la variable del JSON 'data'. Aparte es necesaria la información de la variable Y, como sus explicativas X.

```
{
  "data": [
        {
            "medical_abstracts": "Cell lineage markers in human pancreatic cancer. The normal pancreas consists of three major cell types or lineages that share a common embryologic origin from pluripotent endodermal precursors. The type of cell that undergoes neoplastic transformation to form a pancreatic carcinoma is controversial and may influence the phenotype and biologic behavior of the tumor. In this study, immunohistologic techniques were used to determine the cell lineage differentiation expressed in 29 primary exocrine pancreatic adenocarcinomas, five metastatic exocrine pancreatic adenocarcinomas, and five islet cell neoplasma. Specimens of normal pancreas and chronic pancreatitis were used for comparison. The cell lineage markers consisted of monoclonal and polyclonal antibodies against trypsin and lipase (acinar cells); secretory component, carbonic anhydrase II, and pancreatic cancer mucin SPan-1 (ductal cells); and chromogranin-A and somatostatin (islet cells). The expression of carcinoembryonic antigen (CEA) and lysozyme were also determined. This collection of markers allowed the differentiation between acinar, ductal, and islet cells of normal pancreas and chronic pancreatitis specimens. The expression of cell lineage markers in islet cell tumors was homogeneous and restricted to chromogranin-A. In contrast, the expression of these markers in primary and metastatic exocrine pancreatic adenocarcinomas was variable. Reactivity with monoclonal anti-CEA was absent in normal pancreas, and was present in 83% of chronic pancreatitis specimens as well as 90% of exocrine pancreatic adenocarcinomas. In addition, lysozyme reactivity was absent in normal pancreas; however, lysozyme was expressed in one case of chronic pancreatitis, 17 cases of primary carcinoma, and three cases of metastatic carcinoma. These findings support the concept that the original transformed cell type in many pancreatic exocrine carcinomas resemble endodermal \"stem cells\" that retain the capability of differentiation along more than one cell lineage pathway. \n",
            "problems_described": 1
        },
        {
            "medical_abstracts": "Fatal pulmonary venoocclusive disease secondary to a generalized venulopathy: a new syndrome presenting with facial swelling and pericardial tamponade. We describe a patient who developed fatal pulmonary artery hypertension secondary to diffuse venulitis. This otherwise healthy young woman first presented with generalized venulopathy, with chemosis, facial swelling, pleural effusions, and pericardial tamponade. The symptoms partially responded to steroid therapy, but over a 2-year course, a rapidly progressive and fatal venoocclusive disease developed. No other primary condition was diagnosed, and at autopsy, the patient had striking venulitis throughout, including the pulmonary bed. We believe that this is a unique case of pulmonary hypertension resulting from a generalized venulopathy. \n",
            "problems_described": 5
        }
  ]
}
```

## **HTML**

La aplicación en uso se muestra de buena manera en el siguiente video: 

https://www.youtube.com/watch?v=5HHr2Yk7kIo

Y se puede contrar en:

*     https://medical-test-bi.herokuapp.com/

Es clave recordar y explicar que con el fin de poder hacer *predict* se debe pasar un archivo **.txt** con el abstracto medico como se muestra en la carpeta **tests**.

El resultado del *predict* es la predicción de cual enfermedad es dicho abstract y se muestra en pantalla. 
