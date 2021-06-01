import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Dataset Iris de sklearn

from sklearn import datasets

iris = datasets.load_iris()

df = pd.DataFrame(data = iris.data, columns = iris.feature_names)
df['target'] = iris.target

# Imprimir en consola para visualizar el DataFrame resultante con los 5 primeros elementos
print(df.head())

# Definir X e Y del DataFrame establecido

# axis 0 = rows, axis 1 = columns 
X = df.drop('target', axis =1 )
y = df.target

# Calculamos la distancia entre 2 puntos usando distancia euclidiana

def euclidian_distance(punto1, punto2):
    
    # Inicializamos la variable distancia en 0
    distance = 0
    
    # Calculamos la distancia euclidiana 
    for i in range(len(punto1)):
        print(i)
        distance += abs(punto1[i] - punto2[i])**2      
    
    distance = distance ** (1/2)

    return distance


# Definimos un punto de prueba

test_pt = [4.8, 2.7, 2.5, 0.7]

# Calculamos la distancia entre el punto de prueba y todos los puntos en X

distances = []

print(X.index)

for i in X.index:
    
    distances.append(euclidian_distance(test_pt, X.iloc[i]))
    
df_dists = pd.DataFrame(data = distances, index = X.index, columns=['distance'])

# Imprimimos el nuevo DataFrame que contiene las distancias de los primeros 5 elementos  

print(df_dists.head())

# Encontramos los 5 vecinos más cercanos

# [:5] se refiere a un "slice" (desde el inicio hasta 5-1) 

print("\n5 vecinos más cercanos \n")

df_nn = df_dists.sort_values(by = ['distance'], axis = 0)[:5]
print(df_nn)

# Create counter object to track the labels

counter = Counter(y[df_nn.index])

print(counter)

# Get most common label of all the nearest neighbors

counter.most_common()[0][0]

print(counter.most_common()[0][0])

# Split the data - 75% train, 25% test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,
                                                   random_state=1)

# Scale the X data

print("-----------------------------------------------------------------------------------------")
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def knn(X_train, X_test, y_train, k):
    
    # Make predictions on the test data
    # Need output of 1 prediction per test data point

    y_hat_test = []

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
        y_hat_test.append(prediction)
        
    return y_hat_test


# Make predictions on test dataset
y_hat_test = knn(X_train, X_test, y_train, k=5)

print(y_hat_test)
print(accuracy_score(y_test, y_hat_test))