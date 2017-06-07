import time
import serial
import os
import subprocess
from tkinter import *

outputFile = "output.txt"
mashFile = "mashtun.txt"
bmsg = "Waiting for BK"
os.system('export WIRINGPI_GPIOMEM=1')

#find and remove existing output.txt
if (os.path.exists(outputFile)):
	os.remove(outputFile)

#mash communication variables
mashIP = "192.168.1.236"
mashPort = "8080"

global ser
ser = None
#keg communication variables
ttyName = '/dev/ttyACM0'
ttyAvailable = 0 #flag for ser
#determins if ardino keg is connected
if os.path.exists(ttyName):
	ttyAvailable = 1
	ser = serial.Serial('/dev/ttyACM0', 9600)
else:
	ttyAvailable = 0
#set up only if tty is available

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
global procflag
procflag = 0

#Output functions
def getOutputs():
    ftxt = open(outputFile, "r+")
    bmsg = ftxt.read()
    ftxt.close()
    outmsg.configure(text=bmsg)
    afterid1 = bkui.after(1000, getOutputs)
    #print(afterid1)

def disableFirstReminder():
		firstReminderMsg.config(state=DISABLED)

def enableFirstReminder():
		firstReminderMsg.config(state=ACTIVE)
		bkui.after(60000, disableFirstReminder)

def disableSecondReminder():
		secondReminderMsg.config(state=DISABLED)

def enableSecondReminder():
		secondReminderMsg.config(state=ACTIVE)
		bkui.after(60000, disableSecondReminder);

#Mash Tun Menu Functions 
def getMashData():
		#get inputs
    global mTime
    global mTemp1
    global mTemp2
    mTime = mashTimeEntry.get()
    mTemp1 = mashTemp1Entry.get()
    mTemp2 = mashTemp2Entry.get()
		#set stringvar for gui display
    mTimeString.set(mTime)
    mTemp1String.set(mTemp1)
    mTemp2String.set(mTemp2)
		#write outputs to file
    if mTime and mTemp1 and mTemp2:
    	file = open(mashFile, 'w+')
    	file.write("%s %s %s" % (mTemp1, mTemp2, mTime))
    	file.close()
    	#send data to mash using netcat
    	commandString = "cat mashtun.txt | nc -w 3 " + mashIP + " " + mashPort 
    	#print(commandString)
    	os.system(commandString)

#Boil Kettle Menu Functions
def getBoilTimes():
		#get boil times
    global bTime1
    global bTime2
    global bTime3
    global bTotalTime
    bTime1 = bkTime1Entry.get()
    bTime2 = bkTime2Entry.get()
    bTime3 = bkTime3Entry.get()
    if not bTime3:
   		if bTime2:
   			bTotalTime = int(bTime1) + int(bTime2)
   			bkui.after( (bTime2*60000), enableFirstReminder)
   		elif not bTime2:
   			bTotalTime = int(bTime1)
    else:
   		bTotalTime = int(bTime1) + int(bTime2) + int(bTime3)
   		bkui.after(int(int(bTime2)*60000), enableFirstReminder)
   		bkui.after(int((int(bTime2) + int(bTime3))*60000), enableSecondReminder)
    #bTotalTime = int(bTime1) + int(bTime2) + int(bTime3)
		#set stringvars for gui display
    bTime1String.set(bTime1)
    bTime2String.set(bTime2)
    bTime3String.set(bTime3)
    bTotalTimeString.set(bTotalTime)

def startBoil():
    #TODO: call C program with boil time as inputs
    file = open(outputFile, 'w+')
    file.close()
    os.system('export WIRINGPI_GPIOMEM=1')
    global proc
    proc = subprocess.Popen(['./BoilKettlePi', str(bTotalTime)])
    pid = proc.pid
    global procflag
    procflag = 1
    return
    
#Keg menu functions
def sendDrinkName():
	#TODO: serial name transfer to smart keg
	drinkNameString = kegDrinkEntry.get()
	drinkName.set(drinkNameString)
	if not ser.isOpen():
		ser.open()
	ser.flushInput()
	ser.flushOutput()
	drinkNameString = drinkNameString + "!"
	time.sleep(4)
	ser.write(drinkNameString.encode())
	print("sending: " + str(drinkNameString.encode()))
	time.sleep(2)
	#test arduino code
	#drinkNameReceive = ser.readline()
	#ser.write(drinkNameString.encode())
	#ser.write(drinkNameString.encode())
	##print("received " + drinkNameReceive.decode())

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

def goToKegPage():
		keg_page.tkraise()

def goToKegSentPage():
		sendDrinkName()
		kegSent_page.tkraise()

def exitbk():
    if (procflag == 1):
    	proc.terminate()
    	os.remove(outputFile)
    exit(0)


bkui = Tk()
bkui.attributes("-fullscreen",True)
bkui.title("BoilKettlePi")
#init bkui config to account for resizing
bkui.grid_columnconfigure(0, weight=1)
bkui.grid_rowconfigure(0, weight=1)

#declare pages
menu_page = Frame(bkui)
bk_page = Frame(bkui) 
bkConf_page = Frame(bkui)
out_page = Frame(bkui)
mt_page = Frame(bkui)
mtSent_page = Frame(bkui)
keg_page = Frame(bkui)
kegSent_page = Frame(bkui)

#init config for all pages
for frame in (menu_page, bk_page, bkConf_page, out_page, mt_page, mtSent_page, 
	keg_page, kegSent_page):
    frame.grid(row=0, column=0, sticky=N+S+E+W)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

#MENU PAGE - (menu_page)
#PAGE CONFIG
colwidth = int(bkui.winfo_screenwidth()/6)
menu_page.grid_columnconfigure(0, weight=1)
menu_page.grid_columnconfigure(1, weight=1)
menu_page.grid_columnconfigure(2, weight=1) 
menu_page.grid_columnconfigure(3, weight=1)
menu_page.grid_columnconfigure(4, weight=1)
menu_page.grid_rowconfigure(0, weight=1)
menu_page.grid_rowconfigure(1, weight=1)
menu_page.grid_rowconfigure(2, weight=1)
menu_page.grid_rowconfigure(3, weight=1)
menu_page.grid_rowconfigure(4, weight=1)
#BUTTONS AND PROMPTS
mtConfig = Button(menu_page, text="MashTun Settings", width=colwidth,
	command=goToMtPage)
btConfig = Button(menu_page, text="BoilKettle Settings", width=colwidth, 
	command=goToBkPage)
kegConfig = Button(menu_page, text="Keg Settings", width=colwidth, 
	command=goToKegPage)
exitMenu = Button(menu_page, text='Exit', width=colwidth, command=exitbk)
emptyLabel = Label(menu_page, text=' ', width=colwidth)
menuMsg = Label(menu_page, text="ome to BoilKe", 
	font=("TkDefaultFont", 18))
menuMsg1 = Label(menu_page, text = "Welc", font=("TkDefaultFont",18))
menuMsg2 = Label(menu_page, text = "ttlePi", font=("TkDefaultFont", 18))

mtConfig.grid(row=4, column=0, sticky=N+S+E+W)
btConfig.grid(row=4, column=1, sticky=N+S+E+W)
kegConfig.grid(row=4, column=2, sticky=N+S+E+W)
emptyLabel.grid(row=4, column=3, sticky=N+S+E+W)
exitMenu.grid(row=4, column=4, sticky=N+S+E+W)
menuMsg.grid(row=2, column=2, sticky=N+S+E+W)
menuMsg1.grid(row=2, column=1, sticky=N+S+E)
menuMsg2.grid(row=2, column=3, sticky=N+S+W)

if ttyAvailable == 0:
	kegConfig.config(state=DISABLED)
elif ttyAvailable == 1:
	kegConfig.config(state=ACTIVE)

#BOIL KETTLE PAGE - (bk_page)
#PAGE CONFIG
bk_page.grid_columnconfigure(0, weight=1)
bk_page.grid_columnconfigure(1, weight=1)
bk_page.grid_columnconfigure(2, weight=1) 
bk_page.grid_rowconfigure(0, weight=1)
bk_page.grid_rowconfigure(1, weight=1)
bk_page.grid_rowconfigure(2, weight=1)
bk_page.grid_rowconfigure(3, weight=1)
bk_page.grid_rowconfigure(4, weight=1)
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

bkSettings.grid(row=0, column=1, sticky=N+S+E+W)
bkTime1.grid(row=1, column=0, sticky=N+S+E+W)
bkTime1Entry.grid(row=1, column=1, sticky=N+S+E+W)
bkTime1Units.grid(row=1, column=2, sticky=N+S+E+W)
bkTime2.grid(row=2, column=0, sticky=N+S+E+W)
bkTime2Entry.grid(row=2, column=1, sticky=N+S+E+W)
bkTime2Units.grid(row=2, column=2, sticky=N+S+E+W)
bkTime3.grid(row=3, column=0, sticky=N+S+E+W)
bkTime3Entry.grid(row=3, column=1, sticky=N+S+E+W)
bkTime3Units.grid(row=3, column=2, sticky=N+S+E+W)
btsBK.grid(row=4, column=0, sticky=N+S+E+W)
confirmBK.grid(row=4, column=1, sticky=N+S+E+W)
exitBK.grid(row=4, column=2, sticky=N+S+E+W)

#BOIL KETTLE CONFIRMATION PAGE (bkConf_page
#PAGE CONFIG
bkConf_page.grid_columnconfigure(0, weight=1)
bkConf_page.grid_columnconfigure(1, weight=1)
bkConf_page.grid_columnconfigure(2, weight=1) 
bkConf_page.grid_rowconfigure(0, weight=1)
bkConf_page.grid_rowconfigure(1, weight=1)
bkConf_page.grid_rowconfigure(2, weight=1)
bkConf_page.grid_rowconfigure(3, weight=1)
bkConf_page.grid_rowconfigure(4, weight=1)
bkConf_page.grid_rowconfigure(5, weight=1)
#BUTTONS AND PROMPTS
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

bkConfSettings.grid(row=0, column=1, sticky=N+S+E+W)
bkConfTime1.grid(row=1, column=0, sticky=N+S+E+W)
bkConfTime1Entry.grid(row=1, column=1, sticky=N+S+E+W)
bkConfTime1Units.grid(row=1, column=2, sticky=N+S+E+W)
bkConfTime2.grid(row=2, column=0, sticky=N+S+E+W)
bkConfTime2Entry.grid(row=2, column=1, sticky=N+S+E+W)
bkConfTime2Units.grid(row=2, column=2, sticky=N+S+E+W)
bkConfTime3.grid(row=3, column=0, sticky=N+S+E+W)
bkConfTime3Entry.grid(row=3, column=1, sticky=N+S+E+W)
bkConfTime3Units.grid(row=3, column=2, sticky=N+S+E+W)
bkConfTotalTime.grid(row=4, column=0, sticky=N+S+E+W)
bkConfTotalTimeEntry.grid(row=4, column=1, sticky=N+S+E+W)
bkConfTotalTimeUnits.grid(row=4, column=2, sticky=N+S+E+W)
menuBKConf.grid(row=5, column=0, sticky=N+S+E+W)
startBKConf.grid(row=5, column=1, sticky=N+S+E+W)
exitBKConf.grid(row=5, column=2, sticky=N+S+E+W)

#output page - (out_page)
#PAGE CONFIG
out_page.grid_columnconfigure(0, weight=1)
out_page.grid_columnconfigure(1, weight=2)
out_page.grid_columnconfigure(2, weight=1) 
out_page.grid_rowconfigure(0, weight=1)
out_page.grid_rowconfigure(1, weight=1)
out_page.grid_rowconfigure(2, weight=1)
out_page.grid_rowconfigure(3, weight=1)
out_page.grid_rowconfigure(4, weight=1)

exitOut = Button(out_page, text='Exit', command=exitbk)
outmsg = Message(out_page, text=bmsg, font=("TkDefaultFont", 16), width=10000)
firstReminderMsg = Label(out_page, text="ADD FIRST INGREDIENT", state=DISABLED)
secondReminderMsg = Label(out_page, text="ADD SECOND INGREDIENT", state=DISABLED)

outmsg.grid(row=1, column=1, sticky=N+S+E+W)
firstReminderMsg.grid(row=2, column=1)
secondReminderMsg.grid(row=3, column=1)
exitOut.grid(row=4, column=2, sticky=N+S+E+W)

#MT PAGE - (mt_page)
#PAGE CONFIG
mt_page.grid_columnconfigure(0, weight=1)
mt_page.grid_columnconfigure(1, weight=1)
mt_page.grid_columnconfigure(2, weight=1) 
mt_page.grid_rowconfigure(0, weight=1)
mt_page.grid_rowconfigure(1, weight=1)
mt_page.grid_rowconfigure(2, weight=1)
mt_page.grid_rowconfigure(3, weight=1)
mt_page.grid_rowconfigure(4, weight=1)
mt_page.grid_rowconfigure(5, weight=1)
#prompts and entries
mtSettings = Label(mt_page, text="Mash Tun Settings:")
mashTime = Label(mt_page, text="Mash Time:")
mashTimeEntry = Entry(mt_page)
mashTimeUnits = Label(mt_page, text="minutes")
mashTemp1 = Label(mt_page, text="Mash Temperature:")
mashTemp1Entry = Entry(mt_page)
mashTemp1Units = Label(mt_page, text="\xb0F")
mashTemp2 = Label(mt_page, text="Sparge Temperature:")
mashTemp2Entry = Entry(mt_page)
mashTemp2Units = Label(mt_page, text="\xb0F")
#navigation buttons
btsMT = Button(mt_page, text='Menu', command=goToMenuPage)
sendMTData = Button(mt_page, text="Send to Mash Tun", command=goToMtSentPage)
exitMT = Button(mt_page, text='Exit', command=exitbk)

mtSettings.grid(row=0, column=1, sticky=N+S+E+W)
mashTime.grid(row=1, column=0, sticky=N+S+E+W)
mashTimeEntry.grid(row=1, column=1, sticky=N+S+E+W) 
mashTimeUnits.grid(row=1, column=2, sticky=N+S+E+W)
mashTemp1.grid(row=2, column=0, sticky=N+S+E+W)
mashTemp1Entry.grid(row=2, column=1, sticky=N+S+E+W)
mashTemp1Units.grid(row=2, column=2, sticky=N+S+E+W)
mashTemp2.grid(row=3, column=0, sticky=N+S+E+W)
mashTemp2Entry.grid(row=3, column=1, sticky=N+S+E+W)
mashTemp2Units.grid(row=3, column=2, sticky=N+S+E+W)
btsMT.grid(row=5, column=0, sticky=N+S+E+W)
sendMTData.grid(row=5, column=1, sticky=N+S+E+W)
exitMT.grid(row=5, column=2, sticky=N+S+E+W)

#MT SENT PAGE - (mtSent_page)
#PAGE CONFIG
mtSent_page.grid_columnconfigure(0, weight=1)
mtSent_page.grid_columnconfigure(1, weight=1)
mtSent_page.grid_columnconfigure(2, weight=1) 
mtSent_page.grid_rowconfigure(0, weight=1)
mtSent_page.grid_rowconfigure(1, weight=1)
mtSent_page.grid_rowconfigure(2, weight=1)
mtSent_page.grid_rowconfigure(3, weight=1)
mtSent_page.grid_rowconfigure(4, weight=1)
mtSent_page.grid_rowconfigure(5, weight=1)
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

mtSentMsg.grid(row=0, column=1, sticky=N+S+E+W)
mtSentTime.grid(row=1, column=0, sticky=N+S+E+W)
mtSentTimeEntry.grid(row=1, column=1, sticky=N+S+E+W)
mtSentTimeUnits.grid(row=1, column=2, sticky=N+S+E+W)
mtSentTemp1.grid(row=2, column=0, sticky=N+S+E+W)
mtSentTemp1Entry.grid(row=2, column=1, sticky=N+S+E+W)
mtSentTemp1Units.grid(row=2, column=2, sticky=N+S+E+W)
mtSentTemp2.grid(row=3, column=0, sticky=N+S+E+W)
mtSentTemp2Entry.grid(row=3, column=1, sticky=N+S+E+W)
mtSentTemp2Units.grid(row=3, column=2, sticky=N+S+E+W)
btsMTSent.grid(row=5, column=1, sticky=N+S+E+W)

#KEG PAGE - keg_page
#PAGE CONFIG
keg_page.grid_columnconfigure(0, weight=1)
keg_page.grid_columnconfigure(1, weight=1)
keg_page.grid_columnconfigure(2, weight=1) 
keg_page.grid_rowconfigure(0, weight=1)
keg_page.grid_rowconfigure(1, weight=1)
keg_page.grid_rowconfigure(2, weight=1)
keg_page.grid_rowconfigure(3, weight=1)
keg_page.grid_rowconfigure(4, weight=1)
keg_page.grid_rowconfigure(5, weight=1)
#BUTTONS AND PROMPTS
drinkName = StringVar()
menuKeg = Button(keg_page, text="Menu", command=goToMenuPage) 
kegSettingsPrompt = Label(keg_page, text="Keg Settings") 
kegDrinkPrompt = Label(keg_page, text="Drink Name:")
kegDrinkEntry = Entry(keg_page)
kegSendDrinkName = Button(keg_page, text="Send Keg Name", 
	command=goToKegSentPage)

kegSettingsPrompt.grid(row=0, column=1, sticky=N+S+E+W)
menuKeg.grid(row=5, column=0, sticky=N+S+E+W)
kegDrinkPrompt.grid(row=2, column=0, sticky=N+S+E+W)
kegDrinkEntry.grid(row=2, column=1, sticky=N+S+E+W)
kegSendDrinkName.grid(row=2, column=2, sticky=N+S+E+W)

#KEG SENT PAGE - kegSent_page
#PAGE CONFIG
kegSent_page.grid_columnconfigure(0, weight=1)
kegSent_page.grid_columnconfigure(1, weight=1)
kegSent_page.grid_columnconfigure(2, weight=1) 
kegSent_page.grid_rowconfigure(0, weight=1)
kegSent_page.grid_rowconfigure(1, weight=1)
kegSent_page.grid_rowconfigure(2, weight=1)
kegSent_page.grid_rowconfigure(3, weight=1)
kegSent_page.grid_rowconfigure(4, weight=1)
menuKegSent = Button(kegSent_page, text="Menu", command=goToMenuPage)
kegSentMsg = Label(kegSent_page, text="Drink Name Sent:")
kegSentDrink = Label(kegSent_page, textvariable=drinkName)

menuKegSent.grid(row=4, column=1, sticky=N+S+E+W)
kegSentMsg.grid(row=1, column=1, sticky=N+S+E+W)
kegSentDrink.grid(row=2, column=1, sticky=N+S+E+W)

menu_page.tkraise()
bkui.mainloop()
