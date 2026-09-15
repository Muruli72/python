
from pyspark.sql import SparkSession

spark=SparkSession.builder.appName("word_count").getOrCreate()

df=spark.read.text("/Users/harish/Downloads/python/BDALAB/hello.text")

rdd=df.rdd

word_count=rdd.flatMap(lambda line: line[0].split()) \
              .map(lambda word: (word,1)) \
              .reduceByKey(lambda a,b: a+b)

for word,count in word_count.collect():
    print(word,count)

spark.stop()
