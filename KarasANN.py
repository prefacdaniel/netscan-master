# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn import preprocessing
import keras
import numpy
from keras.models import model_from_json
from sklearn.externals.joblib import dump, load

# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
dataset = numpy.loadtxt("C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\data_for_ann.csv", delimiter=",")
dataset_test = numpy.loadtxt("C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\csv\\data_for_test.csv",
                             delimiter=",")

# print("STD: ")
# print(dataset.std)

# Normalize Training Data

std_scale = preprocessing.StandardScaler().fit(dataset)
dataset = std_scale.transform(dataset)
dataset_test = std_scale.transform(dataset_test)


dump(std_scale, 'std_scaler.bin', compress=True)
sc = load('std_scaler.bin')
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
X = dataset  # [:800]
Y = numpy.ones(len(X))
# create model
model = Sequential()
model.add(Dense(6, input_dim=4, activation='tanh'))
model.add(Dense(3, activation='tanh'))
model.add(Dense(1, activation='relu'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam',
              metrics=['accuracy'])  # todo: for loss user: binary_crossentropy or mean_squared_logarithmic_error
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)
# evaluate the model


prediction = model.predict_classes(dataset_test)
print(prediction)
prediction = model.predict(dataset_test)
print(prediction)

print("evaluate training data")
prediction = model.predict_classes(X)
print(prediction)
prediction = model.predict(X)
print(prediction)


def save_json(model_name, trained_model):
    model_json = trained_model.to_json()
    with open(model_name + ".json", "w") as json_file:
        json_file.write(model_json)
    trained_model.save_weights(model_name + ".h5")


def load_json_model(model_name):
    json_file = open(model_name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_trained_model = model_from_json(loaded_model_json)
    loaded_trained_model.load_weights(model_name + ".h5")
    loaded_trained_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_trained_model


scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0] * 100))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
print("My ev:")
test_Y = numpy.zeros(len(dataset_test))
scores = model.evaluate(dataset_test, test_Y)
print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0] * 100))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

save_json("model", model)

loaded_model = load_json_model("model")

scores = loaded_model.evaluate(X, Y)
print("\n%s: %.2f%%" % (loaded_model.metrics_names[0], scores[0] * 100))
print("\n%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1] * 100))
print("My ev:")
test_Y = numpy.zeros(len(dataset_test))
scores = loaded_model.evaluate(dataset_test, test_Y)
print("\n%s: %.2f%%" % (loaded_model.metrics_names[0], scores[0] * 100))
print("\n%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1] * 100))
