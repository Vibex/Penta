Penta
=====
Penta is a python based WM.
It depends on wm-utils directly and is designed to run on top of a no-wm session.
Below is an example of what a .xinitrc would look like with penta and no-wm.

while ! xprop -root | grep -q Free; do sleep 1; done
xrdb -merge .xresources
xbindkeys
bash "/home/vibex/Documents/penta/mouseFocus.sh" &
bash "/home/vibex/Documents/penta/focusColour.sh" &
bash "/home/vibex/Documents/penta/wewMessanger.sh" &
python2 "/home/vibex/Documents/penta/penta.py" &
exec x-session

Interact
--------
Penta has no direct interaction. It relies on sending messages to a fifo.
Penta then reads though messages and acts upon them.

The messages that Penta currently recognizes are:
* CREATE: wid, x, y, w, h          Adds a window to be managed by Penta.
* DESTROY: wid                     Removes a window being managed by Penta.
* NEXT: wid                        Goes to the next window in the list.
* PREV: wid                        Goes to the prev window in the list.
* WINTAG: wid, tag                 Moves a window to a tag.
* TOGTAG: tag                      Toggels the activation of a tag.
* TILE: mode                       Sets Penta to a tile mode.

Tile
----
Penta currently supports three different tiling modes.
0 = Floating
1 = LStack
2 = Monocole
