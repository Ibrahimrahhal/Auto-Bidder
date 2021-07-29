from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config

import time




def find_selected_elm(name, browser):
    elements = browser.find_elements(By.CLASS_NAME, "auction")
    for element in elements:
        name_elm = element.find_elements(By.CLASS_NAME, "name")
        if len(name_elm) > 0 and name in name_elm[0].text:
            return element


def find_last_bid(auction_elm): 
    last_bid_elm = auction_elm.find_element(By.CSS_SELECTOR, ".auctioneers .body .row:first-child")
    last_bid_user_name = last_bid_elm.find_element(By.CLASS_NAME, "fb-user_name").text
    last_bid_price = float(last_bid_elm.find_element(By.CLASS_NAME, "fb-bid_price").text)
    return {"name": last_bid_user_name, "price": last_bid_price}


def should_bid(last_bid):
    _name = last_bid['name']
    _price = last_bid['price']
    _should_bid = True
    if(config('YOUR_NAME') in _name):
        _should_bid = False
    if(_price > float(config('MAX_PRICE'))):
        _should_bid = False
        
    print("Last Bidder: {name}, Last Price: {price}, Should Bid: {should}".format(name=_name, price=_price, should=_should_bid))
    return _should_bid


def start(browser):
    while True:
        time.sleep(4)
        auction_target = find_selected_elm(config('ITEM_TO_TRACK_NAME'), browser)
        last_bid = find_last_bid(auction_target)
        if should_bid(last_bid):
            btn = auction_target.find_element(By.CLASS_NAME, 'btn-price')
            btn.click()


fp = webdriver.FirefoxProfile(config('FIRE_FOX_PROFILE_PATH'))
browser = webdriver.Firefox(fp)


browser.get(config('ACTION_MOBILE_AUCTION_URL'))

time.sleep(5)

start(browser)






