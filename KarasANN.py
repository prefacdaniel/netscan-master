# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn import preprocessing
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
dataset = numpy.loadtxt("C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\data_for_ann.csv", delimiter=",")
dataset_test = numpy.loadtxt("C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\data_for_test.csv", delimiter=",")

# print("STD: ")
# print(dataset.std)

# Normalize Training Data

std_scale = preprocessing.StandardScaler().fit(dataset)
dataset = std_scale.transform(dataset)
dataset_test = std_scale.transform(dataset_test)

std_scale = preprocessing.StandardScaler().fit(dataset)
# print("STD: ")
# print(dataset.std)


#
# #Converting numpy array to dataframe
# training_norm_col = pd.DataFrame(x_train_norm, index=train_norm.index, columns=train_norm.columns)
# x_train.update(training_norm_col)
# print (x_train.head())
#
# # Normalize Testing Data by using mean and SD of training set
#
# x_test_norm = std_scale.transform(test_norm)
# testing_norm_col = pd.DataFrame(x_test_norm, index=test_norm.index, columns=test_norm.columns)
# x_test.update(testing_norm_col)
# print (x_train.head())



# split into input (X) and output (Y) variables
X = dataset#[:800]
Y = numpy.zeros(len(X))
# create model
model = Sequential()
model.add(Dense(12, input_dim=4, activation='tanh'))
model.add(Dense(6, activation='tanh'))
model.add(Dense(1, activation='tanh'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) #todo: for loss user: binary_crossentropy or mean_squared_logarithmic_error
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)
# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


X_myTest = dataset[800:]
Y_test = numpy.zeros(len(X_myTest))
scores = model.evaluate(X_myTest, Y_test)
print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


# prediction = model.predict_classes(dataset_test)
# print(prediction)
prediction = model.predict(dataset_test)
print(prediction)

print("evaluate training data")
# prediction = model.predict_classes(X)
# print(prediction)
prediction = model.predict(X)
print(prediction)
