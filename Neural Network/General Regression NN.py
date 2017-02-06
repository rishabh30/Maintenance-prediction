import numpy as numpy
import pandas as pd
import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from keras.wrappers.scikit_learn import BaseWrapper
import copy


def custom_get_params(self, **params):
    res = copy.deepcopy(self.sk_params)
    res.update({'build_fn': self.build_fn})
    return res


BaseWrapper.get_params = custom_get_params

# define base mode
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(71, input_dim=10, init='normal', activation='relu'))
    model.add(Dense(1, init='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


input_file = "QUES.csv"
input_file2 = "UIMS1.csv"

df = pd.read_csv(input_file, header=0)
df2 = pd.read_csv(input_file2, header=0)

original_headers = list(df.columns.values)
original_headers2 = list(df2.columns.values)

df = df._get_numeric_data()
df2 = df2._get_numeric_data()

numeric_headers = list(df.columns.values)
numeric_headers2 = list(df.columns.values)

numpy_array = df.as_matrix()
numpy_array2 = df2.as_matrix()

X = numpy_array[:, 0:10]
Y = numpy_array[:, 10]

training_features = [x for (y, x) in sorted(zip(Y, X), key=lambda pair: pair[0])]
training_labels = [y for (y, x) in sorted(zip(Y, X), key=lambda pair: pair[0])]
training_features = numpy.vstack(training_features)
training_labels = numpy.array(training_labels)

seed = 7
numpy.random.seed(seed)
estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=11, batch_size=5, verbose=0)
'''IndexError: list assignment index out of range
kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
'''

from CrossValidation import cross_validation

err = cross_validation(estimator,training_features,training_labels,10)
print "MMRE ERROR:", err