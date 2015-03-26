#!/bin/bash
# wewMessanger is an inbetween that receives messages from wew and outputs them to a fifo that penta can read.
# This is just a basic script to do it. You can write your own (because this one is very shitty).

FIFO=${1:-"/tmp/penta.fifo"}
# Window Event Watcher
wew -a | while IFS=: read message; do
	event=$(echo $message | cut -d ":" -f 1)
	wid=$(echo $message | cut -d ":" -f 2)
	case $event in
		# XCB_CREATE_NOTIFY
		# This was the best way I could come up with to add windows when they are created. 
		# At first I tried using just the message from wew, but then you have lots of fake sub windows with programs like firefox.
		# Then I tried checking the windows against the lsw list, but the list is updated slower then wew. 
		# So the best solution was to just retry and add all the windows in lsw when a new window is created.
		# But then I needed to add the sleep command in because the messages were being sent to quickly to the fifo and penta was getting baffled.
		# So here is the solution I have arrived at. Please someone come up with a better solution.
		# Not fond of this solution either, so for now I'm going to go back to manually adding them to be managed.
		#16) for win in $(lsw); do
		#	echo "CREATE:$win, $(wattr x $win), $(wattr y $win), $(wattr w $win), $(wattr h $win)" > "$FIFO"
		#	sleep 0.001
		#done;;
		# echo "CREATE:$wid" > "$FIFO";;
		# XCB_CREATE_DESTROY
		17) echo "DESTROY:$wid" > "$FIFO";;
	esac
done
