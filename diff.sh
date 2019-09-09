# run to compare vm.c and vm.py

./run.sh > a.txt
python3 vm.py > b.txt
echo "and compare..."
diff a.txt b.txt
