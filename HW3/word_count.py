from pyspark import SparkContext

sc = SparkContext("local", "Recommend")
t = sc.textFile("hw3/pg5000.txt")

print t.count()
