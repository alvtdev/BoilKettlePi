import time
from tkinter import *

filename = "output.txt"
bmsg = "Welcome to BoilKettlePi"
afterid1 = -1;
afterid2 = -1;
pauseflag = -1;

def pause():
	pauseflag = 1;

def start():
	pauseflag = -1;

def manUpdate():
	ftxt = open(filename)
	bmsg = ftxt.read()
	ftxt.close()
	out1.configure(text=bmsg)

def printOutputsLoop():
	ftxt = open(filename)
	bmsg = ftxt.read()
	ftxt.close()
	out1.configure(text=bmsg)
	bkui.after_cancel(afterid2)
	afterid2 = bkui.after(1000, printOutputsLoop)

def printOutputs():
	ftxt = open(filename)
	bmsg = ftxt.read()
	ftxt.close()
	out1.configure(text=bmsg)
	afterid1 = bkui.after(1000, printOutputs)
	
def exitbk():
	exit(0)

def die():
	bmsg = "BoilKettlePi is kill."
	out1.configure(text=bmsg)
	bkui.after_cancel(afterid1)
	bkui.after_cancel(afterid2)


bkui = Tk()
bkui.title("BoilKettlePi")


bkui_Mainframe = Frame(bkui) 
bkui_Mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
bkui_Mainframe.columnconfigure(1, weight=3)
bkui_Mainframe.rowconfigure(0, weight=1)

#manualUpdate = Button(bkui_Mainframe, text='Update', command=manUpdate)
Start = Button(bkui_Mainframe, text="Start", command=printOutputs)
Exit = Button(bkui_Mainframe, text='Exit', command=exitbk)
Pause = Button(bkui_Mainframe, text='Pause', command=die)
out1 = Message(bkui_Mainframe, text=bmsg, width = 10000)

out1.grid(row=1, column=1)
Start.grid(row=2, column=0)
Exit.grid(row=2, column=2)
Pause.grid(row=2, column=1)
#manualUpdate.grid(row=1, column=3)
#printOutputs()
#bkui.Label(bkui_Mainframe, text=bmsg).grid(column=2, row=2, sticky=E)

bkui.mainloop()
