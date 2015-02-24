while true; do
	focus="null"
	for wid in $(lsw); do
		wmp=$(wmp)
		wattr=$(wattr xywh $wid)
		mx=$(echo $wmp | cut -d " " -f 1)
		my=$(echo $wmp | cut -d " " -f 2)
		wx1=$(echo $wattr | cut -d " " -f 1)
		wy1=$(echo $wattr | cut -d " " -f 2)
		ww=$(echo $wattr | cut -d " " -f 3)
		wh=$(echo $wattr | cut -d " " -f 4)
		wx2=$((wx1 + ww)) 
		wy2=$((wy1 + wh))
		if [ "$wx1" -le "$mx" ] && [ "$mx" -le "$wx2" ]; then
			if [ "$wy1" -le "$my" ] && [ "$my" -le "$wy2" ]; then
				focus=$wid
			fi
		fi

	done
	if [ $focus != "null" ]; then
		wtf $focus
		#chwso -r $focus
	fi
done
