#!/bin/bash
echo "RUNNING THE PYTHON SCRIPT PROGRAMMATICALLY"
echo "RESULTS WILL BE PRONTED TO out2.txt"

touch out2.txt

echo "RUNNING ON testdataHW3.csv WITH K 3 Z 0 L 8"
python3 G097HW3.py testdataHW3.csv 3 0 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON testdataHW3.csv WITH K 3 Z 1 L 8"
python3 G097HW3.py testdataHW3.csv 3 1 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON testdataHW3.csv WITH K 3 Z 3 L 8"
python3 G097HW3.py testdataHW3.csv 3 3 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON uber-small.csv WITH K 10 Z 0 L 8"
python3 G097HW3.py uber-small.csv 10 0 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON uber-small.csv WITH K 10 Z 100 L 8"
python3 G097HW3.py uber-small.csv 10 100 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON artificial9000.csv WITH K 9 Z 0 L 8"
python3 G097HW3.py artificial9000.csv 9 0 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON artificial9000.csv WITH K 9 Z 200 L 8"
python3 G097HW3.py artificial9000.csv 9 200 8 &>> out2.txt
echo "" >> out2.txt 
echo "RUNNING ON artificial9000.csv WITH K 9 Z 300 L 8"
python3 G097HW3.py artificial9000.csv 9 300 8 &>> out2.txt

echo "DONE"