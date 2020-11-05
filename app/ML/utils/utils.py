def model_predict_proba(data, model_id):
	import pandas as pd
	from joblib import load

	#from model building
	if model_id == 1:
		model_path = "ML/utils/joblibs/model_rf.joblib"
	else
		model_path = "ML/utils/joblibs/model_dt.joblib"
	model = load(model_path)
	selected_features = load("ML/utils/joblibs/selected_features.joblib")
	features_type = load("ML/utils/joblibs/features_type.joblib")
	encoders = load("ML/utils/joblibs/encoders.joblib")

	#data: list -> DataFrame
	d = {}
	for i in range(0, len(selected_features)):
		if features_type[i] == 'number':
			d[selected_features[i]] = [data[i]]
		elif features_type[i] == 'text':
			d[selected_features[i]] = [encoders[selected_features[i]].transform([data[i]])]
		else:
			d[selected_features[i]] = [1 if data[i] == 'yes' else 0]
	df = pd.DataFrame(data=d, columns=selected_features)

	#model
	proba = model.predict_proba(df)

	return proba[0]