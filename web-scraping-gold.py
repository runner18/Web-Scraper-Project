'''
    ECCS 4411: Programming Languages
    Author: Dr. Al-Haj, October 2021

    Description:
    * This code scrapes two web pages, www.apmex.com and www.ebay.com, and
    finds 1) the current gold price per ounce and 2) the information of the
    first listed item in the searched eBay page.

'''

from bs4 import BeautifulSoup
import requests
import regex
from re import sub
from decimal import Decimal

global kitcoPrice
global apmexPrice
global reasonablePrice

def scrape_kitco():

    global kitcoPrice
    # get the monex webpage:
    url = "https://www.kitco.com/charts/livegold.html"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrapes the current price
    # syntax for the HTML element was: <p class="price">$1,901.30 USD</p>
    price = soup.find("span", {"id": "sp-bid"}).get_text()

    kitcoPrice = float(sub(r'[^\d.]', '', price))

    # Prints the url and the current gold price
    print(url)
    print("Current Gold Price @ KITCO: " + price + "\n")


# Scrape and print the url and the current gold prices posted on APMEX page
def scrape_apmex():
    global apmexPrice
    #get the apmex webpage:
    url = "https://www.apmex.com/gold-price"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Scrapes the current price
    # syntax for the HTML element was: <p class="price">$1,901.30 USD</p>
    price = soup.find("p", {"class": "price"}).get_text()
    apmexPrice = float(sub(r'[^\d.]', '', price))

    # Prints the url and the current gold price
    print(url)
    print("Current Gold Price @ APMEX: " + price + "\n")

# Scarpe and print the url, item description, and price for the first result
# def scrape_ebay():
#     ebay_keywords = ["gold+eagle+1+oz+50"]
#     url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312&_nkw="
#
#     search_url = url + ebay_keywords[0]
#
#     search_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=gold+eagle+1+oz+50&LH_Auction=1&_sop=1"
#     response = requests.get(search_url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")
#
#
#
#     # syntax for the HTML element was: <h3 class="s-item__title">2021 American Gold Eagle 1 oz $50 - BU</h3>
#     description = soup.find("h3", {"class": "s-item__title"}).get_text(separator=u" ")
#
#
#     # syntax for the HTML element was: <span class="s-item__price">$2,032.88</span>
#     price = soup.find("span", {"class": "s-item__price"}).get_text()
#     # another way:
#     #price = soup.find("span", class_= "s-item__price").get_text()
#
#     # display results:
#     print(search_url)
#     print("Item Description: " + description)
#     print("Price: " + price + "\n")

def recently_auctioned(keywords):
    ebay_keywords = keywords #["gold+eagle+ 1+oz+50"]
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312&_nkw="

    search_url = url + keywords + "+Auction=1+Complete=1+Sold=1"

    response = requests.get(search_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # syntax for the HTML element was: <h3 class="s-item__title">2021 American Gold Eagle 1 oz $50 - BU</h3>
    #description = soup.find_all("h3", {"class": "s-item__title"}).get_text(separator=u" ")

    # syntax for the HTML element was: <span class="s-item__price">$2,032.88</span>
    listings = soup.find('li',attrs={'class':'s-item'})
    prices = soup.find("span", {"class": "s-item__price"})
    results = soup.find("span",{"class":"BOLD"})

    prices = [element.text for element in prices]

    new_prices = []

    for price in prices:
        new_prices.append(Decimal(sub(r'[^\d.]', '', price)))

    prices[0] = Decimal(sub(r'[^\d.]', '', prices[0]))
    #new_prices = [float(price) for price in prices]

    # another way:
    # price = soup.find("span", class_= "s-item__price").get_text()

    if(len(new_prices) >= 25):
        new_prices = new_prices[0:25]

    summary = sum(new_prices)
    length = len(new_prices)

    average = 0
    average = sum(new_prices) / len(new_prices)

    # display results:
    print(search_url)
    #print("Item Description: " + description)
    print("Average price recently sold (auction): " + str(average) + "\n")

def recently_sold(keywords):
    ebay_keywords = keywords #["gold+eagle+1+oz+50"]
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312&_nkw="

    search_url = url + keywords + "+Auction=1+Complete=1+Sold=1+BIN=1"

    response = requests.get(search_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # syntax for the HTML element was: <h3 class="s-item__title">2021 American Gold Eagle 1 oz $50 - BU</h3>
    # description = soup.find_all("h3", {"class": "s-item__title"}).get_text(separator=u" ")

    # syntax for the HTML element was: <span class="s-item__price">$2,032.88</span>
    listings = soup.find('li', attrs={'class': 's-item'})
    prices = soup.find("span", {"class": "s-item__price"})
    results = soup.find("span", {"class": "BOLD"})

    prices = [element.text for element in prices]

    new_prices = []

    for price in prices:
        new_prices.append(Decimal(sub(r'[^\d.]', '', price)))

    prices[0] = Decimal(sub(r'[^\d.]', '', prices[0]))
    # new_prices = [float(price) for price in prices]

    # another way:
    # price = soup.find("span", class_= "s-item__price").get_text()

    if (len(new_prices) >= 25):
        new_prices = new_prices[0:25]

    summary = sum(new_prices)
    length = len(new_prices)

    average = 0
    average = sum(new_prices) / len(new_prices)

    # display results:
    print(search_url)
    print("Average price recently sold (buy it now): " + str(average) + "\n")

def endingInOneHour(keywords):
    print('\n~~~items that will sell out in one hour~~~')
    ebay_keywords = keywords #"gold+eagle+1+oz+50"]
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="

    search_url = url + keywords + "&_sop=1"
    #search_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=gold+eagle+1+oz+50&_sop=1"
    response = requests.get(search_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # syntax for the HTML element was: <h3 class="s-item__title">2021 American Gold Eagle 1 oz $50 - BU</h3>
    # description = soup.find_all("h3", {"class": "s-item__title"}).get_text(separator=u" ")

    # syntax for the HTML element was: <span class="s-item__price">$2,032.88</span>
    listings = soup.find_all('li', attrs={'class': 's-item s-item__pl-on-bottom s-item--watch-at-corner'})

    goldPriceAvg = (kitcoPrice + apmexPrice) / 2
    reasonablePrice = goldPriceAvg + (goldPriceAvg * float(.1)) +200
    anyProducts = False
    for list in listings:

        itemPrice = list.find("span", {"class": "s-item__price"})
        itemPrice.text
        #print(itemPrice.text)

        timeLeft = list.find("span", {"class": "s-item__time-left"})
        itemDesc = list.find("h3", {"class":"s-item__title"})
        itemUrl = list.find("a", {"class":"s-item__link"})
        itemAttrs = itemUrl.attrs


        #print(timeLeft.text)



        if(timeLeft is not None and itemPrice is not None):
            itemPriceDec = Decimal(sub(r'[^\d.]', '', itemPrice.text))
            if(itemPriceDec < reasonablePrice):

                timeLeftList = timeLeft.text.split(' ')
                #print(timeLeftList)
                if('1h' in timeLeftList):# and 'd' not in timeLeft.text):
                    anyProducts = True
                    print(itemDesc.text)
                    print(itemPrice.text)
                    print(itemAttrs['href'])
                    print(timeLeft.text)

                    print('\n')

    if (anyProducts == False):
        print("Could not find any auctions (at a reasonable price) that will end in one hour")

    # display results:
    #print(search_url)
    #print("Listings that will end in one hour: " + str(average) + "\n")

def buyItNow(keywords):
    print('\n~~~buy it now items~~~')
    ebay_keywords = keywords #"gold+eagle+1+oz+50"]
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="

    search_url = url + keywords + "&_sop=1&rt=nc&LH_BIN=1"
    #search_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=gold+eagle+1+oz+50&_sop=1"
    response = requests.get(search_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # syntax for the HTML element was: <h3 class="s-item__title">2021 American Gold Eagle 1 oz $50 - BU</h3>
    # description = soup.find_all("h3", {"class": "s-item__title"}).get_text(separator=u" ")

    # syntax for the HTML element was: <span class="s-item__price">$2,032.88</span>
    listings = soup.find_all('li', attrs={'class': 's-item s-item__pl-on-bottom s-item--watch-at-corner'})

    goldPriceAvg = (kitcoPrice + apmexPrice) / 2
    reasonablePrice = goldPriceAvg + (goldPriceAvg * float(.1)) + 200
    anyProducts = False
    for list in listings:

        itemPrice = list.find("span", {"class": "s-item__price"})
        itemPrice.text
        #print(itemPrice.text)

        timeLeft = list.find("span", {"class": "s-item__time-left"})
        itemDesc = list.find("h3", {"class":"s-item__title"})
        itemUrl = list.find("a", {"class":"s-item__link"})
        itemAttrs = itemUrl.attrs


        #print(timeLeft.text)



        if(timeLeft is not None and itemPrice is not None):
            itemPriceDec = Decimal(sub(r'[^\d.]', '', itemPrice.text))
            if(itemPriceDec < reasonablePrice):

                timeLeftList = timeLeft.text.split(' ')
                #print(timeLeftList)
                #if('1h' in timeLeftList):# and 'd' not in timeLeft.text):
                anyProducts = True
                print(itemDesc.text)
                print(itemPrice.text)
                print(itemAttrs['href'])
                print(timeLeft.text)

                print('\n')

    if (anyProducts == False):
        print("Could not find any buy it now products (at a reasonable price)")

# main program

if __name__ == '__main__':


    print('----------Checking Current Gold Price of APMEX and MITCO----------')
    scrape_apmex()
    scrape_kitco()
    input("Press Enter to continue...")

    #new_prices = []

    print('\n\n----------Information for Gold Eagle 1oz Coins----------')
    recently_auctioned('gold+eagle+ 1+oz+50')
    recently_sold('gold+eagle+ 1+oz+50')
    endingInOneHour('gold+eagle+ 1+oz+50')
    buyItNow('gold+eagle+ 1+oz+50')
    input("Press Enter to continue...")

    print('\n\n----------Information for Maple Leaf 1oz Coins----------')
    recently_auctioned('gold+maple+leaf+ 1+oz+50')
    recently_sold('gold+maple+leaf+ 1+oz+50')
    endingInOneHour('gold+maple+leaf+ 1+oz+50')
    buyItNow('gold+maple+leaf+ 1+oz+50')
    input("Press Enter to continue...")