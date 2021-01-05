#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox
import re
import serial

def find_ports(): #find all active COM's

        active_ports = []
        for number in range(10):
            try:
                verify = serial.Serial('COM'+str(number))
                active_ports.append((number, verify.portstr))
                verify.close()

            except serial.SerialException:
                pass
        return active_ports

def chooseCom(index): #choose COM by clicking on a label
        choosedPort = portMenu.entrycget(index, "label")
        print (choosedPort)
        pass

numPorts = find_ports()
root = Tk()
# -------------------------- Main Frames  --------------------------
toolbar = Frame(root)
data = Frame(root)

# -------------------------- Menu --------------------------
menu = Menu()
root.config(menu = menu)

subMenu = Menu(menu, tearoff = 0)
menu.add_cascade(label="Ports", menu = subMenu)

portMenu = Menu(subMenu, tearoff = 0)
for i,item in enumerate(numPorts):
        portMenu.add_command(label=str(item[-1]), command = lambda: chooseCom(i))   

serialPort = someVAr # someVar => Store the choosed label
baudRate = 9600
ser = Serial(serialPort , baudRate, timeout=0, writeTimeout=0) 

subMenu.add_cascade(label="Ports", menu = portMenu)

root.mainloop()