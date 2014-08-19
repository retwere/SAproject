from pyspark import SparkContext

logFile = "/opt/spark-1.0.2/README.md"
sc = SparkContext("local", "Simple App")
logData = sc.textFile(logFile).cache()

numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()

print "Lines with a: {}, lines with b: {}".format(numAs,numBs)
