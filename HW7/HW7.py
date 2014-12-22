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

## Get set S
valueList = []
for user in range(0, userCount):
    valueSum = 0
    averageValue = 0
    for i in range(0, ITERATION_COUNT):
        for friend in relationshipList[user]:
            if (random.random() <= PROPOGATION_PROBABILITY):
                valueSum += 1
    averageValue = valueSum / ITERATION_COUNT
    valueList.append(averageValue)

setS = set()
for i in range(0, SET_S_COUNT):
    maxValue = 0
    maxUser = 0
    for user in range(0, userCount):
        if ((valueList[user] > maxValue) and (user not in setS)):
            maxValue = valueList[user]
            maxUser = user
    setS.add(maxUser)

## Calculate f(S)
activedSet = set()
readySet = set()
prograss = []

for seed in setS:
    readySet.add(seed)
    while len(readySet) > 0:
        theNext = readySet.pop();
        if theNext in activedSet:
            continue
        else:
            activedSet.add(theNext);
        for friend in relationshipList[theNext]:
            if random.random() <= PROPOGATION_PROBABILITY:
                readySet.add(friend)
    prograss.append(len(activedSet))

print('Total user: ' + str(userCount))
print('Actived user: ' + str(len(activedSet)))
print("set S: " + str(setS))
print('Prograss: ' + str(prograss))
