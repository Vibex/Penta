#!/bin/bash
bor=2
while true; do
	for win in $(lsw); do
		if [ $win == $(pfw) ]; then
			chwb -s $bor -c "0x9696bc" $win
			continue
		fi
		chwb -s $bor -c "0x747c84" $win
	done
done
