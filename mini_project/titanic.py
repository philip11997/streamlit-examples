# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:54:50 2022

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pickle
import requests
from io import BytesIO


st.title('PREDICT YOUR SURVIVAL ON THE TITANIC')
url = 'https://raw.githubusercontent.com/philip11997/streamlit-examples/ff154571291c6529da262244d65a451f95fe4f57/mini_project/titanic.jpg'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img,width=600, channels='RGB',caption=None)

df = pd.read_csv('https://raw.githubusercontent.com/philip11997/streamlit-examples/main/mini_project/titanic.csv')
#drop the name columns
df = df.drop(columns='Name')
#encode the sec column
df.loc[df['Sex']=='male', 'Sex'] = 1
df.loc[df['Sex']=='female', 'Sex'] = 0
#split the data in to independent x and y variables
X = df.drop('Survived', axis =1)
y=df['Survived'].values.astype(np.float32)
X = X.values.astype(np.float32)

X_train, X_val, y_train, y_val = train_test_split(X,y, test_size=0.2, random_state=1)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(6,)),
    keras.layers.Dense(6, activation=tf.nn.relu),
	keras.layers.Dense(4, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.relu),
    keras.layers.Dense(1, activation=tf.nn.sigmoid)
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['acc']) 

model.save('titanic.h5')
history = model.fit(X_train, y_train, epochs=119, batch_size=1,validation_data=(X_val, y_val))

with open('training_history','wb') as file:
    pickle.dump(history.history, file)

model = load_model('titanic.h5')
history = pickle.load(open('training_history','rb'))

def survival():
    Pclass = st.sidebar.slider('Pclass',1,3)
    sex = st.sidebar.selectbox('Sex', ('Male','Female'))
    age = st.sidebar.slider('Age',0,80)
    n_siblings_spouses = st.sidebar.slider('N_siblings/spouses',0,3)
    n_parents_children = st.sidebar.slider('N_parents/children',0,3)
    fair = st.sidebar.slider('Fair',0,200)
    
    if sex == 'Male':
        sex = 1
    else:
        sex = 0

    data = [[Pclass, sex, age, n_siblings_spouses,n_parents_children,fair]]
    data = tf.constant(data)
    return data

survive_or_not=survival()
prediction = model.predict(survive_or_not, steps=1)
pred = [round(x[0]) for x in prediction]

if pred ==[0]:
    st.write('You did not survive')
else:
    st.write('You survived')


def plot_data():
    loss_train=history['loss']
    loss_val = history['val_loss']
    epochs = range(1,120)
    fig, ax = plt.subplots()
    ax.scatter([0.25],[0.25])
    plt.plot(epochs, loss_train,'g', label = 'Training Loss')
    plt.plot(epochs, loss_val,'b', label = 'Validation Loss')
    plt.title('Trainig and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    st.pyplot(fig)
    
    loss_train =history['acc']
    loss_val = history['val_acc']
    epochs = range(1,120)
    fig, ax = plt.subplots()
    ax.scatter([1], [1])
    plt.plot(epochs, loss_train, 'g', label='Training Accuracy')
    plt.plot(epochs, loss_val, 'b', label='Validation Accuracy')
    plt.title('Training and Validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
    st.pyplot(fig)
    
plot_data()
