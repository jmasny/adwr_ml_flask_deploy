import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
np.random.seed(2022)

# read cleaned dataset for ML
df = pd.read_csv('data/diamonds_cleaned.csv')
df = df.drop(["Unnamed: 0"], axis=1)

# split features from labels
X = df.drop(['price'], axis=1)
y = df['price']

# split train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2022)

# create RandomForrestRegressor ML model
modelRR = RandomForestRegressor()
# train ML model
modelRR.fit(X_train, y_train)
# check results
y_pred = modelRR.predict(X_test)

print("Stworzono model ML typu RandomForrestRegressor o dokładności:")
print("RMSE: {}".format(np.sqrt(mean_squared_error(y_test, y_pred))))
print("R2:   {}".format(np.sqrt(r2_score(y_test, y_pred))))

# dump to joblib
dump(modelRR, './modelRR.joblib')
