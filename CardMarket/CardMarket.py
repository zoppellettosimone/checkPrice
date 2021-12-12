#IMPORT

import re
import smtplib
from tkinter import *
import requests
from bs4 import BeautifulSoup
import time

#FUNCTION:

def buttonCommand():
    checkPrice()
    root.destroy()

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
            sendPositiveMail(productName)
            print("OK")
        
        #Wait for 12 hour
        time.sleep( timeSend )

#Function for Send email
def sendPositiveMail(title):
    #Definition for fake email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    #Link with fake email
    server.login(loginMail, loginPassword)

    #Send email body
    subject = "Price Down in Amazon"
    body = 'The price of "' + str(title) + '" is down, check the link ' + URL.get()

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(loginMail, mailTo.get(), msg)

    #Change time from 1 hour to 24 hour
    timeSend = 86400

def findNumber(arr):
    for i in range(0,len(arr),1):
        contr = str(arr[i]).replace('<dt class="col-6 col-xl-5">', '').replace('</dt>', '')
        print(contr)
        if (contr == "Da"):
            return i
    return 0

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

#Fake mail to use
#loginMail = 'test@gmail.com'
#loginPassword = "test123"
labelLoginMail = Label(root, text="Login Email", background='#4d0000', foreground="white", padx=10, pady=10).pack()
loginMail = Entry(root)
loginMail.pack()
labelLogin_Password = Label(root, text="Login Password", background='#4d0000', foreground="white", padx=10, pady=10).pack()
loginPassword = Entry(root, show="*")
loginPassword.pack()
mail_from = loginMail.get()

#Mail in which you will receive notifications
labelMailTo = Label(root, text="Mail", background='#4d0000', foreground="white", padx=10, pady=10).pack()
mailTo = Entry(root)
mailTo.pack()

#Like Padx, Pady but between Input Label and Button Label
skipLine = Label(root, text="", background='#4d0000', foreground="white").pack()

Button(root, text="Input", command=buttonCommand).pack()

root.mainloop()