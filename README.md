Penta
=====
Penta is a python based WM.
It depends on wm-utils directly and is designed to run on top of a no-wm session.

Interact
--------
Penta has no direct interaction. It relies on sending messages to a fifo.
Penta then reads though messages and acts upon them.

The messages that Penta currently recognizes are:
* CREATE: wid, x, y, w, h          Adds a window to be managed by Penta.
* DESTROY: wid                     Removes a window being managed by Penta.
* NEXT: wid                        Goes to the next window in the list.
* PREV: wid                        Goes to the prev window in the list.
* TOGRULE: wid, rule               Applies a rule to a window.
* WINTAG: wid, tag                 Moves a window to a tag.
* TOGTAG: tag                      Toggels the activation of a tag.
* TILE: mode                       Sets Penta to a tile mode.

Tile
----
Penta currently supports three different tiling modes.
* 0 = Floating
* 1 = LStack
* 2 = Monocole

RULE
----
Rules can be applied to windows and effect how windows are tiled.
* full = full screen the window
* float = makes the window always floating
* psuedo = applys a psuedo tile mode (float size at tiled pos)
