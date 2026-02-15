# Following Machine learning examples with Google dev , Josh Gordon.
# playlist https://youtube.com/playlist?list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal&si=eTDh_txY7s9OS9eR
# date 1 feb 26
# ep3 ; example3


import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree


iris = load_iris()
test_idx = [0, 50, 100]

# training data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# testing data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

# save classifier in a variable
clf = tree.DecisionTreeClassifier()

# train the classifier
clf = clf.fit(train_data, train_target)

# check data manually before predicting
print(test_data, test_target)

# predict from test data
#prd = clf.predict(test_data)
prd = clf.predict( [[7. , 3.1 , 4.7 , 1.4]] )
print(prd)
