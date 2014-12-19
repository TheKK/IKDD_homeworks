import random
import numpy as np
import re

SET_S_COUNT = 10
ITERATION_COUNT = 10
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

## Start iteration
def getUserIdWhoHasLotsFriends(inputList, activedSet):
    maxFriendCount = 0;
    toReturn = 0;
    friendSet = set()
    for i in range(0, len(inputList)):
        if i in activedSet:
            continue
        friendSet.clear()
        ## Import all i's friends to a set
        for friend in inputList[i]:
            friendSet.add(friend)
        friendSet = friendSet - activedSet
        if (len(friendSet) > maxFriendCount):
            toReturn = i
            maxFriendCount = len(friendSet)
    return toReturn

topTenSet = set()
activedSet = set()
readySet = set()
prograss = []

for i in range(0, SET_S_COUNT):
    theFirstOne = getUserIdWhoHasLotsFriends(relationshipList, activedSet)
    topTenSet.add(theFirstOne)
    readySet.add(theFirstOne)
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
print('Top 10 seed: ' + str(topTenSet))
print('Prograss: ' + str(prograss))
