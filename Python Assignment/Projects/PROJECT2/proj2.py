#Project:  Machine Learning Mine Versus Rock
#This project uses MLP classifiers to detect mines in the sea.
#The accuracy is tested for different number of components thanks to PCA

#import the libraries needed
import pandas as pd     #To read the data file
from sklearn.model_selection import train_test_split    #To split the data as training and test datasets
import matplotlib.pyplot as plt     #To Plot the graph
from sklearn import datasets    #To perform ML
import numpy as np      #For the arrays
from sklearn.decomposition import PCA       #To divide into many components
from sklearn.preprocessing import StandardScaler    #To standardize the data
from sklearn.metrics import accuracy_score      #To find the accuracy
from sklearn.metrics import confusion_matrix    #To create the confusion matrix
from sklearn.neural_network import MLPClassifier    #To use the MLP classifier
from warnings import filterwarnings     #To filter out any warnings we may get

#Filter the warning
filterwarnings('ignore')

#Read the data from the csv file using pandas
df = pd.read_csv("sonar_all_data_2.csv", header = None)

#Split the data to 70% training and 30% test data
train, test = train_test_split(df, test_size = 0.3, random_state = 0)
X_train = train.iloc[:, 0:60]   #The features lie from column 0 t0 60
y_train = train[61]             #The classes are in column 61
X_test = test.iloc[:, 0:60]     #The features lie from column 0 t0 60
y_test = test[61]               #The classes are in column 61

#Empty variables to later store the maximum accuracy and component, to calculate the confusion matrix
max_accuracy = 0.00
max_component = 0

#Apply standardization
stdsc = StandardScaler()
X_train_std = stdsc.fit_transform(X_train)
X_test_std = stdsc.transform(X_test)

#Create empty arrays to hold the values of accuracy and number of components, this will be used to plot the graph
number_of_components = np.zeros(61)
accuracy = np.zeros((61), dtype = float)

#Fill in the number of components array
for i in range(1,61):
    number_of_components[i] = i

#Create a random seed to be used as the value for the random state of MLP classifier
random_seed = np.random.randint(0, 2147483645)

#Create a for loop to calculate the accuracy for each number of componet from 1 to 60
for n in range(1, 61):
    pca = PCA(n_components=n)
    X_train_pca = pca.fit_transform(X_train_std)
    X_test_pca = pca.transform(X_test_std)

    model = MLPClassifier( hidden_layer_sizes = (100), activation='logistic', max_iter=2000, alpha=0.00001, solver='adam', tol=0.0001, random_state = random_seed)
    model.fit(X_train_pca, y_train)

#Find and print the accuracy for each number of components
    y_pred = model.predict(X_test_pca)
    print('Number of components used is {} and the accuracy is {} '.format(n, round(accuracy_score(y_test, y_pred), 2)))
#Store the accuracy in the array
    accuracy[n] = round(accuracy_score(y_test, y_pred), 2)
#Find the maximum accuracy and store it in the variable, max_accuracy and number of component in max_component
    if(round(accuracy_score(y_test, y_pred), 2) > max_accuracy):
        max_accuracy = round(accuracy_score(y_test, y_pred), 2)
        max_component = n
        y_test_max = y_test
        y_pred_max = y_pred

#Print the maximum accuracy achieved and the number of components used to achieve the accuracy
print('\nThe maximum accuracy is {} which is got when {} components are used'.format(max_accuracy, max_component))

#Find the confusion matrix for the maximum accuracy achieved and print it
confusion_matrix = confusion_matrix(y_test_max,y_pred_max)
print('The confusion matrix for the maximum accuracy is: ')
print(confusion_matrix)

#Plot the graph with number of components in x-axis and accuracy in y-axis and display it
plt.plot(number_of_components, accuracy)
plt.xlabel('Number of components')
plt.ylabel('Accuracy')
plt.show()