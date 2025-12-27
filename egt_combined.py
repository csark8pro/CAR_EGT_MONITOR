import os
import subprocess
import tkinter
import serial
from serial.serialutil import Timeout
import serial.tools.list_ports_windows
import threading
import time
import winsound
from tkinter import ttk
from tkinter import *
import pdb

timetodie = False

#add function for offset temps
def add_temp_offset(temps):
    correction = [cyl1_offset_selection.current(),cyl2_offset_selection.current(),cyl3_offset_selection.current(),
                cyl4_offset_selection.current(),cyl5_offset_selection.current(),cyl6_offset_selection.current()]
    corrected = temps
    #pdb.set_trace()
    for i in range(6):
        corrected[i] = str(int(temps[i]) + correction[i])
    return corrected
    
def cleanupandclose():
    #add some cleanup logik here
    exit()

def change_average_temp(temps):
    average = 0
    for i in temps:
        if i.isdecimal():
            average += int(i)
            print('[DEBUG] average_inloop '+str(average))
        else:
            pass
    average /= 6
    average = round(average,2)
    print('[Debug] average ='+str(average))
    cylinderavertemp.configure(text=str(average))
    canvas.coords(cyl_aver,20, 400, average+25, 440)

def write_to_logfile(temps,fileid):
    datafailure = False
    #pdb.set_trace()
    if len(temps) != 6:
        datafailure = True
    logstring = time.asctime()
    if datafailure:
        pass
        error_function('write to logfile','maybe message length off')
    else:
        cylinder = 1
        for i in temps:
            logstring += ','
            if i.isdecimal():
                logstring += 'Cylinder'+str(cylinder)
                logstring += ','
                logstring += str(i)
            else:
                pass
            cylinder += 1
        logstring += '\n'
        fileid.write(logstring)
    #pdb.set_trace()

def refresh_portlist():
    portlist = serial.tools.list_ports_windows.comports()
    if portlist:
        comport.configure(values=portlist)
        comport.current(0)
    else:
        comport.configure(values=['NoDev'])
        print('[DEBUG] No COM Device listed.')
    #pdb.set_trace()

def error_function(area,message):
    print('[ERROR in] '+area)
    print('[Developer Hint] '+message)
    #exit()

def start_log():
    #add open logfile
    if log_thread.is_alive():
        button_start_log.configure(text="Stop Log", command=stop_log)
        change_recordlight_color()
    else:
        button_start_log.configure(text="Stop Log", command=stop_log)
        change_recordlight_color()
        log_thread.start()

def stop_log():
    #add close open file
    button_start_log.configure(text="Start Log", command=start_log)
    change_recordlight_color()

#modification plan -> keep the thread alive! done
def log():
    #add check if mainthread is alive, else die
    prepstatus = False
    while True:
        logstatus = get_logstatus()
        #pdb.set_trace()
        if logstatus:
            if prepstatus == FALSE:
                try:
                    serialports = serial.tools.list_ports_windows.comports()
                except:
                    error_function('serial.tools.list_ports','serial.tools.list_ports_windows.comports()')
                if serialports == []:
                    print("No Ports available, check your Hardware and Driver configuration!")
                    #exit()
                else:
                    print("Available Ports:")
                    for port in serialports:
                        print(port)
                try:
                    #serialconnection = serial.Serial("COM4",9600)
                    #add selected com port here
                    print('[DEBUG] connecting with port '+str(serialports[comport.current()])[0:4])
                    serialconnection = serial.Serial(str(serialports[comport.current()])[0:4],9600,timeout=10)
                    #pdb.set_trace()
                except:
                    error_function('Creating serial Connection','maybe wrong port ? ')
                try:
                    logfile = open("EGT_Logfile_"+time.asctime().replace(" ","_")[0:10]+".csv","a")
                except:
                    error_function('open(logfile)','hm thats weird.')
                prepstatus = True
            else:
                #get serial data
                try:
                    time.sleep(0.2)
                    rawdata = serialconnection.readline()
                    #pdb.set_trace()
                except:
                    error_function('get data from serial device','check the serial connection,usb...')
                    
                if len(rawdata) < 18:
                    #pdb.set_trace()
                    print('[Debug] rawdata size wrong')
                else:
                    data = rawdata.decode()
                    #sort serial data out
                    temps = data.replace('\n','').split('\t')
                    print('[Debug temps]')
                    print(temps)
                    #modify + offset temps here
                    #temps_plus_offset = function_to_add_offset_temp(temps)
                    #pdb.set_trace()
                    temps = add_temp_offset(temps)

                    alerttemp = alerttemp_selection.current()
                    #pdb.set_trace()
                    cylinder = 0
                    for c in temps:
                        
                        if c.isdecimal():
                            if int(c) >= alerttemp:
                                winsound.Beep(4000,80)
                            change_cylindertemp(cylinder,int(c))
                        else:
                            pass
                        cylinder += 1
                    change_average_temp(temps)
                    write_to_logfile(temps,logfile)
        else:
            #important to save cpu and energy !
            #fullspeed thread without job is dangerous!
            #check every 2 sec, condition else it would check millions of times in a sec !!! 
            #think lowlevel ! jle -> jle ...
            try:
                logfile.close()
                serialconnection.close()
            except:
                error_function('logfile.close(),serialconnection.close','idk')
            prepstatus = False
            time.sleep(2)
            #!!!!!!!!!!!!

def get_logstatus():
    if canvas.itemcget(recordlight, 'fill') == 'green2':
        return True
    else:
        return False
        
def change_recordlight_color():
    if canvas.itemcget(recordlight, 'fill') == 'red':
        canvas.itemconfigure(recordlight, fill = 'green2')
    else:
        canvas.itemconfigure(recordlight, fill = 'red')
        
def openlogfilelocation():
    subprocess.run(os.path.join(os.getenv('WINDIR'), 'explorer.exe .'))

def change_cylindertemp(cyl,temp):
    #change temp on cyl1 testing
    if cyl == 0:
        canvas.coords(cyl_1_id,20, 100, temp+25, 140)
        cylindertemp1.configure(text=str(temp))
    if cyl == 1:
        canvas.coords(cyl_2_id,20, 150, temp+25, 190)
        cylindertemp2.configure(text=str(temp))
    if cyl == 2:
        canvas.coords(cyl_3_id,20, 200, temp+25, 240)
        cylindertemp3.configure(text=str(temp))
    if cyl == 3:
        canvas.coords(cyl_4_id,20, 250, temp+25, 290)
        cylindertemp4.configure(text=str(temp))
    if cyl == 4:
        canvas.coords(cyl_5_id,20, 300, temp+25, 340)
        cylindertemp5.configure(text=str(temp))
    if cyl == 5:
        canvas.coords(cyl_6_id,20, 350, temp+25, 390)
        cylindertemp6.configure(text=str(temp))

def eventhandler(event):
    #print(event)
    toggle_fullscreen()
    
def toggle_nightmode():
        if canvas['bg'] == 'black':
            canvas.configure(bg='white')
            button_nightmode.configure(text="Nightmode(Black)")
        else:
            canvas.configure(bg='black')
            button_nightmode.configure(text="Daymode(white)")

def toggle_fullscreen():
    if tkFenster.attributes('-fullscreen') == True:
        tkFenster.attributes('-fullscreen', False)
        #change Button to 'Fullscreen' 
        button_fullscreen.configure(text= "Fullscreen")
    else:
        tkFenster.attributes('-fullscreen', True)
        #change Button to 'Windowed'
        button_fullscreen.configure(text= "Windowed")
#Fenster Fullscreen windowed
pad = -5
tkFenster = Tk()
tkFenster.title('EGT-Logger')
tkFenster.geometry("{0}x{1}+0+0".format(
            tkFenster.winfo_screenwidth()-pad, tkFenster.winfo_screenheight()-pad))
tkFenster.bind('<Escape>', eventhandler)
#Zeichnung
canvas = Canvas(master=tkFenster, bg='white')
canvas.place(x=-5,y=-5,width=1600,height=1400)
#actual temperatur realtime
cyl_1_id = canvas.create_rectangle(20, 100, 25, 140,fill='red')
cyl_2_id = canvas.create_rectangle(20, 150, 25, 190,fill='red')
cyl_3_id = canvas.create_rectangle(20, 200, 25, 240,fill='red')
cyl_4_id = canvas.create_rectangle(20, 250, 25, 290,fill='red')
cyl_5_id = canvas.create_rectangle(20, 300, 25, 340,fill='red')
cyl_6_id = canvas.create_rectangle(20, 350, 25, 390,fill='red')
#average temp
cyl_aver = canvas.create_rectangle(20, 400, 25, 440,fill='orange')
#cylinderlabel
cylindername1 = Label(master=tkFenster,text='Cylinder 1')
cylindername1.place(x=20,y=105,width=80,height=20)
cylindername1 = Label(master=tkFenster,text='Cylinder 2')
cylindername1.place(x=20,y=155,width=80,height=20)
cylindername1 = Label(master=tkFenster,text='Cylinder 3')
cylindername1.place(x=20,y=205,width=80,height=20)
cylindername1 = Label(master=tkFenster,text='Cylinder 4')
cylindername1.place(x=20,y=255,width=80,height=20)
cylindername1 = Label(master=tkFenster,text='Cylinder 5')
cylindername1.place(x=20,y=305,width=80,height=20)
cylindername1 = Label(master=tkFenster,text='Cylinder 6')
cylindername1.place(x=20,y=355,width=80,height=20)
#averagelabel
cyl_avername = Label(master=tkFenster,text='Average')
cyl_avername.place(x=20,y=405,width=80,height=20)
#cylindertemps
cylindertemp1 = Label(master=tkFenster,text='-')
cylindertemp1.place(x=1150,y=105,width=80,height=20)
cylindertemp2 = Label(master=tkFenster,text='-')
cylindertemp2.place(x=1150,y=155,width=80,height=20)
cylindertemp3 = Label(master=tkFenster,text='-')
cylindertemp3.place(x=1150,y=205,width=80,height=20)
cylindertemp4 = Label(master=tkFenster,text='-')
cylindertemp4.place(x=1150,y=255,width=80,height=20)
cylindertemp5 = Label(master=tkFenster,text='-')
cylindertemp5.place(x=1150,y=305,width=80,height=20)
cylindertemp6 = Label(master=tkFenster,text='-')
cylindertemp6.place(x=1150,y=355,width=80,height=20)
#averagecylindertemp
cylinderavertemp = Label(master=tkFenster,text='-')
cylinderavertemp.place(x=1150,y=405,width=80,height=20)
#combobox for com port selection
comport = ttk.Combobox(master=tkFenster)
comport.place(x=390,y=20,width=260,height=20)
#Alert Temperatur
alerttemp_label = ttk.Label(master=tkFenster,text='Alerttemp')
alerttemp_label.place(x=660,y=20,width=80,height=20)
#combobox selection
alerttemp_selection = ttk.Combobox(master=tkFenster,values=list(range(0,1200)))
alerttemp_selection.place(x=750,y=20,width=50,height=20)
alerttemp_selection.current(449)

#Cylinder Temp Offset(reading correction)
Cylinder_temp_offset_label = ttk.Label(master=tkFenster,text='Offsets')
Cylinder_temp_offset_label.place(x=1250,y=50,width=50,height=20)

#Cylinder Temp Offset combobox cyl1
cyl1_offset_selection = ttk.Combobox(master=tkFenster,values=list(range(0,50)))
cyl1_offset_selection.place(x=1250,y=105,width=50,height=20)
cyl1_offset_selection.current(0)

#Cylinder Temp Offset combobox cyl2
cyl2_offset_selection = ttk.Combobox(master=tkFenster,values=list(range(0,50)))
cyl2_offset_selection.place(x=1250,y=155,width=50,height=20)
cyl2_offset_selection.current(0)

#Cylinder Temp Offset combobox cyl3
cyl3_offset_selection = ttk.Combobox(master=tkFenster,values=list(range(0,50)))
cyl3_offset_selection.place(x=1250,y=205,width=50,height=20)
cyl3_offset_selection.current(0)

#Cylinder Temp Offset combobox cyl4
cyl4_offset_selection = ttk.Combobox(master=tkFenster,values=list(range(0,50)))
cyl4_offset_selection.place(x=1250,y=255,width=50,height=20)
cyl4_offset_selection.current(0)

#Cylinder Temp Offset combobox cyl5
cyl5_offset_selection = ttk.Combobox(master=tkFenster,values=list(range(0,50)))
cyl5_offset_selection.place(x=1250,y=305,width=50,height=20)
cyl5_offset_selection.current(0)

#Cylinder Temp Offset combobox cyl6
cyl6_offset_selection = ttk.Combobox(master=tkFenster,values=list(range(0,50)))
cyl6_offset_selection.place(x=1250,y=355,width=50,height=20)
cyl6_offset_selection.current(0)

#refresh portlist button
button_refresh_portlist = Button(master=tkFenster, text='Refresh COM ports', command=refresh_portlist)
button_refresh_portlist.place(x=220,y=20,width=160,height=20)
#create new thread and run logger
log_thread = threading.Thread(target=log)
#log_thread.daemon = True
button_start_log = Button(master=tkFenster, text='Start Log', command=start_log)
button_start_log.place(x=20,y=20,width=160,height=20)
#change the light from red to green2 if rec or not
recordlight = canvas.create_oval(200,30,210,40, fill='red')
#fullscreentoggle
button_fullscreen = Button(master=tkFenster, text='Fullscreen', command=toggle_fullscreen)
button_fullscreen.place(x=20,y=50,width=160,height=20)
#Nightmode/Daymode
button_nightmode = Button(master=tkFenster, text='Nightmode(Dark)', command=toggle_nightmode)
button_nightmode.place(x=190,y=50,width=160,height=20)
#open logfile location
button_logfopen = Button(master=tkFenster, text='Open Logfile Location', command=openlogfilelocation)
button_logfopen.place(x=360,y=50,width=160,height=20)
#exit button
button_exit = Button(master=tkFenster, text='Exit', command=cleanupandclose)
button_exit.place(x=530,y=50,width=160,height=20)
#get COMPORTS
refresh_portlist()
#run mainloop
tkFenster.mainloop()