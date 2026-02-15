# Following Machine learning examples with Google dev , Josh Gordon.
# playlist https://youtube.com/playlist?list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal&si=eTDh_txY7s9OS9eR
# date 1 feb 26
# ep1 ; example1


#print('hello world!')

import sklearn as sk
from sklearn import tree

features = [ [140, 1], [130, 1], [150, 0], [170, 0] ]
labels = [0, 0, 1, 1]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)
prd = clf.predict([[160, 1]])
print(prd)
