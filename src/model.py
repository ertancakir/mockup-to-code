import numpy as np
import cv2
import glob
import pandas as pd

from keras import optimizers
from keras.utils import np_utils
from keras.models import Sequential, load_model, model_from_json
from keras.layers import Dense,Conv2D, MaxPooling2D, Dropout, Flatten
from sklearn.preprocessing import LabelEncoder # for one hot encoding
import matplotlib.pyplot as plt

class DeepModel(object):
    
    def __init__(self):
        self.model = self.create_model()

        self.labels = []

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape = (100,100,3)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512, activation='sigmoid'))
        model.add(Dropout(0.50))
        model.add(Dense(4, activation='softmax'))


        return model

    def imagesToNumpyArray(self, files):
        data = []
        for file in files:
            image = cv2.imread(file)
            image = cv2.resize(image,(100 ,100))
            data.append(image)
        data = np.array(data, dtype = 'float32')
        return data

    def load_data(self):
        #Train data
        csv_data = pd.read_csv('train.csv', header = None)
        data = csv_data.values
        data = np.array(data)
        for i in range(0,200):
            np.random.shuffle(data)
        
        train_data = self.imagesToNumpyArray(data[:,0])
        train_data /= 255

        self.labels = np.unique(data[:,1])

        encoder = LabelEncoder()
        encoder.fit(data[:,1])
        encoded_train_label = encoder.transform(data[:,1])
        train_labels_one_hot = np_utils.to_categorical(encoded_train_label)

        #Test data
        csv_data = pd.read_csv('test.csv', header = None)
        data = csv_data.values
        data = np.array(data)

        for i in range(0,200):
            np.random.shuffle(data)
        
        test_data = self.imagesToNumpyArray(data[:,0])
        test_data /= 255

        encoder = LabelEncoder()
        encoder.fit(data[:,1])
        encoded_test_label = encoder.transform(data[:,1])
        test_labels_one_hot = np_utils.to_categorical(encoded_test_label)

        return train_data, train_labels_one_hot, test_data ,test_labels_one_hot
        
    def train_model(self,train_data, train_labels_one_hot):
        #sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.2, nesterov=True)
        del self.model
        self.model = self.create_model()
        self.model.compile(optimizer="rmsprop", loss='categorical_crossentropy', metrics=['accuracy'])
        history = self.model.fit(train_data, train_labels_one_hot, batch_size=32, epochs=10, validation_split=(0.1))
        self.model.save("my_model.h5")
        

    def test_model(self, test_data, test_labels_one_hot):
        test_loss, test_acc = self.model.evaluate(test_data, test_labels_one_hot)
        print('test_acc:', test_acc)
        print('test_loss:',test_loss)

    def predict(self, data):
        result = []
        output = self.model.predict(np.array(data))
        indis = 0
        idx = 0
        for o in output:
            largest_value = max(o)
            indis = list(o).index(largest_value)
            if(largest_value > 0.60):
                result.append([idx, self.labels[indis]])
            idx += 1
        result = np.array(result)
        return result

    def load_weight(self):
        del self.model
        self.model = load_model('my_model.h5')