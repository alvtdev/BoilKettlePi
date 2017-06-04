import time
from tkinter import *

filename = "output.txt"
bmsg = "Waiting for BK"
afterid1 = -1;
afterid2 = -1;

#PAGE NUMBER VAR
#0 = start page
#1 = boil kettle page
#2 = output page
#3 = mash tun page
#4 = MT info sent page
pagenumber = 0;

#Page navigation helper functions
def goToStartPage():
    pagenumber = 0
    #start_page.pack()

def goToBkPage():
    pagenumber = 1
    #bk_page.pack()
    bk_page.tkraise()

def goToOutPage():
    pagenumber = 2
    #out_page.pack()
    printOutputs()
    out_page.tkraise()

def goToMtPage():
    pagenumber = 3
    #mt_page.pack()
    mt_page.tkraise()

def exitbk():
    exit(0)

#Output functions
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


bkui = Tk()
bkui.title("BoilKettlePi")
bkui.columnconfigure(0, weight=1)
bkui.columnconfigure(1, weight=1)
bkui.columnconfigure(2, weight=1) 
#bkui.columnconfigure(3, weight=1)
bkui.rowconfigure(0, weight=1)
bkui.rowconfigure(1, weight=1)
bkui.rowconfigure(2, weight=1)
#bkui.rowconfigure(3, weight=1)

#declare pages
start_page = Frame(bkui)
bk_page = Frame(bkui) 
mt_page = Frame(bkui)
out_page = Frame(bkui)
mtSent_page = Frame(bkui)

#init config for all pages
for frame in (start_page, bk_page, mt_page):
    frame.grid(row=0, column=0, sticky=(N, S, E, W))
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1) 
#    frame.columnconfigure(3, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
#    frame.rowconfigure(3, weight=1)


#exit button
exitStart = Button(start_page, text='Exit', command=exitbk)
exitBK = Button(bk_page, text='Exit', command=exitbk)
exitOut = Button(out_page, text='Exit', command=exitbk)
exitMT = Button(mt_page, text='Exit', command=exitbk)

#START PAGE
startmsg = Message(start_page, text="Welcome to BoilKettlePi", width=10000)
MTconfig = Button(start_page, text="MashTun Settings", command=goToMtPage)
BTconfig = Button(start_page, text="BoilKettle Settings", command=goToBkPage)
startmsg.grid(row=2, column=1)
MTconfig.grid(row=3, column=0)
BTconfig.grid(row=3, column=1)
exitStart.grid(row=3, column=2)

#BOIL KETTLE PAGE
Start = Button(bk_page, text="Start Boil", command=goToOutPage)
out1 = Message(bk_page, text=bmsg, width = 10000)

out1.grid(row=2, column=1)
Start.grid(row=3, column=0)
exitBK.grid(row=3, column=2)

#output page
outmsg = Message(out_page, text=bmsg, width=10000)
outmsg.grid(row=2, column=2)
exitOut.grid(row=3, column=2)


#MT PAGE
exitMT.grid(row=3, column=2)

start_page.tkraise()
bkui.mainloop()
