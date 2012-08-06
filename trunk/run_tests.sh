for i in test_data/*.rdt; do 
	echo "--------- $i ----------"; 
	python compd.py --ds=$i --cf=ELAPSED --of1; 
done
