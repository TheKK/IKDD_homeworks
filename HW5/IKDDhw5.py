import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import cross_validation

# clean training data
df = pd.read_csv('train.csv', header=0)
df = df.drop(['Ticket', 'Cabin', 'Embarked', 'Name'], axis=1)
mean = np.mean(np.array([i for i in df['Age'] if not np.isnan(i)])).astype(int)
df['Age'] = df['Age'].map(lambda a: mean if np.isnan(a) else a)
df['Sex'] = df['Sex'].map(lambda a: 1 if a == 'female' else 0)
y = df['Survived']
x = df.drop(['Survived'], axis=1).values

# clean test data
tf = pd.read_csv('test.csv', header=0)
tf = tf.drop(['Name', 'Embarked', 'Cabin', 'Ticket'], axis=1)
mean = np.mean(np.array([i for i in tf['Age'] if not np.isnan(i)])).astype(int)
tf['Age'] = tf['Age'].map(lambda a: mean if np.isnan(a) else a)
tf['Sex'] = tf['Sex'].map(lambda a: 1 if a == 'female' else 0)
tf['Fare'] = tf['Fare'].map(lambda a: 0 if np.isnan(a) else int(a)).astype(int)

# fit and predict
x_train, x_test, y_train, y_test = \
        cross_validation.train_test_split(x, y, test_size=0.3, random_state=0)
        t = tree.DecisionTreeClassifier(max_depth=5)
        t.fit(x_train, y_train)
        p = t.predict(tf)

# save file
pid = tf['PassengerId'].values
r = {'PassengerId': pid, 'Survived': p}
r = pd.DataFrame(r).to_csv('result.csv', index=False) 
