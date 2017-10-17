#!/bin/bash

LINE=''
FLAG=()

for AREA in 10000
#for AREA in 6000 5000 4000 3000 2000 1000
do 
	for SEED in {1..100}
	do
#		for NODE in {2..120}
		for NODE in 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200
		do
			#./main $AREA $NODE $SEED >> output | awk -F $'\t' '{ if ($8 == 1) print $FLAG = $3}' | tee output
			echo "./main $AREA $SEED $NODE" 
                        LINE="$(./main $AREA $SEED $NODE)"
			echo $LINE >> results/$AREA-$NODE.txt
			IFS=$'\t' read -ra FLAG <<< "$LINE"
			if [ ${FLAG[8]} -gt 2 ]
			then
				break
			fi
			if [ ${FLAG[8]} -gt 3 ]
                        then
                                break
                        fi
		done
	done
done
