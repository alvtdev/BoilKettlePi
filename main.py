import time
from tkinter import *

outputFile = "output.txt"
bmsg = "Waiting for BK"
afterid1 = -1;
afterid2 = -1;

#mash time var
mTime = None
mTemp1 = None
mTemp2 = None 

#PAGE NUMBER VAR
#0 = menu page
#1 = boil kettle page
#2 = output page
#3 = mash tun page
#4 = MT info sent page
pagenumber = 0;

#Output functions
def printOutputs():
    ftxt = open(outputFile, "r+")
    bmsg = ftxt.read()
    ftxt.close()
    outmsg.configure(text=bmsg)
    afterid1 = bkui.after(1000, printOutputs)

#Mash Tun Menu Functions 
def getMashData():
    global mTime
    global mTemp1
    global mTemp2
    mTime = mashTimeEntry.get()
    mTemp1 = mashTemp1Entry.get()
    mTemp2 = mashTemp2Entry.get()
    mTimeString.set(mTime)
    mTemp1String.set(mTemp1)
    mTemp2String.set(mTemp2)
    file = open('mashtun.txt', 'w+')
    file.write("Mash time: %s \n" % mTime)
    file.write("Mash temp1: %s \n" % mTemp1)
    file.write("Mash temp2: %s \n" % mTemp2)
    file.close()
    #print(mTime)
    #print(mTemp1)
    #print(mTemp2)

#Page navigation helper functions
def goToMenuPage():
    pagenumber = 0
    menu_page.tkraise()

def goToBkPage():
    pagenumber = 1
    bk_page.tkraise()

def goToOutPage():
    pagenumber = 2
    printOutputs()
    out_page.tkraise()

def goToMtPage():
    pagenumber = 3
    mt_page.tkraise()

def goToMtSentPage():
    pagenumber = 4
    getMashData()
    mtSent_page.tkraise()

def exitbk():
    bkui.quit()
    exit(0)


bkui = Tk()
bkui.title("BoilKettlePi")
#init bkui config to account for resizing
bkui.columnconfigure(0, weight=1)
bkui.columnconfigure(1, weight=1)
bkui.columnconfigure(2, weight=1) 
bkui.columnconfigure(3, weight=1)
bkui.columnconfigure(4, weight=1)
bkui.rowconfigure(0, weight=1)
bkui.rowconfigure(1, weight=1)
bkui.rowconfigure(2, weight=1)
bkui.rowconfigure(3, weight=1)
bkui.rowconfigure(4, weight=1)

#declare pages
menu_page = Frame(bkui)
bk_page = Frame(bkui) 
mt_page = Frame(bkui)
out_page = Frame(bkui)
mtSent_page = Frame(bkui)

#init config for all pages
for frame in (menu_page, bk_page, out_page, mt_page, mtSent_page):
    frame.grid(row=0, column=0, sticky=(N, S, E, W))
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1) 
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)

#MENU PAGE
mtConfig = Button(menu_page, text="MashTun Settings", command=goToMtPage)
btConfig = Button(menu_page, text="BoilKettle Settings", command=goToBkPage)
exitMenu = Button(menu_page, text='Exit', command=exitbk)
menuMsg = Message(menu_page, text="Welcome to BoilKettlePi", width=10000)

mtConfig.grid(row=3, column=0)
btConfig.grid(row=3, column=1)
exitMenu.grid(row=3, column=2)
menuMsg.grid(row=2, column=1)

#BOIL KETTLE PAGE
startBoil = Button(bk_page, text="Start Boil", command=goToOutPage)
btsBK = Button(bk_page, text='Menu', command=goToMenuPage)
exitBK = Button(bk_page, text='Exit', command=exitbk)
bkSettings = Message(bk_page, text="BoilKettle Settings", width = 10000)

bkSettings.grid(row=0, column=1)
btsBK.grid(row=4, column=0)
startBoil.grid(row=4, column=1)
exitBK.grid(row=4, column=2)

#output page
exitOut = Button(out_page, text='Exit', command=exitbk)
outmsg = Message(out_page, text=bmsg, width=10000)

outmsg.grid(row=2, column=1)
exitOut.grid(row=4, column=2)

#MT PAGE
mtSettings = Label(mt_page, text="Mash Tun Settings:")
mashTime = Label(mt_page, text="Mash Time:")
mashTimeEntry = Entry(mt_page)
mashTimeUnits = Label(mt_page, text="minutes")
#mTime = mashTimeEntry.get()
mashTemp1 = Label(mt_page, text="Mash Temperature:")
mashTemp1Entry = Entry(mt_page)
mashTemp1Units = Label(mt_page, text="\xb0F")
#mTemp1 = mashTemp1Entry.get()
mashTemp2 = Label(mt_page, text="Mash Temperature:")
mashTemp2Entry = Entry(mt_page)
mashTemp2Units = Label(mt_page, text="\xb0F")
#mTemp2 = mashTemp2Entry.get()
btsMT = Button(mt_page, text='Menu', command=goToMenuPage)
sendMTData = Button(mt_page, text="Send to Mash Tun", command=goToMtSentPage)
exitMT = Button(mt_page, text='Exit', command=exitbk)

mtSettings.grid(row=0, column=1)
mashTime.grid(row=1, column=0)
mashTimeEntry.grid(row=1, column=1) 
mashTimeUnits.grid(row=1, column=2)
mashTemp1.grid(row=2, column=0)
mashTemp1Entry.grid(row=2, column=1)
mashTemp1Units.grid(row=2, column=2)
mashTemp2.grid(row=3, column=0)
mashTemp2Entry.grid(row=3, column=1)
mashTemp2Units.grid(row=3, column=2)
btsMT.grid(row=4, column=0)
sendMTData.grid(row=4, column=1)
exitMT.grid(row=4, column=2)

#MT SENT PAGE
#stringvars to store display user input
mTimeString = StringVar()
mTemp1String = StringVar()
mTemp2String = StringVar()
btsMTSent = Button(mtSent_page, text='Menu', command=goToMenuPage)
mtSentMsg = Message(mtSent_page, text="MT Info Sent:", width=10000)
mtSentTime = Label(mtSent_page, text="Mash Time:")
mtSentTimeEntry = Label(mtSent_page, textvariable=mTimeString)
mtSentTimeUnits = Label(mtSent_page, text="minutes")
mtSentTemp1 = Label(mtSent_page, text="Mash Temperature:")
mtSentTemp1Entry = Label(mtSent_page, textvariable=mTemp1String)
mtSentTemp1Units = Label(mtSent_page, text="\xb0F")
mtSentTemp2 = Label(mtSent_page, text="Mash Temperature:")
mtSentTemp2Entry = Label(mtSent_page, textvariable=mTemp2String)
mtSentTemp2Units = Label(mtSent_page, text="\xb0F")

mtSentMsg.grid(row=0, column=1)
mtSentTime.grid(row=1, column=0)
mtSentTimeEntry.grid(row=1, column=1)
mtSentTimeUnits.grid(row=1, column=2)
mtSentTemp1.grid(row=2, column=0)
mtSentTemp1Entry.grid(row=2, column=1)
mtSentTemp1Units.grid(row=2, column=2)
mtSentTemp2.grid(row=3, column=0)
mtSentTemp2Entry.grid(row=3, column=1)
mtSentTemp2Units.grid(row=3, column=2)
btsMTSent.grid(row=4, column=1)


menu_page.tkraise()
bkui.mainloop()
