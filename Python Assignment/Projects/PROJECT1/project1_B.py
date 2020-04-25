import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

RANDOM_STATE = 10 # fixing random state to get reproducible results

df = pd.read_csv("data_banknote_authentication.txt", header=None)

train, test = train_test_split(df, test_size=0.2, random_state=RANDOM_STATE) # Splitting dataset into 80% train-20% test
train_X = train.iloc[:, 0:4] # the independent variables lie in indexes 0 through 4 (0 inclusive, 4 exclusive)
train_Y = train[4] # the dependent variable / class variable is in the 4th index
test_X = test.iloc[:, 0:4] # Similar to train's independent variable
test_Y = test[4] # Similar to test's dependent variable

def classify_data(classifier, classifier_params, classifier_name, train_X, train_Y, test_X, test_Y):
    # This function takes the sklearn classifier function, parameters to be passed to the classifier,
    # classifier name, the training data, training ground truth, testing data and testing ground truth

    clf = classifier(**classifier_params).fit(train_X, train_Y)  # Instantiating the classifier model and training it
    train_predictions = clf.predict(train_X) # Getting our model predictions of training set
    test_predictions = clf.predict(test_X) # Getting our model predictions of testing set

    # Calculating the various metrics of our model viz. accuracy, precision (tp/tp+fp) and recall (tp/tp+fn) and storing in DataFrame

    results_df = pd.DataFrame.from_dict({
        "classifier_name": [classifier_name],
        "train_precision": [precision_score(train_Y, train_predictions)],
        "train_recall": [recall_score(train_Y, train_predictions)],
        "train_accuracy": [accuracy_score(train_Y, train_predictions)],
        "test_precision": [precision_score(test_Y, test_predictions)],
        "test_recall": [recall_score(test_Y, test_predictions)],
        "test_accuracy": [accuracy_score(test_Y, test_predictions)]
    }).set_index('classifier_name')

    return results_df

# Configuring all the classification techniques and their parameters
classifier_params = {
    "perceptron": [Perceptron, {"random_state": RANDOM_STATE}],
    "logistic_regression": [LogisticRegression, {"random_state": RANDOM_STATE, "solver":"lbfgs"}],
    "knn_classifier": [KNeighborsClassifier, {"n_neighbors": 2}],
    "decision_tree": [DecisionTreeClassifier, {"random_state": RANDOM_STATE}],
    "random_forest": [RandomForestClassifier, {"random_state": RANDOM_STATE, "max_depth": 10}],
    "svm": [SVC, {"random_state": RANDOM_STATE, "gamma": "auto"}]
}

# Initializing an empty dataframe
results = pd.DataFrame.from_dict({
    "train_precision": [],
    "train_recall": [],
    "train_accuracy": [],
    "test_precision": [],
    "test_recall": [],
    "test_accuracy": []
})

# Looping through all classification techniques
for key, val in classifier_params.items():
    results = results.append(
                classify_data(val[0], val[1], key, train_X, train_Y, test_X, test_Y),
                sort=True
              )
# Displaying the results sorted descending first by test accuracy, following by train accuracy
print("results: \n", results.sort_values(["test_accuracy", "train_accuracy"], ascending=False))