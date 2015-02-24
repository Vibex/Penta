#!/bin/python2
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
##### END



##### CLASSES
class Window:
    def __init__(self, wid, tag=0, x=0, y=0, w=1000, h=800):
        # Unique Window ID
        self.wid = wid

        # Tag that the window is stored on
        self.tag = tag

        # Current Geometry of the window
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Floating Geometry of the window
        self.floatX = x
        self.floatY = y
        self.floatW = w
        self.floatH = h

    def __repr__(self):
        return self.wid + "_" + "(" + str(self.x) + "," + str(self.y) + "," + str(self.w) + "," + str(self.h) + ")"

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
        return self.positionA(self.x + x, self.y + y, self.w + w, self.h + h, set)

    # Moves the window to it's default position (the position stored in itself).
    # Returns the new position of the window.
    def float(self):
        return self.positionA(self.floatX, self.floatY, self.floatW, self.floatH)
    
    # Places the window outside of the screens borders.
    # Returns the new position of the window.
    def hide(self, monW):
        return self.positionA(monW, 0, max(self.floatW, self.w), max(self.floatH, self.h))

    # Focus the window and bring it to the top of the stack. Also place the cursor in the bottom right corner.
    def focus(self):
        call(["chwso", "-r", self.wid])
        call(["wmp", str(self.x + self.w), str(self.y + self.h)])
        call(["wtf", self.wid])
    
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


class Manager:
    def __init__(self, fifo, output, monw, monh, master, tbar, bbar, bor, wingap, mongap):
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

        # A List of all the Windows that are being managed
        self.low=[]

        # A list of all the tags in the wm.
        self.tags=[True, False, False, False, False]

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
            self.interpret(message)
    
    # NOT MEANT TO BE CALLED ON ITS OWN, NOT EVEN REALLY SURE WHY IT IS ITS OWN FUNCTION.
    # Takes the info from the read function and acts upon it.
    def interpret(self, message):
        # If the message is not formated properly then output an error.
        # Otherwise act on the message.
        try:
            event = message.split(':')[0]
            data = message.split(':')[1]
            print message
        except:
            print "ERROR WITH MESSAGE:  '" + message + "'"
            return
        # If it was a create message and the window is not in the list yet, then add it to the low.
        if event == "CREATE":
            try:
                data1 = data.split(',')[0]
                data2 = data.split(',')[1]
                data3 = data.split(',')[2]
                data4 = data.split(',')[3]
                data5 = data.split(',')[4]
            except:
                print "ERROR WITH MESSAGE:  '" + message + "'"
                return
            # Check if its already in the list.
            if self.inListAt(data1) == -1:
                # Place the window on the lowest numbered active tag.
                count = 0
                found = False
                for tag in self.tags:
                    if tag:
                        found = True
                        break
                    count += 1
                # If no tags are active then send it to the first tag.
                if not found:
                    count = 0
                win = Window(data1, count, data2, data3, data4, data5)
                self.low.append(win)
                self.retile()
        # If it was a destroy message, and the window is in the low, then remove it.
        elif event == "DESTROY":
            place = self.inListAt(data)
            if place != -1:
                self.low.pop(place)
                self.retile()
        # If it was a next message switch focus to the next window.
        elif event == "NEXT":
            self.next(data)
        # If it was a prev message switch focus to the prev window.
        elif event == "PREV":
            self.prev(data)
        # If it was a wintag message then send a window to a tag.
        elif event == "WINTAG":
            try:
                data1 = data.split(',')[0]
                data2 = data.split(',')[1]
            except:
                print "ERROR WITH MESSAGE:  '" + message + "'"
                return
            # Check to see if the window is in the list.
            place = self.inListAt(data1)
            if place != -1:
                self.low[place].setTag(int(data2))
            self.retile()
        elif event == "TOGTAG":
                self.togTag(int(data))
                self.retile()
        elif event == "TILE":
            # Change the tile method
            self.tiled = int(data)
            # Retile everything
            self.retile()
    
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
        workingList = self.workWithWins()
        otherList = self.otherWins()
        for win in otherList:
            win.hide(self.monw)
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
                        x1 = x
                        y1 = y
                        w1 = self.master - (self.bor * 2)
                        h1 = h - (self.bor * 2)
                        win.positionA(x1, y1, w1, h1)
                        # Create the geometry for the sub windows
                        x2 = x + w1 + (self.bor * 2) + self.wingap
                        y2 = y
                        w2 = w - w1 - self.wingap - self.mongap
                        h2 = (h - ((len(low) - 2) * self.wingap)) / (len(low) - 1) - (self.bor * 2)
                        count = 0
                        first = False
                    else:
                        # Place the sub windows
                        win.positionA(x2, y2 + (count * (h2 + (self.wingap * 2))), w2, h2)
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

##### MAIN FUNCTION
def Main(fifo, output, monw, monh, master, tbar, bbar, bor, wingap, mongap):
    man = Manager(fifo, output, monw, monh, master, tbar, bbar, bor, wingap, mongap)
    while True:
        man.read()
        man.write()

##### CALL MAIN
Main(FIFO, OUTPUT, MONW, MONH, MASTER, TBAR, BBAR, BOR, WINGAP, MONGAP)
