from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import time
import struct
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep
from datetime import datetime
import json
import time
from datetime import datetime
import serial
import threading

millis = (round(time.time()))
INPUT_PIN = 37
INPUT_PIN1 = 35
print(millis)
currentTime = millis
startTime = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
my_file = open(startTime+".txt","w+")
my_file.write("Start Time:"+startTime+"\r\n")
my_file.close()
ser = serial.Serial('COM4',9600,timeout =1)
root = Tk()
var = IntVar()
root.title("AP Vent")
root.configure(background= 'black')
root.geometry("1200x800")


left = Frame(root, width=600, background="deep sky blue")
right = Frame(root ,background="deep sky blue")
left.pack_propagate(False)
right.pack_propagate(False)
container = Frame(left, borderwidth=2,background="deep sky blue")

box1 = Frame(right, borderwidth=2, background="pale green")
box2 = Frame(left, borderwidth=2, background="pale green")
heading = Frame(box2);
spinboxlabel1 = Frame(box1, bd="1", relief="solid");
spinboxlabel5 = Frame(box2, bd="1", relief="solid");
spinboxes1 = Frame(box1);
spinboxes12 = Frame(box2);

spinboxlabel2 = Frame(box1, bd="1", relief="solid");
spinboxes2 = Frame(box1);
spinboxes21 = Frame(box2);
spinboxlabel3 = Frame(box1,bd="1", relief="solid");
spinboxes3 = Frame(box1);
spinboxlabel4 = Frame(box1,bd="1", relief="solid");
spinboxes4 = Frame(box1);
spinboxes5 = Frame(box2);
heading2 = Frame(box2);
radiogrp1 = Frame(box2);
radiogrp2 = Frame(box2);
btngroup=Frame(box2);

fig=Figure(figsize=(12,2.4), dpi=80);
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, container)
fig1=Figure(figsize=(12,2.4), dpi=80);
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, container)

ax1.set_title('Volume/time',color='black',weight="bold")
ax1.set_ylabel('Volume',color='w',weight="bold")
ax1.xaxis.label.set_color('black')
ax1.tick_params(axis='x',colors='black')
ax1.yaxis.label.set_color('black')
ax1.tick_params(axis='y',colors='black')
ax1.grid(True)
ax1.set_facecolor('lightblue')
ax1.autoscale_view(True,True,True)

fig2=Figure(figsize=(12,2.4), dpi=80);
ax2 = fig2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(fig2, container)

ax2.set_title('Flow(L/min)',color='black',weight="bold")
ax2.set_ylabel('Flow(l/min)',color='w',weight="bold")
ax2.xaxis.label.set_color('black')
ax2.tick_params(axis='x',colors='black')
ax2.yaxis.label.set_color('black')
ax2.tick_params(axis='y',colors='black')
ax2.grid(True)
ax2.set_facecolor('lightblue')
ax2.autoscale_view(True,True,True)

def close():
    response = messagebox.askokcancel("Confirmation", "Press OK to Exit or Cancel to return?")
    if response == True:
        my_file = open(startTime+".txt","a+")
        my_file.write("Program closed at ")
        my_file.write(datetime.now().strftime("%d-%m-%Y_%H-%M-%S_%p")+"\r\n")
    ##    ser.close()
        my_file.close()
        print("Program Closing")
        root.destroy()
def stop():
    response = messagebox.askokcancel("Confirmation", "Press OK to Stop Ventilator operation or Cancel to return?")
    if response == True:
        my_file = open(startTime+".txt","a+")
        my_file.write("Operation Stopped at ")
        my_file.write(datetime.now().strftime("%d-%m-%Y_%H-%M-%S_%p")+"\r\n")
        my_file.close()
        my_file = open(startTime+".txt","a+")
    

btnQuit = Button(box2, text="Quit Application", background= "sky blue",relief="solid",command=close)
btnStop = Button(box2, text="Stop", background= "sky blue",relief="solid",command=stop)

#Manual Mode Controls
label7 = Label(spinboxlabel1, text="VT(L)", width=10, borderwidth=1, relief="solid",
               font=Font(family='Times', size=10, weight='bold'),background="sky blue")

labelV1 = Label(spinboxes1, width=8, height=2, borderwidth=1, relief="solid",
               font=Font(family='Times', size=45, weight='bold'),background="sky blue")
label8 = Label(spinboxlabel2, text="MV(L/min)", width=10,  borderwidth=1, relief="solid",
               font=Font(family='Times', size=10, weight='bold'),background="sky blue")
labelV2 = Label(spinboxes2, width=8,height=2, borderwidth=1, relief="solid",
               font=Font(family='Times', size=45, weight='bold'),background="sky blue")
label81 = Label(spinboxlabel3, text="FLOW(L/min)", width=10,  borderwidth=1, relief="solid",
               font=Font(family='Times', size=8, weight='bold'),background="sky blue")
labelV21 = Label(spinboxes3, width=8, height=2,borderwidth=1, relief="solid",
               font=Font(family='Times', size=45, weight='bold'),background="sky blue")
label82 = Label(spinboxlabel4, text="PIP(cmh2O)", width=10,  borderwidth=1, relief="solid",
               font=Font(family='Times', size=8, weight='bold'),background="sky blue")
labelV22 = Label(spinboxes4, width=8,height=2, borderwidth=1, relief="solid",
               font=Font(family='Times', size=45, weight='bold'),background="sky blue")

spin1 = Scale(spinboxes12, label="I:E", from_=1, to=3, orient=HORIZONTAL,
              font=Font(family='Courier', size=13, weight='bold'), background="sky blue",relief="solid")
spin2 = Scale(spinboxes12, label="BPM", from_=8, to=30, orient=HORIZONTAL,
              font=Font(family='Courier', size=13, weight='bold'), background="sky blue",relief="solid")
spin3 = Scale(spinboxes12, label="PIP", from_=5, to=35, orient=HORIZONTAL,
              font=Font(family='Courier', size=13, weight='bold'), background="sky blue",relief="solid")
spin4 = Scale(spinboxes12, label="PEEP", from_=5, to=25, orient=HORIZONTAL,
              font=Font(family='Courier', size=13, weight='bold'), background="sky blue",relief="solid")
spin5 = Scale(spinboxes12, label="Tidal Vol (mL)", from_=5, to=25, orient=HORIZONTAL,
              font=Font(family='Courier', size=13, weight='bold'), background="sky blue",relief="solid")


def startPCV():
    pip = int(spin3.get())
    peep = int(spin4.get())
    tidalvol = spin5.get()
    currentie= spin1.get()
    bpm=spin2.get()
    ser.write(struct.pack('>BBBBB', 10, currentie, bpm, pip, peep));
    container.after(500, ardDataReader(pip, peep, currentie, bpm, tidalVol))



def startVCV():
    print("open")
    pip = spin3.get()
    peep = spin4.get()
    currentie= spin1.get()
    bpm=spin2.get()
    tidalVol = spin5.get()
    GUI = threading.Thread(target=ardDataReader(pip, peep, currentie, bpm, tidalVol))
    GUI.start()

def startSIMVPC():
    pip = spin3.get()
    peep = spin4.get()
    tidalvol = spin5.get()
    global flagSIMVPCV
    flagSIMVPCV = True


def startSIMVVC():
    pip = spin3.get()
    peep = spin4.get()
    tidalvol = spin5.get()
    global flagSIMVVCV
    flagSIMVVCV = True

btnStartPCV = Button(btngroup, text="Start PCV)", command=startPCV,
                        font=Font(family='Courier', size=13, weight='bold'))
btnStartVCV = Button(btngroup, text="Start VCV", command=startVCV,
                     font=Font(family='Courier', size=13, weight='bold'))
btnStartSIMVPC = Button(btngroup, text="Start SIMV-PC", command=startSIMVPC,
                        font=Font(family='Courier', size=13, weight='bold'))
btnStartSIMVVC= Button(btngroup, text="Start SIMV-VC)", command=startSIMVVC,
                        font=Font(family='Courier', size=13, weight='bold'))

        
def ardDataReader(pip, peep, currentie, bpm, tidalVolume):
   
    GAIN = 2/3
    sum1 = 0
    P = [
    F = []
    CM=[]
    x,y=[],[]
    def plot_2(i):
        tidal = 0.0
        ser.flush()
        if ser.in_waiting > 0:
            tidal = float(ser.readline().decode('utf-8').strip())
            print(tidal)
            if (tidal>=0.0):
                volFlow = tidal
                volFlowInt = int(volFlow)
                volFlowStr = str(volFlowInt)
                MinFlow = int(volFlowInt*bpm)
                MinFlowStr = str(MinFlow)
                labelV1.configure(text=volFlowStr)
                F.append(volFlowInt)
                x.append(len(F))
            elif (tidal<0.0):
                volFlow = -tidal
                volFlowInt = int(volFlow)
                volFlowStr = str(volFlowInt)
                MinFlow = int(volFlowInt*bpm)
                MinFlowStr = str(MinFlow)
                labelV1.configure(text=volFlowStr)
                F.append(volFlowInt)
                x.append(len(F))
            lines1.set_ydata(F)
            lines1.set_xdata(np.arange(0,len(F)))
            fig1.canvas.draw()
            ax1.set_xlim(left=max(0, i-20), right=i+1)
            ax1.set_ylim(min(F)-2,max(F)+2)
    global lines1
    lines1 = ax1.plot([],[],'b')[0]
    global anim1
    anim1 = animation.FuncAnimation(fig, plot_2, interval = 10)
    canvas.draw()


canvas1.get_tk_widget().grid(row = 1, column = 0)
fig1.patch.set_facecolor('lightblue')
label9 = Label(box1,background="khaki")
label10 = Label(box1,background="khaki")
label12 = Label(box2,background="khaki")
label13 = Label (box2,background="khaki")

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container.pack(expand=True, fill="both", padx=3, pady=2)

box1.pack(expand=True, fill="both", padx=3, pady=3)
box2.pack(expand=True, fill="both", padx=3, pady=3)
heading.pack(pady=7)
spinboxlabel5.pack();
spinboxes12.pack(pady=10);
spinboxes21.pack();
spinboxlabel2.pack(pady=3)
spinboxes2.pack()
spinboxlabel1.pack()
spinboxes1.pack(pady=3)
spinboxlabel3.pack()
spinboxes3.pack(pady=3)

spinboxlabel4.pack()
spinboxes4.pack(pady=3)
btngroup.pack(pady=5)
btnStop.pack(side="left", padx=250)
btnQuit.pack(side="left", padx=80)

label7.pack(side="left") #PIP
labelV1.pack(side="left")
label8.pack(side="left") #PEEP
labelV2.pack(side="left") #PEEP
label81.pack(side="left") #PEEP
labelV21.pack(side="left") #PEEP
label82.pack(side="left") #PEEP
labelV22.pack(side="left") #PEEP

#Sliders
spin1.pack(side="left") #IE
spin2.pack(side="left") #bpm
spin3.pack(side="left") #PIP
spin4.pack(side="left") #PEEP
spin5.pack(side="left")

#Mode buttons
btnStartPCV.pack(side="left")
btnStartVCV.pack(side="left",padx=7)
btnStartSIMVPC.pack(side="left",padx=7)
btnStartSIMVVC.pack(side="left")

root.mainloop()
