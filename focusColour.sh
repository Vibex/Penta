#!/bin/bash
bor=2
while true; do
	for win in $(lsw); do
		if [ $win == $(pfw) ]; then
			chwb -s $bor -c "0xaf99bf" $win
			continue
		fi
		chwb -s $bor -c "0x373a3f" $win
	done
done
