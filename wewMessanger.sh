#!/bin/bash
# wewMessanger is an inbetween that receives messages from wew and outputs them to a fifo that penta can read.
# This is just a basic script to do it. You can write your own (because this one is very shitty).

FIFO=${1:-"/tmp/penta.fifo"}
test -p $FIFO || mkfifo $FIFO
# Window Event Watcher
wew -a | while IFS=: read message; do
	event=$(echo $message | cut -d ":" -f 1)
	wid=$(echo $message | cut -d ":" -f 2)
	case $event in
		# You could use a clause like this one to automatically add programs
		# There are some problems with it because it will add even no display windows
		# Instead I use hotkeys to add individual windows to the WM
		# XCB_CREATE_NOTIFY
		# 16) echo "CREATE:$wid" > "$FIFO";;
		# XCB_CREATE_DESTROY
		17) echo "DESTROY:$wid" > "$FIFO";;
	esac
done
