#IMPORT

from tkinter import *
import requests
from bs4 import BeautifulSoup
import time
import telegram_send

#FUNCTION:

def buttonCommand():
    checkPrice()
    root.destroy()

'''
#Function for check price product
def checkPrice():
    #Hide the window
    root.withdraw()
    #Infinite loop
    while(True):
        #Find and Take the price from .html id/class in the page url
        page = requests.get(URL.get(), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Product Name
        title = soup.find_all("div", {"class": "flex-grow-1"})
        productName = str(title[0]).replace('<div class="flex-grow-1"><h1>', '').replace('<span class="h4 text-muted font-weight-normal font-italic">Regno Glaciale - Singles</span></h1></div>', '')

        #Search the line
        linesx = soup.find_all("dt", {"class": "col-6 col-xl-5"})
        nr = findNumber(linesx)

        #I extract the dd (html) which also contains the price
        mydivs = soup.find_all("dd", {"class": "col-6 col-xl-7"})
        #I only extract the price
        price = str(mydivs[nr]).replace('<dd class="col-6 col-xl-7">', '').replace('€</dd>', '').replace(',', '.')
        #Cast from str to float
        price = float(price)
        print(price)

        #Check if the price is less or equal than what we want
        if (price <= float(expectedPrice.get())):
            #Send email
            sendTelegramMessage(productName)
            print("OK")
        
        #Wait for 12 hour
        time.sleep( timeSend )

#Function for Send telegram message
def sendTelegramMessage(titleLink):
    sendMessage = "Price down for " + str(titleLink) + ": " + str(URL.pack())
    telegram_send.send(messages=[sendMessage])

def findNumber(arr):
    for i in range(0,len(arr),1):
        contr = str(arr[i]).replace('<dt class="col-6 col-xl-5">', '').replace('</dt>', '')
        print(contr)
        if (contr == "Da"):
            return i
    return 0
'''

#Function for check price product
def checkPrice():
    #Hide the window
    root.withdraw()
    #Infinite loop
    while(True):
        #Output info
        printTime()
        #Find and Take the price from .html id/class in the page url
        page = requests.get(URL.get(), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Search the line
        linesx = soup.find_all("dt", {"class": "col-6 col-xl-5"})
        nr = findNumber(linesx)

        #I extract the dd (html) which also contains the price
        mydivs = soup.find_all("dd", {"class": "col-6 col-xl-7"})
        #I only extract the price
        price = str(mydivs[nr]).replace('<dd class="col-6 col-xl-7">', '').replace('€</dd>', '').replace(',', '.')
        print("Current Price:", price)
        #Se la carta ha un effettivo prezzo
        if(price != "N/A"):
            #Cast from str to float
            price = float(price)

            #Check if the price is less or equal than what we want
            if (price <= float(expectedPrice.get())):
                #Send email
                sendTelegramMessage()
                print("Notification sent")
            else:
                print("Price too high")
            
            #Wait
            print("Wait for next check")
            time.sleep( timeSend )
        else:
            #Wait
            print("Wait for next check")
            time.sleep( timeSend )
            #Dopo ricontrolla

#Function for Send telegram message
def sendTelegramMessage():
    sendMessage = "Price down for: " + str(URL.get())
    telegram_send.send(messages=[sendMessage])

def findNumber(arr):
    for i in range(0,len(arr),1):
        contr = str(arr[i]).replace('<dt class="col-6 col-xl-5">', '').replace('</dt>', '')
        if (contr == "Da"):
            return i
    return 0

def printTime():
    print(time.ctime())
    print("Desired Price:", expectedPrice.get())

#CODE

#Definition for Tkinter
root = Tk()
root.geometry('380x380')
root.title("CardMarket Pokemon Check Price (write by Simone Zoppelletto)")
root.configure(background='#4d0000')

#Waiting time between checks, 1 hour
timeSend = 3600

#URL input (CardMarket)
label_URL = Label(root, text="Link to the Cardmarket product", background='#4d0000', foreground="white", padx=10, pady=10).pack()
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