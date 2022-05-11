#!/bin/bash
echo "RUNNING THE PYTHON SCRIPT PROGRAMMATICALLY"
echo "RESULTS WILL BE PRONTED TO out.txt"

if [ -s out.txt ]; then
    echo "REMOVING OLD RESULTS"
    rm -f out.txt
fi
touch out.txt

python G097HW2.py -f artifical9000.csv -k 9 -z 0 &>> out.txt
echo "" >> out.txt 
python G097HW2.py -f artifical9000.csv -k 9 -z 200 &>> out.txt
echo "" >> out.txt 
python G097HW2.py -f artifical9000.csv -k 9 -z 300 &>> out.txt
echo "DONE"