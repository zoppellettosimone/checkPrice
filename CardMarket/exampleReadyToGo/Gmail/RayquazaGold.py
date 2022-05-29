#IMPORT

import re
import smtplib
import requests
from bs4 import BeautifulSoup
import time

#FUNCTION:

#Function for check price product
def checkPrice():
    #Infinite loop
    while(True):
        #Output info
        printTime()
        #Find and Take the price from .html id/class in the page url
        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Product Name
        title = soup.find_all("div", {"class": "flex-grow-1"})
        productName = str(title[0]).replace('<div class="flex-grow-1"><h1>', '').replace('<span class="h4 text-muted font-weight-normal font-italic">Regno Glaciale - Singles</span></h1></div>', '').replace('<span class="h4 text-muted font-weight-normal font-italic">VMAX Climax - Singles</span></h1></div>', '')

        #Search the line
        linesx = soup.find_all("dt", {"class": "col-6 col-xl-5"})
        nr = findNumber(linesx)

        #I extract the dd (html) which also contains the price
        mydivs = soup.find_all("dd", {"class": "col-6 col-xl-7"})
        #I only extract the price
        price = str(mydivs[nr]).replace('<dd class="col-6 col-xl-7">', '').replace('€</dd>', '').replace(',', '.')
        print("Prezzo attuale:", price)
        #Se la carta ha un effettivo prezzo
        if(price != "N/A"):
            #Cast from str to float
            price = float(price)

            #Check if the price is less or equal than what we want
            if (price <= float(pricePerfect)):
                #Send email
                sendPositiveMail(productName)
                print("Mail inviata")
            else:
                print("Prezzo troppo alto")
            
            #Wait for 12 hour
            print("Wait for next check")
            time.sleep( timeSend )
        else:
            #Wait for 12 hour
            print("Wait for next check")
            time.sleep( timeSend )
            #Dopo ricontrolla

#Function for Send email
def sendPositiveMail(title):
    #Definition for fake email server
    server = smtplib.SMTP('smtp.mail.yahoo.com.', 465)
    server.ehlo()
    server.starttls()
    server.ehlo()

    #Fake mail info (!!!!! TO INSERT !!!!!)
    fakeGmail = ""
    fakePassword = ""

    #Link with fake email
    server.login(fakeGmail, fakePassword)

    #Send email body
    subject = "Price Down in Cardmarket"
    body = 'The price of "' + str(title) + '" is down, check the link ' + link

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(fakeGmail, "zoppellettosimone@gmail.com", msg)

    #Change time from 1 hour to 24 hour
    timeSend = 86400

def findNumber(arr):
    for i in range(0,len(arr),1):
        contr = str(arr[i]).replace('<dt class="col-6 col-xl-5">', '').replace('</dt>', '')
        if (contr == "Da"):
            return i
    return 0

def printTime():
    print(time.ctime())
    print("Nome carta: Rayquaza Black Gold (s8b)")
    print("Prezzo voluto:", pricePerfect)

#CODE

#Waiting time between checks, 1 hour
timeSend = 3600

pricePerfect = 3000

link = "https://www.cardmarket.com/it/Pokemon/Products/Singles/VMAX-Climax/Rayquaza-VMAX-V3-s8b284?sellerCountry=17&sellerType=0,1,2&language=7"
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

checkPrice()