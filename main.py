import time
import os
import subprocess
from tkinter import *

outputFile = "output.txt"
bmsg = "Waiting for BK"
afterid1 = -1;
afterid2 = -1;

#mash time var
mTime = None
mTemp1 = None
mTemp2 = None 

#boil time var
bTotalTime = None
bTime1 = None
bTime2 = None
bTime3 = None

#process var
global proc
proc = None

#Output functions
def getOutputs():
    ftxt = open(outputFile, "r+")
    bmsg = ftxt.read()
    ftxt.close()
    outmsg.configure(text=bmsg)
    afterid1 = bkui.after(1000, getOutputs)
    #print(afterid1)

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
    #file.write("%s %s %s" % (mTime, mTemp1, mTemp2))
    file.close()

#Boil Kettle Menu Functions
def getBoilTimes():
    global bTime1
    global bTime2
    global bTime3
    global bTotalTime
    bTime1 = bkTime1Entry.get()
    bTime2 = bkTime2Entry.get()
    bTime3 = bkTime3Entry.get()
    #print(bTime1)
    #print(bTime2)
    #print(bTime3)
    
    bTotalTime = int(bTime1) + int(bTime2) + int(bTime3)

    bTime1String.set(bTime1)
    bTime2String.set(bTime2)
    bTime3String.set(bTime3)
    bTotalTimeString.set(bTotalTime)

def startBoil():
    #TODO: call C program with boil time as inputs
    #proc = os.system("sudo ./BoilKettlePi " + str(bTotalTime) + ' &')
    global proc
    proc = subprocess.Popen(['sudo', './BoilKettlePi', str(bTotalTime)])
    pid = proc.pid
    return

#Page navigation helper functions
def goToMenuPage():
    menu_page.tkraise()

def goToBkPage():
    bk_page.tkraise()

def goToBkConfPage():
    getBoilTimes()
    bkConf_page.tkraise()

def goToOutPage():
    startBoil()
    getOutputs()
    out_page.tkraise()

def goToMtPage():
    mt_page.tkraise()

def goToMtSentPage():
    getMashData()
    mtSent_page.tkraise()

def exitbk():
    proc.terminate()
    exit(0)


bkui = Tk()
bkui.title("BoilKettlePi")
#init bkui config to account for resizing
bkui.columnconfigure(0, weight=1)
bkui.columnconfigure(1, weight=1)
bkui.columnconfigure(2, weight=1) 
bkui.columnconfigure(3, weight=1)
bkui.columnconfigure(4, weight=1)
bkui.columnconfigure(5, weight=1)
bkui.rowconfigure(0, weight=1)
bkui.rowconfigure(1, weight=1)
bkui.rowconfigure(2, weight=1)
bkui.rowconfigure(3, weight=1)
bkui.rowconfigure(4, weight=1)
bkui.rowconfigure(5, weight=1)

#declare pages
menu_page = Frame(bkui)
bk_page = Frame(bkui) 
bkConf_page = Frame(bkui)
mt_page = Frame(bkui)
out_page = Frame(bkui)
mtSent_page = Frame(bkui)

#init config for all pages
for frame in (menu_page, bk_page, bkConf_page, out_page, mt_page, mtSent_page):
    frame.grid(row=0, column=0, sticky=(N, S, E, W))
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1) 
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=1)
    frame.columnconfigure(5, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)
    frame.rowconfigure(5, weight=1)

#MENU PAGE - (menu_page)
mtConfig = Button(menu_page, text="MashTun Settings", command=goToMtPage)
btConfig = Button(menu_page, text="BoilKettle Settings", command=goToBkPage)
exitMenu = Button(menu_page, text='Exit', command=exitbk)
menuMsg = Message(menu_page, text="Welcome to BoilKettlePi", width=10000)

mtConfig.grid(row=5, column=0)
btConfig.grid(row=5, column=1)
exitMenu.grid(row=5, column=2)
menuMsg.grid(row=0, column=1)

#BOIL KETTLE PAGE - (bk_page)
#prompts and entries
bkSettings = Message(bk_page, text="BoilKettle Settings", width = 10000)
bkTime1 = Label(bk_page, text="Initial Boil:")
bkTime1Entry = Entry(bk_page)
bkTime1Units = Label(bk_page, text="minutes")
bkTime2 = Label(bk_page, text="1st reminder:")
bkTime2Entry = Entry(bk_page)
bkTime2Units = Label(bk_page, text="minutes")
bkTime3 = Label(bk_page, text="2nd reminder:")
bkTime3Entry = Entry(bk_page)
bkTime3Units = Label(bk_page, text="minutes")
#navigation buttons
confirmBK = Button(bk_page, text="Confirm", command=goToBkConfPage)
btsBK = Button(bk_page, text='Menu', command=goToMenuPage)
exitBK = Button(bk_page, text='Exit', command=exitbk)

bkSettings.grid(row=0, column=1)
bkTime1.grid(row=1, column=0)
bkTime1Entry.grid(row=1, column=1)
bkTime1Units.grid(row=1, column=2)
bkTime2.grid(row=2, column=0)
bkTime2Entry.grid(row=2, column=1)
bkTime2Units.grid(row=2, column=2)
bkTime3.grid(row=3, column=0)
bkTime3Entry.grid(row=3, column=1)
bkTime3Units.grid(row=3, column=2)
btsBK.grid(row=5, column=0)
confirmBK.grid(row=5, column=1)
exitBK.grid(row=5, column=2)

#BOIL KETTLE CONFIRMATION PAGE
bTime1String = StringVar()
bTime2String = StringVar()
bTime3String = StringVar()
bTotalTimeString = StringVar()
bkConfSettings = Message(bkConf_page, text="Confirm BoilKettle Settings", width = 10000)
bkConfTime1 = Label(bkConf_page, text="Initial Boil:")
bkConfTime1Entry = Label(bkConf_page, textvariable=bTime1String)
bkConfTime1Units = Label(bkConf_page, text="minutes")
bkConfTime2 = Label(bkConf_page, text="1st reminder:")
bkConfTime2Entry = Label(bkConf_page, textvariable=bTime2String)
bkConfTime2Units = Label(bkConf_page, text="minutes")
bkConfTime3 = Label(bkConf_page, text="2nd reminder:")
bkConfTime3Entry = Label(bkConf_page, textvariable=bTime3String)
bkConfTime3Units = Label(bkConf_page, text="minutes")
bkConfTotalTime = Label(bkConf_page, text="Total Boil Time:")
bkConfTotalTimeEntry = Label(bkConf_page, textvariable=bTotalTimeString)
bkConfTotalTimeUnits = Label(bkConf_page, text="minutes") 
#navigation buttons
menuBKConf = Button(bkConf_page, text="Back", command=goToBkPage)
startBKConf = Button(bkConf_page, text="Start Boil", command=goToOutPage)
exitBKConf = Button(bkConf_page, text='Exit', command=exitbk)

bkConfSettings.grid(row=0, column=1)
bkConfTime1.grid(row=1, column=0)
bkConfTime1Entry.grid(row=1, column=1)
bkConfTime1Units.grid(row=1, column=2)
bkConfTime2.grid(row=2, column=0)
bkConfTime2Entry.grid(row=2, column=1)
bkConfTime2Units.grid(row=2, column=2)
bkConfTime3.grid(row=3, column=0)
bkConfTime3Entry.grid(row=3, column=1)
bkConfTime3Units.grid(row=3, column=2)
bkConfTotalTime.grid(row=4, column=0)
bkConfTotalTimeEntry.grid(row=4, column=1)
bkConfTotalTimeUnits.grid(row=4, column=2)
menuBKConf.grid(row=5, column=0)
startBKConf.grid(row=5, column=1)
exitBKConf.grid(row=5, column=2)

#output page - (out_page)
exitOut = Button(out_page, text='Exit', command=exitbk)
outmsg = Message(out_page, text=bmsg, width=10000)

outmsg.grid(row=2, column=1)
exitOut.grid(row=5, column=2)

#MT PAGE - (mt_page)
#prompts and entries
mtSettings = Label(mt_page, text="Mash Tun Settings:")
mashTime = Label(mt_page, text="Mash Time:")
mashTimeEntry = Entry(mt_page)
mashTimeUnits = Label(mt_page, text="minutes")
mashTemp1 = Label(mt_page, text="Mash Temperature:")
mashTemp1Entry = Entry(mt_page)
mashTemp1Units = Label(mt_page, text="\xb0F")
mashTemp2 = Label(mt_page, text="Mash Temperature:")
mashTemp2Entry = Entry(mt_page)
mashTemp2Units = Label(mt_page, text="\xb0F")
#navigation buttons
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
btsMT.grid(row=5, column=0)
sendMTData.grid(row=5, column=1)
exitMT.grid(row=5, column=2)

#MT SENT PAGE - (mtSent_page)
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
btsMTSent.grid(row=5, column=1)


menu_page.tkraise()
bkui.mainloop()
