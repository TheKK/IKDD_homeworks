import random
import numpy as np
import re

SET_S_COUNT = 10
ITERATION_COUNT = 1
PROPOGATION_PROBABILITY = 0.1

## Read data sheet
rawData_fd = open('./loc-brightkite_edges.txt')
rawData_str = rawData_fd.readlines()
rawData_fd.close()

## Get total user count
searchResult = re.search('\d*', rawData_str[-1])
userCount = int(searchResult.group()) + 1

## Construct user relationship vector
relationshipList = []
for i in range(0, userCount):
    relationshipList.append([])

for line in rawData_str:
    searchResult = re.search('\d*', line)
    userId = int(searchResult.group())
    searchResult = re.search('(?<=\t)\d*', line)
    friendId = int(searchResult.group())
    relationshipList[userId].append(friendId)

## Caculate f(s) of each user node
activedSet = set()
setS = set()
prograss = []

for round in range(0, SET_S_COUNT):
    valueList = []
    ## Try everyone
    for user in range(0, userCount):
        totalActiveNum = 0
        averageActiveNum = 0
        for i in range(0, ITERATION_COUNT):
            readySet = set()
            testActivedSet = activedSet.copy()
            readySet.add(i)
            while len(readySet) > 0:
                toActive = readySet.pop()
                if toActive in testActivedSet:
                    continue
                testActivedSet.add(toActive)
                for friend in relationshipList[toActive]:
                    if (random.random() <= PROPOGATION_PROBABILITY):
                        readySet.add(friend)
            totalActiveNum += len(testActivedSet)
        averageActiveNum = totalActiveNum / ITERATION_COUNT
        valueList.append(averageActiveNum)
    ## Find the most powerful user
    for user in range(0, userCount):
        maxInfluence = 0
        candidate = 0
        if (valueList[i] > maxInfluence) and (i not in setS):
            candidate = i
            maxInfluence = valueList[i]
    setS.add(candidate)
    ## Do real play
    readySet = set()
    readySet.add(i)
    while len(readySet) > 0:
        toActive = readySet.pop()
        if toActive in activedSet:
            continue
        activedSet.add(toActive)
        for friend in relationshipList[toActive]:
            if (random.random() <= PROPOGATION_PROBABILITY):
                readySet.add(friend)
    prograss.append(len(activedSet))

print(setS)
print(prograss)
