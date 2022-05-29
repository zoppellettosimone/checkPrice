#IMPORT

import re
import smtplib
from tkinter import *
import requests
from bs4 import BeautifulSoup
import time
from shutil import copyfile

#FUNCTION:

def buttonCommand():
    createProgram()
    root.destroy()

#Function for check price product
def createProgram():
    #Hide the window
    root.withdraw()
    #Creation of MyReadyToGoProgram.py file from TemplateReadyToGo.py
    copyfile("template/TemplateReadyToGoNotification.py", "MyReadyToGoNotification.py")
    
    #Read MyReadyToGoNotification.py
    with open('MyReadyToGoNotification.py', 'r') as file :
        filedata = file.read()

    #Replace link and price
    filedata = filedata.replace('LINKTOCHANGE', URL.get())
    filedata = filedata.replace('PRICETOCHANGE', expectedPrice.get())

    #Write the file out again
    with open('MyReadyToGoNotification.py', 'w') as file:
        file.write(filedata)

    #Creation of MyReadyToGoProgram.bat file
    with open("MyReadyToGoNotification.bat", "w") as file:
        file.write("%CD%\n")
        file.write("Python MyReadyToGoNotification.py\n")
    

#CODE

#Definition for Tkinter
root = Tk()
root.geometry('380x380')
root.title("CardMarket Check Price (write by Simone Zoppelletto)")
root.configure(background='#4d0000')

#Waiting time between checks, 1 hour
timeSend = 3600

#URL input (AMAZON)
label_URL = Label(root, text="Link to the CardMarket product", background='#4d0000', foreground="white", padx=10, pady=10).pack()
URL = Entry(root, width = 20)
URL.pack()

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

#Price input to check
labelExpectedPrice = Label(root, text="Expected Price", background='#4d0000', foreground="white", padx=10, pady=10).pack()
expectedPrice = Entry(root, width = 20)
expectedPrice.pack()

#Like Padx, Pady but between Input Label and Button Label
skipLine = Label(root, text="", background='#4d0000', foreground="white").pack()

Button(root, text="Input", command=buttonCommand).pack()

#Footer Credits
footer = Label(root, text="Created by Simone Zoppelletto", background='#4d0000', foreground="white", padx=10, pady=10).pack()

root.mainloop()