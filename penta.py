#!/bin/python2
import subprocess
from subprocess import call

##### CONFIG
# This is the fifo that penta reads from. No real need to change it.
# If you do change it though you must change it in wewMessanger too.
FIFO = "/tmp/penta.fifo"
# Sets the file that penta writes data too.
OUTPUT = "/tmp/penta_out"
# The width of your monitor. I could grab this, but setting it allows for a bit more control. (plus I'm lazy)
MONW = 1920
# The height of your monitor. I could grab this, but setting it allows for a bit more control. (plus I'm lazy)
MONH = 1080
# This is the width of the master window when tiled.
MASTER = 1200
# This is the height of your taskbar on the top of your monitor (if you have one).
TBAR = 22
# This is the height of your taskbar on the bottom of your monitor (if you have one).
BBAR = 0
# This is the borders on your windos.
BOR = 2
# This is the gap between your windows.
WINGAP = 8
# This is the gap between the window and the edge of the screen.
MONGAP = 16
# This is the number of tags that Penta manages.
TAGNUM = 5
##### END


##### CLASSES
class Window:
    def __init__(self, wid, tag, rule="none"):
        # Unique Window ID
        self.wid = wid

        # Tag that the window is stored on
        self.tag = tag

        # Current Geometry of the window
        self.x = int(subprocess.Popen(["wattr", "x", wid], stdout=subprocess.PIPE).communicate()[0][:-1])
        self.y = int(subprocess.Popen(["wattr", "y", wid], stdout=subprocess.PIPE).communicate()[0][:-1])
        self.w = int(subprocess.Popen(["wattr", "w", wid], stdout=subprocess.PIPE).communicate()[0][:-1])
        self.h = int(subprocess.Popen(["wattr", "h", wid], stdout=subprocess.PIPE).communicate()[0][:-1])

        # Floating Geometry of the window
        self.floatX = self.x
        self.floatY = self.y
        self.floatW = self.w
        self.floatH = self.h

        # Rules for the window
        self.rule = rule

    # Representation of a window. This is what is outputed to the output file
    def __repr__(self):
        return self.wid + "_" + str(self.tag) + "_(" + str(self.x) + "," + str(self.y) + "," + str(self.w) + "," + str(self.h) + ")_" + self.rule

    # Int Int Int Int -> [Int, Int, Int, Int]
    # Takes in geometry cordinates and places the window at that location.
    # If the float variable is set to true then penta will save the geometry for floating the window.
    # Returns the new position of the window.
    def positionA(self, x, y, w, h, float=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if float:
            self.floatX = x
            self.floatY = y
            self.floatW = w
            self.floatH = h
        call(["wtp", str(x), str(y), str(w), str(h), self.wid])
        return [x, y, w, h]

    # Int Int Int Int -> [Int, Int, Int, Int]
    # Takes in geometry offsets and moves the window in relation to them.
    # Returns the new position of the window.
    def positionR(self, x=0, y=0, w=0, h=0, float=False):
        return self.positionA(self.x + x, self.y + y, self.w + w, self.h + h, float)

    # Moves the window to it's default position (the position stored in itself).
    # Returns the new position of the window.
    def float(self):
        return self.positionA(self.floatX, self.floatY, self.floatW, self.floatH)
    
    # Set the map setting of the window
    # Setting is one of u (unmap), m (map), or t (toggle)
    def map(self, setting):
        call(["mapw", "-" + setting, self.wid])

    # Int, Int, Int, Int, Int -> [Int, Int, Int, Int]
    # Place a window in a corner
    def corner(self, corner, tbar, bbar, monw, monh):
        x = 0
        y = tbar
        if corner == 1 or corner == 4:
            x = monw - self.floatW
        if corner == 3 or corner == 4:
            y = monh - self.floatH - bbar
        return self.positionA(x, y, self.floatW, self.floatH, True)
    
    # Center a window on an area
    # Returns the new position of the window.
    def psuedo(self, x, y, w, h, float=False):
        x = x + (w / 2) - (self.floatW / 2)
        y = y + (h / 2) - (self.floatH / 2)
        return self.positionA(x, y, self.floatW, self.floatH, float)

    # Focus the window and bring it to the top of the stack. Also place the cursor in the bottom right corner.
    def focus(self):
        call(["chwso", "-r", self.wid])
        self.mouseCorner()
        call(["wtf", self.wid])

    # Place the cursor in the bottom corner of the window
    def mouseCorner(self):
        call(["wmp", str(self.x + self.w), str(self.y + self.h)])

    # String(or Int) String -> None
    # The first string must be a number.
    # The second string must be a coulour code.
    # Set the border on the window.
    def border(self, size, colour):
        call(["chwb", "-s", str(size), "-c", colour, self.wid])
    
    # String -> Boolean
    # Returns if the wid of this is the same as that.
    def equal(self, wid):
        return self.wid == wid
    
    # Int -> Boolean
    # Returns if the window is on the tag.
    def inTag(self, tag):
        return self.tag == tag

    # Int -> 
    # Sets the current tag for the window.
    def setTag(self, tag):
        self.tag = tag

    # String -> 
    # Toggles a rule of the window
    def setRule(self, setrule):
        self.rule = setrule

    # String -> boolean
    # Checks if the window has a rule set
    def checkRule(self, checkrule):
        return self.rule == checkrule


class Manager:
    def __init__(self, fifo, output, monw, monh, master, tbar, bbar, bor, wingap, mongap, tagnum):
        self.fifo = fifo
        self.output = output
        self.monw = monw
        self.monh = monh
        self.master = master
        self.tbar = tbar
        self.bbar = bbar
        self.bor = bor
        self.wingap = wingap
        self.mongap = mongap
        self.tagnum = tagnum

        # A List of all the Windows that are being managed
        self.low=[]

        # A list of all the tags in the wm.
        self.tags = []
        first = True
        for count in range(self.tagnum):
            if first:
                add = True
                first = False
            else:
                add = False
            self.tags.append(add)

        # This variable represents what tiling mode is currently active.
        # 0 = Float
        # 1 = LStack
        # 2 = Monocole
        self.tiled = 1

    # Writes the current state of penta to the output file
    def write(self):
        out = open(self.output, "w")
        tagOut = "TAGS:"
        tileOut = "TILE: " + str(self.tiled) + "\n"
        for tag in self.tags:
            if tag:
                tagOut += " 1"
            else:
                tagOut += " 0"
        tagOut += "\n"
        out.write(tagOut)
        out.write(tileOut)
        out.write("MANAGED_WINDOWS:\n")
        for win in self.low:
            out.write(win.__repr__() + "\n")
        out.close()
    
    # String -> Int
    # Checks to see if a window is in the low.
    # Returns the position of the window in that list. If the window is not in the list, it returns -1.
    def inListAt(self, wid):
        count = 0
        for win in self.low:
            if win.equal(wid):
                return count
            count += 1
        return -1

    # Reads information out of the fifo.
    # Does actions based on the output (the actions are run by the interpret function).
    def read(self):
        with open(self.fifo) as fd:
            message = fd.read().strip()
            return self.interpret(message)
    
    # NOT MEANT TO BE CALLED ON ITS OWN, NOT EVEN REALLY SURE WHY IT IS ITS OWN FUNCTION.
    # Takes the info from the read function and acts upon it.
    def interpret(self, message):
        stop = False
        # fail if to much input from the fifo
        if "\n" in message:
            print "Error with:  '" + message + "'"
            print "Most likely caused by an overflow in the fifo."
            return stop
        # Split the message into its parts
        j = message.split(':')
        event = j[0]
        data = j[1]
        print message
        # If it was a create message and the window is not in the list yet, then add it to the low.
        if event == "CREATE":
            win = self.createWindow(data)
            self.retile()
            win.focus()

        # If it was a destroy message, and the window is in the low, then remove it.
        elif event == "DESTROY":
            place = self.inListAt(data)
            if place != -1:
                self.low.pop(place)
                focus = False
                for win in self.low:
                    winPlace = self.inListAt(win.wid)
                    if winPlace == place or winPlace == place - 1:
                        focus = win
                self.retile()
                if focus:
                    focus.focus()

        # If it was a movewina message then move the window to an absolute position
        elif event == "WINMOVEA":
            n = data.split(',')
            wid = n[0]
            x = n[1]
            y = n[2]
            w = n[3]
            h = n[4]
            
            win = self.setWindow(wid)
            if self.tiled != 0 and not win.checkRule('float'):
                win.setRule('float')
            win.positionA(int(x), int(y), int(w), int(h), True)
            win.mouseCorner()
            self.retile()
        
        # If it was a movewinr message then move the window relative to the win
        elif event == "WINMOVER":
            n = data.split(',')
            wid = n[0]
            x = n[1]
            y = n[2]
            w = n[3]
            h = n[4]
            
            win = self.setWindow(wid)
            if self.tiled != 0 and not win.checkRule('float'):
                win.setRule('float')
            win.positionR(int(x), int(y), int(w), int(h), True)
            win.mouseCorner()
            self.retile()

        # If it was a movecorner message then move the window to a corner of the monitor
        elif event == "WINCORNER":
            n = data.split(',')
            wid = n[0]
            cor = n[1]
            
            win = self.setWindow(wid)
            if self.tiled != 0 and not win.checkRule('float'):
                win.setRule('float')
            win.corner(int(cor), self.tbar, self.bbar, self.monw - (self.bor * 2), self.monh - (self.bor * 2))
            win.mouseCorner()
            self.retile()

        # If it was a wincenter message then center the window on the monitor
        elif event == "WINCENTER":
            place = self.inListAt(data)
            x, y, w, h = self.basics()
            win = self.setWindow(data)
            if self.tiled != 0 and not win.checkRule('float'):
                win.setRule('float')
            win.psuedo(x - self.bor, y - self.bor, w, h, True)
            win.mouseCorner()
            self.retile()

        # If it was a next message switch focus to the next window.
        elif event == "NEXT":
            self.next(data)

        # If it was a prev message switch focus to the prev window.
        elif event == "PREV":
            self.prev(data)

        # If it was a togrule message it toggles the rule state on the window
        elif event == "TOGRULE":
            n = data.split(',')
            wid = n[0]
            rule = n[1]
            
            win = self.setWindow(wid)
            if win.checkRule(rule):
                win.setRule("none")
            else:
                win.setRule(rule)
            self.retile()

        # If it was a wintag message then send a window to a tag.
        elif event == "WINTAG":
            n = data.split(',')
            wid = n[0]
            tag = n[1]
            
            # Check to see if the window is in the list.
            win = self.setWindow(wid)
            win.setTag(int(tag))
            self.retile()
        
        # If it was a togtag message it toggles the state of the tag
        elif event == "TOGTAG":
            self.togTag(int(data))
            self.retile()
        
        elif event == "ONETAG":
            self.oneTag(int(data))
            self.retile()
    
        # If it wasa tile message it changes the toggle state of the window
        elif event == "TILE":
            # Change the tile method
            self.tiled = int(data)
            # Retile everything
            self.retile()
        return stop

    # Get a window in the list of windows, if it doesn't exist create it
    # Can also set a tag for the gotten window and a rule
    def setWindow(self, wid, tag=-1, rule=-1):
        place = self.inListAt(wid)
        if place == -1:
            win = self.createWindow(wid, tag, rule)
        else:
            win = self.low[place]
        if tag != -1:
            win.setTag(tag)
        if rule != -1:
            win.setRule(rule)
        return win

    # create a window
    # String Int Rules -> Window
    def createWindow(self, wid, tag=-1, rule="none"):
        if tag == -1:
            # Place the window on the lowest numbered active tag.
            tag = 0
            found = False
            for checkTag in self.tags:
                if checkTag:
                    found = True
                    break
                tag += 1
            # If no tags are active then send it to the first tag.
            if not found:
                tag = 0
        win = Window(wid, tag, rule)
        self.low.append(win)
        return win

    # Returns a list of all windows that are on operational tags.
    def workWithWins(self):
        workingList = []
        for win in self.low:
            count = 0
            for tag in self.tags:
                if tag and win.inTag(count):
                    workingList.append(win)
                    break
                count += 1
        return workingList

    # Returns a list of all windows that are not on operational tags.
    def otherWins(self):
        workingList = []
        for win in self.low:
            count = 0
            for tag in self.tags:
                if not tag and win.inTag(count):
                    workingList.append(win)
                    break
                count += 1
        return workingList

    # String Boolean -> None
    # Changes the current selected window to one in the given direction.
    def change(self, wid, forward):
        list = self.workWithWins()
        if not forward:
            list = reversed(list)
        found = False
        for win in list:
            if found:
                win.focus()
                break
            if win.equal(wid):
                found = True
    
    # String -> None
    # Changes focus to the next window in the low.
    def next(self, wid):
        self.change(wid, True)
    
    # String -> None
    # Changes focus to the prev window in the low.
    def prev(self, wid):
        self.change(wid, False)
    
    # Retiles the windows.
    def retile(self):
        # Split the low into two lists based on their use
        workingList = self.workWithWins()
        otherList = self.otherWins()
        # Hide all wins that aren't going to be tiled
        for win in otherList:
            win.map("u")
        # If the win has the float rule set, then float it
        # If the win has the full rule set, then fullscreen it
        # Then remove it from the tile list
        count = 0
        for win in workingList:
            win.map("m")
            if win.checkRule('full'):
                workingList.pop(count)
                win.positionA(0 - self.bor, 0 - self.bor, self.monw, self.monh)
            elif win.checkRule('float'):
                workingList.pop(count)
                win.float()
            count += 1
        # Tile the rest of the windows based on the tile mode
        if self.tiled == 1:
            # LStack
            self.lStack(workingList)
        elif self.tiled == 2:
            # Monocole
            self.monocole(workingList)
        else:
            # Float
            self.float(workingList)

    # -> [Int, Int]
    # Returns a list of the starting positons of the window.
    def startPos(self):
        startX = 0 + self.mongap
        startY = 0 + self.mongap + self.tbar
        return [startX, startY] 

    # -> [Int, Int]
    # Returns a list of the maximum size of the window.
    def maxSize(self):
        maxW = self.monw - (self.mongap * 2)
        maxH = self.monh - (self.mongap * 2) - self.tbar - self.bbar
        return [maxW, maxH]
    
    # -> [Int, Int, Int, Int]
    # Calls both startPos and maxSize.
    def basics(self):
        x, y = self.startPos()
        w, h = self.maxSize()
        return [x, y, w, h]
    
    # Places all windows as if they were maximum size.
    def monocole(self, low):
        x, y, w, h = self.basics()
        if low != []:
            for win in low:
                if win.checkRule('psuedo'):
                    win.psuedo(x, y, w, h)
                else:
                    win.positionA(x, y, w - (self.bor * 2), h - (self.bor * 2))

    # Places all windows in the lstack formation.
    def lStack(self, low):
        first = True
        x, y, w, h = self.basics()
        if low != []:
            if len(low) == 1:
                self.monocole(low)
            else:
                for win in low:
                    # If first set master window
                    if first:
                        twins = len(low)
                        x1 = x
                        y1 = y
                        w1 = self.master - (self.bor * 2)
                        h1 = h - (self.bor * 2)
                        if win.checkRule('psuedo'):
                            win.psuedo(x1, y1, w1, h1)
                        else:
                            win.positionA(x1, y1, w1, h1)
                        # Create the geometry for the sub windows
                        x2 = x + w1 + (self.bor * 2) + self.wingap
                        y2 = y
                        w2 = w - w1 - (self.wingap * 2)
                        h2 = (h - ((twins - 2) * self.wingap)) / (twins - 1) - (self.bor * 2)
                        count = 0
                        first = False
                    else:
                        # Place the sub windows
                        if win.checkRule('psuedo'):
                            win.psuedo(x2, y2 + (count * (h2 + (self.wingap * 1.5))), w2, h2)
                        else:
                            win.positionA(x2, y2 + (count * (h2 + (self.wingap * 1.5))), w2, h2)
                        count += 1
    
    # Places all windows in there float positons.
    def float(self, low):
        for win in low:
            win.float()

    # Toggles the tags state.
    def togTag(self, tag):
        count = 0
        for j in self.tags:
            if count == tag:
                self.tags[count] = not self.tags[count]
                return
            count += 1

    def oneTag(self, tag):
        count = 0
        for j in self.tags:
            if count == tag:
                self.tags[count] = True
            else:
                self.tags[count] = False
            count += 1

##### MAIN FUNCTION
def Main(fifo, output, monw, monh, master, tbar, bbar, bor, wingap, mongap, tagnum):
    # rm the fifo so that it doesn't receive any broken calls from a previous run.
    call(["rm", fifo])
    # remake the fifo so that it can start receiving input again.
    call(["mkfifo", fifo])
    # Create the manager
    man = Manager(fifo, output, monw, monh, master, tbar, bbar, bor, wingap, mongap, tagnum)
    # start the while loop
    stop = False
    while not stop:
        # Write to the output
        man.write()
        # Read from the output
        stop = man.read()

##### CALL MAIN
Main(FIFO, OUTPUT, MONW, MONH, MASTER, TBAR, BBAR, BOR, WINGAP, MONGAP, TAGNUM)
