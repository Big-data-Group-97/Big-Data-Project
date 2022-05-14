#!/bin/bash
echo "RUNNING THE PYTHON SCRIPT PROGRAMMATICALLY"
echo "RESULTS WILL BE PRONTED TO out.txt"

if [ -s out.txt ]; then
    echo "REMOVING OLD RESULTS"
    rm -f out.txt
fi
touch out.txt

echo "RUNNING ON testdataHW2.csv WITH K 3 Z 0"
python3 G097HW2.py -f testdataHW2.csv -k 3 -z 0 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON testdataHW2.csv WITH K 3 Z 1"
python3 G097HW2.py -f testdataHW2.csv -k 3 -z 1 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON testdataHW2.csv WITH K 3 Z 3"
python3 G097HW2.py -f testdataHW2.csv -k 3 -z 3 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON uber-small.csv WITH K 10 Z 0"
python3 G097HW2.py -f uber-small.csv -k 10 -z 0 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON uber-small.csv WITH K 10 Z 100"
python3 G097HW2.py -f uber-small.csv -k 10 -z 100 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON artificial9000.csv WITH K 9 Z 0"
python3 G097HW2.py -f artificial9000.csv -k 9 -z 0 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON artificial9000.csv WITH K 9 Z 200"
python3 G097HW2.py -f artificial9000.csv -k 9 -z 200 &>> out.txt
echo "" >> out.txt 
echo "RUNNING ON artificial9000.csv WITH K 9 Z 300"
python3 G097HW2.py -f artificial9000.csv -k 9 -z 300 &>> out.txt

echo "DONE"