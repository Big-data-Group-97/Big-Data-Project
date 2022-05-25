from pyspark import SparkContext, SparkConf
import sys
import os
import random as rand


def first_elaboration(RDD, S):
    if(S!="all"):
        RDD = RDD.filter(lambda line: line.split(",")[7] == S and int(line.split(",")[3]) > 0)
    else:
        RDD = RDD.filter(lambda line: line.split(",")[3] > 0)
    print("Number of rows after filter:", RDD.count())
    RDD.flatMap(lambda line: ((line.split(",")[1], line.split(",")[6]), 1))
    print("Number of rows after mapping:", RDD.count())
    RDD.groupByKey()
    print("Number of rows after group:", RDD.count())
    RDD.flatMap(lambda line: (line[0][0], line[0][1]))
    print("Number of rows, point 2:", RDD.count())
    print(RDD.collect())
    return RDD

def second_elaboration(RDD):
    RDD = RDD.mapPartitions(manipulatePartition).groupByKey().mapValues(lambda vals: sum(vals))
    print("Number of rows, point 3:", RDD.count())
    print(RDD.collect())
    return RDD

def manipulatePartition(partition):
    new_partition=[]
    for pair in partition:
        pair=(pair[0], 1)
        new_partition.append(pair)
        return new_partition

def third_elaboration(RDD):
    RDD = RDD.map(lambda line: (line[0], 1)).reduceByKey(lambda x, y: x + y)
    print("Number of rows, point 4:", RDD.count())
    print(RDD.collect())
    return RDD

def fourth_elaboration(RDD, H):
    RDD.map(lambda line: (line[1], line[0])).sortByKey(False)
    list = RDD.take(H)
    print("First ", H, " elements by popularity:\n")
    for x in list:
        print(x, "\n")
    return

def fifth_elaboration(RDD_1, RDD_2):
    list = RDD_1.sortByKey().collect().tolist()
    print("Elements in productPopularity1:\n")
    for x in list:
        print(x, "\n")
    list = RDD_2.sortByKey().collect().tolist()
    print("Elements in productPopularity2:\n")
    for x in list:
        print(x, "\n")
    return

def main():
    assert len(sys.argv) == 5, "Usage: python GxxxHW1.py <K> <H> <S> <file_name>"

    conf = SparkConf().setAppName('G097HW1').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    K = sys.argv[1]
    assert K.isdigit(), "K must be an integer"
    K = int(K)
    H = sys.argv[2]
    assert H.isdigit(), "H must be an integer"
    H = int(H)
    S = sys.argv[3]

    data_path = sys.argv[4]
    assert os.path.isfile(data_path), "File or folder not found"
    rawData  = sc.textFile(data_path,minPartitions=K).cache().repartition(numPartitions=K)
    print("Number of rows:", rawData.count())
    productCostumer = first_elaboration(rawData, S)
    productPopularity1 = second_elaboration(productCostumer)
    productPopularity2 = third_elaboration(productCostumer)
    if H>0:
        fourth_elaboration(productPopularity1, H)
    if H==0:
        fifth_elaboration(productPopularity1, productPopularity2)

if __name__ == "__main__":
	main()