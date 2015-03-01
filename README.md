Penta
=====
Penta is a python based WM.
It depends on wm-utils directly and is designed to run on top of a no-wm session.

FIFO
----
Penta has no direct interaction. It relies on sending messages to a fifo. Penta then reads those messages and acts upon them.
All messages follow this format. First is the event (in all caps). Then a colon ":". Next comes a set of params. These are all desermined by the specific menu. They are seperated by a comma "," and NOTHING ELSE.

The messages that Penta currently recognizes are:
* CREATE: wid, x, y, w, h = Adds a window to be managed by Penta.
* DESTROY: wid = Removes a window being managed by Penta.
* WINMOVEA: wid, x, y, w, h = Moves a window to an absolute location.
* WINMOVER: wid, x, y, w, h = Moves a window to a realative location.
* WINCORNER: wid, quadrant = Moves a window to a corner of the monitor.
* WINCENTER: wid = Moves a window to the center of the monitor.
* NEXT: wid = Goes to the next window in the list.
* PREV: wid = Goes to the prev window in the list.
* TOGRULE: wid, rule = Applies a rule to a window.
* WINTAG: wid, tag = Moves a window to a tag.
* TOGTAG: tag = Toggels the activation of a tag.
* TILE: mode = Sets Penta to a tile mode.

Tile
----
Penta currently supports three different tiling modes.
* 0 = Floating
* 1 = LStack
* 2 = Monocole

RULES
-----
Rules can be applied to windows and effect how windows are tiled.
* full = full screen the window
* float = makes the window always floating
* psuedo = applys a psuedo tile mode (float size at tiled pos)

TODO
----
* Add manipulation of the list of windows.
* Add the ability to dynamicaly create and destroy tags.
* Add the ability to change the settings on the fly.
* Tinker around with the code to make it more concise and clean.
