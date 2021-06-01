import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


# Leemos dataset iris.csv
dataset = pd.read_csv('iris.csv')

# Asignamos X a sus medidas y y a su especie
X = dataset.iloc[:,[0,3]]
y = dataset.iloc[:,4]

# Calculamos la distancia entre 2 puntos usando distancia euclidiana

def euclidian_distance(punto1, punto2):
    
    # Inicializamos la variable distancia en 0
    distance = 0
    
    # Calculamos la distancia euclidiana 
    for i in range(len(punto1)):
        distance += abs(punto1[i] - punto2[i])**2    

    distance = distance ** (1/2)
    return distance

# Split the data - 75% train, 25% test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
                                                   random_state=1)

# Scale the X data

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def knn(X_train, X_test, y_train, k):
    
    # Make predictions on the test data
    # Need output of 1 prediction per test data point

    y_pred_test = []

    for test_point in X_test:
        distances = []

        for train_point in X_train:
            distance = euclidian_distance(test_point, train_point)
            distances.append(distance)
        
        # Store distances in a dataframe
        df_dists = pd.DataFrame(data=distances, columns=['dist'], 
                                index=y_train.index)
        
        # Sort distances, and only consider the k closest points
        df_nn = df_dists.sort_values(by=['dist'], axis=0)[:k]

        # Create counter object to track the labels of k closest neighbors
        counter = Counter(y_train[df_nn.index])

        # Get most common label of all the nearest neighbors
        prediction = counter.most_common()[0][0]
        
        # Append prediction to output list
        y_pred_test.append(prediction)
        
    return y_pred_test


# Make predictions on test dataset

predictions = knn(X_train, X_test, y_train, k=5)

print(accuracy_score(y_test, predictions))