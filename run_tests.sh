for i in test_data/*.rdt; do 
	echo "--------- $i ----------"; 
	python compd.py --ds1=$i --ds2=$i --cf=ELAPSED; 
done
