from pyspark.mllib.recommendation import ALS
from numpy import array
from pyspark.sql import SQLContext, Row
from pyspark import SparkContext

sc = SparkContext("local", "Recommend")
# User input

grade = [4, 3, 5, 2, 4, 1, 3, 5, 2, 5]
movie = [2340, 2687, 1721, 919, 595, 661, 1193, 2268, 3030, 1253]

# Load and parse the data
data = sc.textFile("hw3/lesson/ratings.dat")
ratings = data.map(lambda line: array([float(x) for x in line.split('::')[0:3]]))

# Build the recommendation model using Alternating Least Squares
rank = 10
numIterations = 20
model = ALS.train(ratings, rank, numIterations)

maxUser = ratings.map(lambda a: a[0]).max()
predictResult = []
z = []
for k in range(0, len(movie)):
    td = [(i, movie[k]) for i in range(1, int(maxUser + 1))]
    testdata = sc.parallelize(td)
    predictResult.append(model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2])))
    z.append(predictResult[k].collect())

dif = []
user = []
for i in range(0, int(maxUser)):
    tmp = 0
    t = z[0][i][0]
    for j in range(0, len(movie)):
        tmp += (z[j][i][1] - grade[j]) ** 2
    dif.append(tmp)
    user.append(t)

tmp = 100000
for i in range(0, len(dif)):
    if dif[i] < tmp:
        tmp = dif[i]
        userid = user[i][0]

maxMovie = ratings.map(lambda a: a[1]).max()
td = [(userid, i) for i in range(1, int(maxMovie + 1))]
testdata = sc.parallelize(td)

# Evaluate the model on training data
predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).reduce(lambda x, y: x + y)/ratesAndPreds.count()
predictions.collect()

predictions = predictions.map(lambda p: (p[1], p[0]))
result = predictions.top(10)


# Find Movie Name by SQL
sqlContext = SQLContext(sc)
lines = sc.textFile("hw3/lesson/movies.dat")
parts = lines.map(lambda l: l.split("::"))
movieName = parts.map(lambda p: Row(index=int(p[0]), name=p[1]))

schemaMovie = sqlContext.inferSchema(movieName)
schemaMovie.registerTempTable("movie")

ans = []
c = []
for index in result:
    tmp = sqlContext.sql("SELECT name FROM movie WHERE index=" + str(index[1][1]))
    ans.append(tmp.collect()[0].name)
    c.append(index[1][1])

print c
f = open("log", "a")
f.write(str(c))
f.close()

for i in ans:
    print i.encode('utf-8')
