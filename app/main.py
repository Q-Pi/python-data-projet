from fastapi import FastAPI
from joblib import load
from ML.model import predict
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import status

from pydantic import BaseModel

#features = 		['age', 	'job', 	'marital', 	'education', 'balance', 'housing', 	'contact', 	'duration', 'campaign', 'pdays',  'previous','poutcome']
#features_type = 	['number', 	'text', 'text', 	'text', 	 'number', 	'bool', 	'text', 	'number', 	'number', 	'number', 'number',  'text']

class Customer(BaseModel):
	age: 		int
	job: 		str
	marital:	str
	education:	str
	balance:	int
	housing:	bool
	contact:	str
	duration:	int
	campaign:	int
	pdays:		int
	previous:	int
	poutcome:	str

#endpoints:
#/
#/models
#/model/1/
#/model/1/predict
#/model/1/result
#/model/2/
#/model/2/predict
#/model/2/result
#/crud/c/
#/crud/r/
#/crud/u/
#/crud/d/

app = FastAPI()

@app.get('/')
def index():
	return RedirectResponse(url='/models')

@app.get('/models', response_class=HTMLResponse)
async def models(request: Request):
	html = "<h1>Modèles :</h1>"
	html += "<a href=\"model/1\">RandomForest</a>"
	html += "<br></br>"
	html += "<a href=\"model/2\">DecisionTree</a>"
	return html

@app.get('/model/1', response_class=HTMLResponse)
def model_1():
	html = "<h1>RandomForest :</h1>"
	html += "<h2>n_estiamtors=250</h2>"
	html += "<a href=\"/model/1/predict\">Prédire</a>"
	return html

@app.get('/model/2', response_class=HTMLResponse)
def model_2():
	html = "<h1>DecisionTree :</h1>"
	html += "<h2>max_depth=7</h2>"
	html += "<a href=\"/model/2/predict\">Prédire</a>"
	return html

@app.get('/model/1/predict', response_class=HTMLResponse)
def model_1_predict():
	selected_features = load("ML/utils/joblibs/selected_features.joblib")
	features_type = load("ML/utils/joblibs/features_type.joblib")
	html = "<p>Features</p>"
	html += "<form method=\"POST\">"
	for i in range(0, len(selected_features)):
		html += "<p>" + selected_features[i] + "</p><input type=\""
		html += "number" if features_type[i] == "number" else ("checkbox" if features_type[i] == "bool" else "text")
		html += "\" name=\"" + selected_features[i] + "\" value=\"\"><br></br>"
	html += "<input type=\"submit\" value=\"Valider\"></form>"
	return html

@app.get('/model/2/predict', response_class=HTMLResponse)
def model_2_predict():
	selected_features = load("ML/utils/joblibs/selected_features.joblib")
	features_type = load("ML/utils/joblibs/features_type.joblib")
	html = "<p>Features</p>"
	html += "<form method=\"POST\">"
	for i in range(0, len(selected_features)):
		html += "<p>" + selected_features[i] + "</p><input type=\""
		html += "number" if features_type[i] == "number" else ("checkbox" if features_type[i] == "bool" else "text")
		html += "\" name=\"" + selected_features[i] + "\" value=\"\"><br></br>"
	html += "<input type=\"submit\" value=\"Valider\"></form>"
	return html

@app.post('/model/1/predict')
async def model_1_predict_post(request: Request):
	data = []
	form_data = await request.form()
	for each in form_data:
		data.append(form_data[each])
	return RedirectResponse(url='/model/1/result/'+str(predict(data, 1)), status_code=status.HTTP_303_SEE_OTHER)

@app.post('/model/2/predict')
async def model_2_predict_post(request: Request):
	data = []
	form_data = await request.form()
	for each in form_data:
		data.append(form_data[each])
	return RedirectResponse(url='/model/2/result/'+str(predict(data, 2)), status_code=status.HTTP_303_SEE_OTHER)

@app.get('/model/1/result/{data}', response_class=HTMLResponse)
def model_1_result(data: str = None):
	data = data[1:-1]
	data = data.split("+")
	html = "<h1>Resultat : {}</h1>".format('Non' if data.index(max(data)) == 0 else 'Oui')
	html += "<p>{} : {}</p>".format('Non', data[0])
	html += "<p>{} : {}</p>".format('Oui', data[1])
	return html

@app.get('/model/2/result/{data}', response_class=HTMLResponse)
def model_2_result(data: str = None):
	data = data[1:-1]
	data = data.split("+")
	html = "<h1>Resultat : {}</h1>".format('Non' if data.index(max(data)) == 0 else 'Oui')
	html += "<p>{} : {}</p>".format('Non', data[0])
	html += "<p>{} : {}</p>".format('Oui', data[1])
	return html

@app.get('/csv_to_db', response_class=HTMLResponse)
def csv_to_db():
	csv_to_db()
