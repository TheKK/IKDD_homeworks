import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

data = np.array([])
f = open('data.txt', 'r')
data = f.read().split('\n')
data = data[0:-1]

answer = []
for i in range(0, len(data)):
    data[i] = data[i].split(',')
    if data[i][0] == 'republican':
        answer.append(1)
    elif data[i][0] == 'democrat':
        answer.append(0)
    data[i] = data[i][1:]

for i in range(0, len(data)):
    for j in range(0, len(data[0])):
        if data[i][j] == 'y':
            data[i][j] = 1
        elif data[i][j] == 'n':
            data[i][j] = -1
        else:
            data[i][j] = 0

kmeans = KMeans(n_clusters=2, n_init=50)
kmeans.fit(data)
labels = kmeans.labels_

# write file
c1 = pd.DataFrame([i for i in range(0, len(labels)) if labels[i] == 0])
c2 = pd.DataFrame([i for i in range(0, len(labels)) if labels[i] == 1])
c1.to_csv("cluster1.csv", index=False, header=False)
c2.to_csv("cluster2.csv", index=False, header=False)


# F1-score
def score():
    c = 0
    TP, TN, FN, FP = 0, 0, 0, 0
    for i in range(0, len(answer)):
        if labels[i] == answer[i] and labels[i] == 1:
            TP += 1
            c += 1
        elif labels[i] == answer[i] and labels[i] == 0:
            TN += 1
            c += 1
        elif labels[i] != answer[i] and labels[i] == 0:
            FN += 1
        elif labels[i] != answer[i] and labels[i] == 1:
            FP += 1
    F = 2 * TP / (2*TP + FP + FN)
    return F
s1 = score()
answer = [abs(k-1) for k in answer]
s2 = score()
print(max(s1, s2))
