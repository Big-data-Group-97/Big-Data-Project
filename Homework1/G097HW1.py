
from pyspark import SparkContext, SparkConf
import sys
import os
import random as rand


def main():

	# CHECKING NUMBER OF CMD LINE PARAMTERS
	assert len(sys.argv) == 3, "Usage: python HW097.py <K> <H> <S> <database>"

	# SPARK SETUP
	conf = SparkConf().setAppName('HomeWork 1 Group 97').setMaster("local[*]")
	sc = SparkContext(conf=conf)

	# INPUT READING

	# 1. Read number of partitions
	K = sys.argv[1]
	assert K.isdigit(), "K must be an integer"
	K = int(K)

	H = sys.argv[2]
	assert H.isdigit(), "H must be an integer"
	H = int(H)

	S = sys.argv[3]
	assert S.isalphanum(), "S must be an string"
	S = string(S)

	# 2. Read input file and subdivide it into K random partitions
	data_path = sys.argv[4]
	assert os.path.isfile(data_path), "File or folder not found"
	docs = sc.textFile(data_path,minPartitions=K).cache()
	docs.repartition(numPartitions=K)



if __name__ == "__main__":
	main()
