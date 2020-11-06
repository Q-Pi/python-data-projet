def model_predict_proba(data, model_id):
	import pandas as pd
	from joblib import load

	#from model building
	if model_id == 1:
		model_path = "ML/utils/joblibs/model_rf.joblib"
	else:
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

def model_build():
	import joblib
	df = pd.read_csv('bank-full.csv')

	df = df.drop(columns=['day', 'month', 'default', 'loan'])

	numerics = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
	cats = ['job', 'marital', 'education', 'contact', 'poutcome']
	bools = ['housing', 'y']

	###

	encoders = {}
	#should month be handled manually ?
	for each in cats:
	  le = LabelEncoder()
	  le.fit(df[each])
	  #print('{}: {}'.format(each, le.classes_))
	  df[each] = le.transform(df[each])
	  encoders[each] = le
	joblib.dump(encoders, 'encoders.joblib')

	###

	for each in bools:
	  df[each] = df[each].apply(lambda x: 1 if x == 'yes' else 0)

	###

	target = df['y'].copy()
	features = df.copy().drop(columns=['y'])

	###

	X_tr, X_te, Y_tr, Y_te = train_test_split(features, target)

	###

	rf = RandomForestClassifier(n_estimators=250)
	rf.fit(X_tr, Y_tr)

	###

	dt = DecisionTreeClassifier(max_depth=7)
	dt.fit(X_tr, Y_tr)

	###

	joblib.dump(rf, "model_rf.joblib")
	joblib.dump(dt, "model_dt.joblib")

	###

	joblib.dump(features.columns.to_list(), "selected_features.joblib")

	###

	features_type = ['number', 'text', 'text', 'text', 'number', 'bool', 'text', 'number', 'number', 'number', 'number', 'text']
	joblib.dump(features_type, "features_type.joblib")

def csv_to_db():
	import psycopg2
	HOST = "localhost"
	USER = "postgres"
	PASSWORD = "password"
	DATABASE = "marketing"
	conn = psycopg2.connect("host={} dbname={} user={} password={}".format(HOST, DATABASE, USER, PASSWORD))
	cur = conn.cursor()
	for each in sqls:
		cur.execute(each)
	conn.commit()
	sql = "SELECT * FROM customer"
	cur.execute(sql)
	print(cur.fetchall())
	conn.close()

def db_to_csv():
	query = "SELECT * FROM customer"
	HOST = "localhost"
	USER = "postgres"
	PASSWORD = "password"
	DATABASE = "marketing"
	conn = psycopg2.connect("host={} dbname={} user={} password={}".format(HOST, DATABASE, USER, PASSWORD))
	cur = conn.cursor()

	SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)

	file = Open('data/dump.csv', 'w')
	cur.copy_expert(SQL_for_file_output, file)

	db_cursor.close()
	db_conn.close()
