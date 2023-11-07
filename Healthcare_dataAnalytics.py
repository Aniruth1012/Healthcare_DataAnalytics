# -*- coding: utf-8 -*-
"""Untitled63.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FdDa_gYG2TsKykayjqDAxE9T-Llqb9sy

**Importing the Libraries**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""**Importing the Dataset**"""

dataset=pd.read_csv('heart_2020_cleaned.csv')

"""**Checking for Missing Values**"""

dataset.isnull().any().any()

"""**Shifting the dummy variables together for Feature Scaling**"""

shift=dataset.pop('HeartDisease')
dataset.insert(17,'HeartDisease', shift)

columns_to_shift = ['SkinCancer', 'KidneyDisease','Smoking','AlcoholDrinking','Stroke','Asthma','Sex','DiffWalking','GenHealth','PhysicalActivity','AgeCategory','Diabetic']

# Extract the selected columns
selected_columns = dataset[columns_to_shift]

# Drop the selected columns from their original positions
dataset.drop(columns=columns_to_shift, inplace=True)

# Concatenate the selected columns at the beginning of the DataFrame
dataset = pd.concat([selected_columns, dataset], axis=1)

"""**Encoding the Categorical Variables with a numerical order**

Label Encoding
"""

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
categorical_columns = ['SkinCancer', 'KidneyDisease','Smoking','AlcoholDrinking','Stroke','Asthma','Sex','DiffWalking','GenHealth','PhysicalActivity','AgeCategory','Diabetic']
dataset[categorical_columns] = dataset[categorical_columns].apply(lambda col: le.fit_transform(col))

"""**Seperating the Dependent and Independent Variables**"""

X=dataset.iloc[:,:-1].values
Y=dataset.iloc[:,-1].values

print(dataset)

"""**Encoding the Categorical Variables with a random order**

One Hot Encoding
"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
columns_to_encode=[15]
ct=ColumnTransformer(transformers=[('OneHotEncoding',OneHotEncoder(),columns_to_encode)],remainder='passthrough')
X=np.array(ct.fit_transform(X))

"""**Encoding the dependent variable**"""

Y=le.fit_transform(Y)

"""**Feature Engineering**"""

from sklearn.feature_selection import mutual_info_regression
mi_scores = mutual_info_regression(X,Y)
feature_names=['SkinCancer', 'KidneyDisease','Smoking','AlcoholDrinking','Stroke','Asthma','Sex','DiffWalking','GenHealth','PhysicalActivity','AgeCategory','Diabetic','Race','PhysicalHealth','SleepTime','BMI','MentalHealth']
feature_mi_scores = list(zip(feature_names, mi_scores))
feature_mi_scores.sort(key=lambda x: x[1], reverse=True)

print(feature_mi_scores)

"""**Splitting into Training and Test Set**"""

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.35,random_state=0)
#Y_train=Y_train.astype('int')
#Y_test=Y_test.astype('int')

"""**Feature Scaling**"""

print(X[3])

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train[:,14:]=sc.fit_transform(X_train[:,14:])
X_test[:,14:]=sc.transform(X_test[:,14:])

"""**Applying PCA**"""

from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

"""**Training the Best Classification Model on training set**"""

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, Y_train)

"""**Predicting the Test set results**"""

Y_pred = classifier.predict(X_test)
print(np.concatenate((Y_pred.reshape(len(Y_pred),1), Y_test.reshape(len(Y_test),1)),1))

"""**Making the Confusion Matrix**"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(Y_test,Y_pred)
print(cm)
accuracy_score(Y_test, Y_pred)

"""**Cross validation Score**"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X_train, y = Y_train, cv = 10)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation: {:.2f} %".format(accuracies.std()*100))