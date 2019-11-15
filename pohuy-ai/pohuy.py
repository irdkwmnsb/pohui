import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from catboost import Pool
from catboost import CatBoostClassifier
import scipy.io.wavfile as wavfile
import python_speech_features.base as speech

class pohuy:
    def __init__(self):
        if not os.path.exists('data/ours.csv'):
            raise Exception("No base data to train on (data/ours.csv missing)")
        if not os.path.exists('data/random.csv'):
            raise Exception("No base data to train on (data/random.csv missing)")
        self.ourdata = pd.read_csv('data/ours.csv')
        self.ourdata = self.ourdata.sample(frac=1)
        self.randoms = pd.read_csv('data/random.csv')
        self.upd = pd.concat([self.randoms, self.ourdata], ignore_index = True).sample(frac = 1)
        if not os.path.exists('models'):
            os.makedirs('models')
            trainModels()
        else:
            self.cbc0 = CatBoostClassifier()
            self.cbc1 = CatBoostClassifier()
            self.cbc2 = CatBoostClassifier()
            self.cbc3 = CatBoostClassifier()
            self.cbc4 = CatBoostClassifier()
            try:
                self.cbc0.load_model('models/cbc0.cbm')
                self.cbc1.load_model('models/cbc1.cbm')
                self.cbc2.load_model('models/cbc2.cbm')
                self.cbc3.load_model('models/cbc3.cbm')
                self.cbc4.load_model('models/cbc4.cbm')
    def trainModels():
        x = self.upd.drop(columns = ["person"]).values
        y = self.upd["person"].values
        x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.42)
        le = preprocessing.LabelEncoder()
        le.fit(list(upd.person.unique()))
        y_train = le.transform(y_train)
        y_valid = le.transform(y_valid)

        train = Pool(x_train, y_train)
        valid = Pool(x_valid, y_valid)

        self.cbc0 = CatBoostClassifier(iterations=100, learning_rate=0.01, depth=5)
        self.cbc0.fit(train, eval_set=valid, use_best_model=True, verbose=False)
        self.cbc1 = CatBoostClassifier(iterations=100, learning_rate=0.001, depth=4)
        self.cbc1.fit(train, eval_set=valid, use_best_model=True, verbose=False)
        self.cbc2 = CatBoostClassifier(iterations=100, learning_rate=0.0001, depth=3)
        self.cbc2.fit(train, eval_set=valid, use_best_model=True, verbose=False)
        self.cbc3 = CatBoostClassifier(iterations=100, learning_rate=0.00001, depth=2)
        self.cbc3.fit(train, eval_set=valid, use_best_model=True, verbose=False)
        self.cbc4 = CatBoostClassifier(iterations=100, learning_rate=0.000001, depth=1)
        self.cbc4.fit(train, eval_set=valid, use_best_model=True, verbose=False)
    def registerUser(self, name, age, gender, pathToWav):
        # name - string
        # age - int
        # gender - 0/1 (0 - male, 1 - female)
    def predict(self, age, gender, pathToWav):
        # do smth