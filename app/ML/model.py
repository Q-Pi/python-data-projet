from ML.utils.utils import model_predict_proba

def predict(data, model_id):
	return model_predict_proba(data, model_id)

#import joblib
#df = pd.read_csv('data/bank-full.csv')
#
#df = df.drop(columns=['day', 'month', 'default', 'loan'])
#
#numerics = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
#cats = ['job', 'marital', 'education', 'contact', 'poutcome']
#bools = ['housing', 'y']
#
####
#
#encoders = {}
#for each in cats:
#  le = LabelEncoder()
#  le.fit(df[each])
#  #print('{}: {}'.format(each, le.classes_))
#  df[each] = le.transform(df[each])
#  encoders[each] = le
#joblib.dump(encoders, 'encoders.joblib')
#
####
#
#for each in bools:
#  df[each] = df[each].apply(lambda x: 1 if x == 'yes' else 0)
#
####
#
#target = df['y'].copy()
#features = df.copy().drop(columns=['y'])
#
####
#
#X_tr, X_te, Y_tr, Y_te = train_test_split(features, target)
#
####
#
#rf = RandomForestClassifier(n_estimators=250)
#rf.fit(X_tr, Y_tr)
#
####
#
#dt = DecisionTreeClassifier(max_depth=7)
#dt.fit(X_tr, Y_tr)
#
####
#
#joblib.dump(rf, "model_rf.joblib")
#joblib.dump(dt, "model_dt.joblib")
#
####
#
#joblib.dump(features.columns.to_list(), "selected_features.joblib")
#
####
#
#features_type = ['number', 'text', 'text', 'text', 'number', 'bool', 'text', 'number', 'number', 'number', 'number', 'text']
#joblib.dump(features_type, "features_type.joblib")
