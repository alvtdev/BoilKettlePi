import time
from tkinter import *

filename = "output.txt"
bmsg = "test string"

def printOutputs():
	ftxt = open(filename)
	bmsg = ftxt.read()
	ftxt.close()
	out1.configure(text=bmsg)
	bkui.after(1000, printOutputs)


bkui = Tk()
bkui.title("BoilKettlePi")

#bkui_Mainframe = Frame(bkui, padding="3 3 12 12") 
#bkui_Mainframe.grid(column=0, row=0)
#bkui_Mainframe.columnconfigure(1, weight=3)
#bkui_Mainframe.rowconfigure(0, weight=1)


out1 = Message(bkui, text=bmsg)
out1.pack(side=LEFT)
printOutputs()

#bkui.Label(bkui_Mainframe, text=bmsg).grid(column=2, row=2, sticky=E)

bkui.mainloop()
