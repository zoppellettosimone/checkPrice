#IMPORT

from tkinter import *
import requests
from bs4 import BeautifulSoup
import time
from plyer import notification
import telegram_send

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
        title = soup.find(id="productTitle").get_text()
        #I extract the Span (html) which also contains the price
        mydivs = soup.find_all("span", {"class": "a-offscreen"})
        #I only extract the price
        price = str(mydivs[0]).replace('<span class="a-offscreen">', '').replace('€</span>', '').replace(',', '.')
        #Cast from str to float
        price = float(price)

        #Check if the price is less or equal than what we want
        if (price <= float(expectedPrice.get())):
            #Send email
            sendTelegramMessage(title)
            print("Ok")
        
        #Wait for 12 hour
        time.sleep( timeSend )

#Function for Send telegram message
def sendTelegramMessage(titleLink):
    sendMessage = "Price down for " + str(titleLink) + ": " + str(URL.pack())
    telegram_send.send(messages=[sendMessage])

#CODE

#Definition for Tkinter
root = Tk()
root.geometry('380x380')
root.title("Amazon Check Price (write by Simone Zoppelletto)")
root.configure(background='#4d0000')

#Waiting time between checks, 1 hour
timeSend = 3600

#URL input (AMAZON)
label_URL = Label(root, text="Link to the Amazon product", background='#4d0000', foreground="white", padx=10, pady=10).pack()
URL = Entry(root, width = 20)
URL.pack()

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

#Price input to check
labelExpectedPrice = Label(root, text="Expected Price", background='#4d0000', foreground="white", padx=10, pady=10).pack()
expectedPrice = Entry(root, width = 20)
expectedPrice.pack()

#Fake mail to use
#loginMail = 'checkpricebysimonez@gmail.com'
#loginPassword = "tost12345"
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

#Footer Credits
footer = Label(root, text="Created by Simone Zoppelletto", background='#4d0000', foreground="white", padx=10, pady=10).pack()

root.mainloop()