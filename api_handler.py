#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib2
import math
import datetime
import time

BTC = 0
ETH = 1
LTC = 2
DASH = 3
XMR = 4
ZEC = 5
ALIS = 0
SATIS = 1
market_BTC = ["Bitfinex", "Gemini", "Poloniex", "Bitstamp", "Kraken", "BitTrex", "OKCoin", "Cexio", "BTCE", "Coinbase"]
market_ALTCOIN = ["Poloniex", "Bitfinex", "BitTrex", "Kraken"]
market_LTC = ["Poloniex", "Bitfinex", "BitTrex", "Kraken"]

kur_url = "http://www.doviz.com/api/v1/currencies/USD/latest"
b = requests.get(kur_url).json()
tl_deger = b["selling"]


def calculate_after_fee_amounts(price,market,currency_id,is_buying,BTC_dic,ETH_dic,LTC_dic,DASH_dic,XMR_dic,ZEC_dic):
    """
    fee'lerde key ve values var. Values'de sırasıyla tüm altcoinlerin fee miktarları var. her altcoin içinde bir array daha var
    o da sırasıyla alış ve satış fee'sidir.
    TL olarak hesaplar geri kalan parayı
    TL olarak girilmelidir price

    currency id BTC-0, ETH-1 vs
    is_buying , 1 ve ya 0
    """
    price = price / 100.0

    fees = {}
    fees["Bitfinex"] = [[price*0.2,0.0004*BTC_dic["Bitfinex"]], [price*0.2,0.01*ETH_dic["Bitfinex"]], [price*0.2,0.001*LTC_dic["Bitfinex"]],  [price*0.2,0.01*DASH_dic["Bitfinex"]], [price*0.2,0.01*XMR_dic["Bitfinex"]], [price*0.2,0.001*ZEC_dic["Bitfinex"]] ]
    fees["Gemini"] = [[price*0.15,price*0.15],[],[],[],[],[] ]
    fees["Poloniex"] = [[price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25]]
    fees["Bitstamp"] = [[price*0.25,price*0.25],[],[],[],[],[]]
    fees["Kraken"] = [[price*0.26,price*0.26], [price*0.26,price*0.26], [price*0.26,price*0.26], [price*0.26,price*0.26], [price*0.26,price*0.26], [price*0.26,price*0.26]]
    fees["BitTrex"] = [[price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25], [price*0.25,price*0.25]]
    fees["OKCoin"] = [[price*0.2,price*0.2],[],[],[],[],[]]
    fees["Cexio"] = [[price*0.2,price*0.2],[],[],[],[],[]]
    fees["BTCE"] = [[price*0.2,(price*0.2)+0.001*BTC_dic["BTCE"]],[],[],[],[],[]]
    fees["Coinbase"] = [[price*1.49,price*1.49],[],[],[],[],[]]
    fees["Paribu"] = [[price*0.4,price*0.4],[],[],[],[],[]]
    fees["Koinim"] = [[price*0.4+0.5,(price*0.4)+3.5+(0.0015*BTC_dic["Koinim"])], [],[price*0.4+0.5,(price*0.4)+3.5+(0.015*LTC_dic["Koinim"])],[],[],[]]

    remaining = 0
    price = price * 100.0
    remaining = price - fees[market][currency_id][is_buying]

    return remaining


def get_koinim_BTC_and_LTC_price():
    request_url_BTC = "https://coinmarketcap.com/exchanges/koinim/"
    sum_BTC = urllib2.urlopen(request_url_BTC).read()
    sum_BTC = sum_BTC[sum_BTC.find("Updated"):]
    sum_BTC = sum_BTC[sum_BTC.find("data-usd") + 5:]
    sum_BTC = sum_BTC[sum_BTC.find("data-usd"):]
    s = sum_BTC.find("\"") + 1
    e = sum_BTC[s + 1:].find("\"") + 1

    BTCp = float(sum_BTC[10:s + e])

    sum_BTC = sum_BTC[sum_BTC.find("data-usd") + 5:]
    sum_BTC = sum_BTC[sum_BTC.find("data-usd") + 5:]
    sum_BTC = sum_BTC[sum_BTC.find("data-usd"):]

    s = sum_BTC.find("\"") + 1
    e = sum_BTC[s + 1:].find("\"") + 1
    LTCp = float(sum_BTC[10:s + e])

    if LTCp > BTCp:
        tmp = BTCp
        BTCp = LTCp
        LTCp = tmp

    return BTCp,LTCp

get_koinim_BTC_and_LTC_price()

def get_paribu_price():
    request_url_BTC = "https://coinmarketcap.com/exchanges/paribu"
    sum_BTC = urllib2.urlopen(request_url_BTC).read()
    sum_BTC = sum_BTC[sum_BTC.find("Updated"):]
    sum_BTC = sum_BTC[sum_BTC.find("data-usd")+5:]
    sum_BTC = sum_BTC[sum_BTC.find("data-usd"):]
    s = sum_BTC.find("\"") + 1
    e = sum_BTC[s+1:].find("\"") + 1
    return sum_BTC[10:s+e]


def initialize_prices():
    BTC_prices = []
    ETH_prices = []
    LTC_prices = []
    DASH_prices = []
    XMR_prices = []
    ZEC_prices = []

    for i in market_BTC:
        request_url_BTC = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&e=" + i
        sum_BTC = requests.get(request_url_BTC).json()["USD"] * tl_deger
        # print i + " : " + str(sum_BTC)
        BTC_prices.append(sum_BTC)

    for i in market_ALTCOIN:
        if i == "BitTrex":
            typ = "BTC"
            carpan = BTC_prices[5]
        else:
            typ = "USD"
            carpan = tl_deger

        request_url_ETH = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms="+typ+"&e=" + i
        request_url_LTC= "https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms="+typ+"&e=" + i
        request_url_DASH = "https://min-api.cryptocompare.com/data/price?fsym=DASH&tsyms="+typ+"&e=" + i
        request_url_XMR = "https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms="+typ+"&e=" + i
        request_url_ZEC  = "https://min-api.cryptocompare.com/data/price?fsym=ZEC&tsyms="+typ+"&e=" + i

        sum_ETH = requests.get(request_url_ETH).json()[typ] * carpan
        sum_LTC = requests.get(request_url_LTC).json()[typ] * carpan
        sum_DASH = requests.get(request_url_DASH).json()[typ] * carpan
        sum_XMR = requests.get(request_url_XMR).json()[typ] * carpan
        sum_ZEC = requests.get(request_url_ZEC).json()[typ] * carpan

        #print  i+" : " + str(sum_ETH) +","+str(sum_LTC)+","+str(sum_DASH)+","+str(sum_XMR)+","+str(sum_ZEC)
        ETH_prices.append(sum_ETH)
        LTC_prices.append(sum_LTC)
        DASH_prices.append(sum_DASH)
        XMR_prices.append(sum_XMR)
        ZEC_prices.append(sum_ZEC)


    market_BTC.append("Paribu")
    market_BTC.append("Koinim")
    BTC_prices.append(float(get_paribu_price())*tl_deger)
    koinim_BTC,koinim_LTC = get_koinim_BTC_and_LTC_price()
    BTC_prices.append(float(koinim_BTC) * tl_deger)
    market_LTC.append("Koinim")
    LTC_prices.append(float(koinim_LTC) * tl_deger)

    BTC_dic = {}
    ETH_dic = {}
    LTC_dic = {}
    DASH_dic = {}
    XMR_dic = {}
    ZEC_dic = {}

    for idx,i in enumerate(market_BTC):
        BTC_dic[i] = BTC_prices[idx]
    for idx,i in enumerate(market_ALTCOIN):
        ETH_dic[i] = ETH_prices[idx]
    for idx,i in enumerate(market_ALTCOIN):
        DASH_dic[i] = DASH_prices[idx]
    for idx,i in enumerate(market_ALTCOIN):
        XMR_dic[i] = XMR_prices[idx]
    for idx,i in enumerate(market_ALTCOIN):
        ZEC_dic[i] = ZEC_prices[idx]
    for idx,i in enumerate(market_LTC):
        LTC_dic[i] = LTC_prices[idx]

    return BTC_dic,ETH_dic,LTC_dic,DASH_dic,XMR_dic,ZEC_dic


def get_minutely_statistics(coin_type,min_back):
    """
    Geçmiş 1 günün dakika olarak datasını dönderir
    """

    hourly_data = {}
    to_time = get_current_utc_timestamp()

    if coin_type == 0:
        typo = "BTC"
        market = market_BTC
    elif coin_type == 1:
        typo = "ETH"
        market = market_ALTCOIN
    elif coin_type == 2:
        typo = "LTC"
        market = market_LTC
    elif coin_type == 3:
        typo = "DASH"
        market = market_ALTCOIN
    elif coin_type == 4:
        typo = "XMR"
        market = market_ALTCOIN
    elif coin_type == 5:
        typo = "ZEC"
        market = market_ALTCOIN

    for i in market:
        open_price_arr = []
        close_price_arr = []
        high_price_arr = []
        low_price_arr = []
        time_arr = []
        request_url = "https://min-api.cryptocompare.com/data/histominute?fsym="+str(typo)+"&tsym=USD&limit="+str(min_back)+"&aggregate=1&toTs="+str(to_time)+"&e=" + i
        returned = requests.get(request_url).json()["Data"]

        for k in returned:
            high_price_arr.append(k["high"])
            low_price_arr.append(k["low"])
            open_price_arr.append(k["open"])
            close_price_arr.append(k["close"])
            time_arr.append(datetime.datetime.utcfromtimestamp(int(k["time"])).strftime('%Y-%m-%dT%H:%M:%SZ'))
        hourly_data[i] = [high_price_arr,low_price_arr,open_price_arr,close_price_arr,time_arr]

    return hourly_data


def get_hourly_statistics(coin_type,hour_back):
    """
    Geçmiş 1 haftanın saat olarak datasını dönderir
    """
    hourly_data = {}
    to_time = get_current_utc_timestamp()
    if coin_type == 0:
        typo = "BTC"
        market = market_BTC
    elif coin_type == 1:
        typo = "ETH"
        market = market_ALTCOIN
    elif coin_type == 2:
        typo = "LTC"
        market = market_LTC
    elif coin_type == 3:
        typo = "DASH"
        market = market_ALTCOIN
    elif coin_type == 4:
        typo = "XMR"
        market = market_ALTCOIN
    elif coin_type == 5:
        typo = "ZEC"
        market = market_ALTCOIN

    for i in market:
        open_price_arr = []
        close_price_arr = []
        high_price_arr = []
        low_price_arr = []
        time_arr = []
        request_url = "https://min-api.cryptocompare.com/data/histohour?fsym="+str(typo)+"&tsym=USD&limit="+str(hour_back)+"&aggregate=1&toTs="+str(to_time)+"&e=" + i
        returned = requests.get(request_url).json()["Data"]
        for k in returned:
            high_price_arr.append(k["high"])
            low_price_arr.append(k["low"])
            open_price_arr.append(k["open"])
            close_price_arr.append(k["close"])
            time_arr.append(datetime.datetime.utcfromtimestamp(int(k["time"])).strftime('%Y-%m-%dT%H:%M:%SZ'))
        hourly_data[i] = [high_price_arr,low_price_arr,open_price_arr,close_price_arr,time_arr]

    return hourly_data


def get_daily_statistics(coin_type,day_back):
    """
    Geçmiş 3 ayın gün olarak datasını gösterir
    """
    hourly_data = {}
    to_time = get_current_utc_timestamp()
    if coin_type == 0:
        typo = "BTC"
        market = market_BTC
    elif coin_type == 1:
        typo = "ETH"
        market = market_ALTCOIN
    elif coin_type == 2:
        typo = "LTC"
        market = market_LTC
    elif coin_type == 3:
        typo = "DASH"
        market = market_ALTCOIN
    elif coin_type == 4:
        typo = "XMR"
        market = market_ALTCOIN
    elif coin_type == 5:
        typo = "ZEC"
        market = market_ALTCOIN

    for i in market:
        open_price_arr = []
        close_price_arr = []
        high_price_arr = []
        low_price_arr = []
        time_arr = []
        request_url = "https://min-api.cryptocompare.com/data/histoday?fsym="+str(typo)+"&tsym=USD&limit="+str(day_back)+"&aggregate=1&toTs="+str(to_time)+"&e=" + i
        returned = requests.get(request_url).json()["Data"]
        for k in returned:
            high_price_arr.append(k["high"])
            low_price_arr.append(k["low"])
            open_price_arr.append(k["open"])
            close_price_arr.append(k["close"])
            time_arr.append(datetime.datetime.utcfromtimestamp(int(k["time"])).strftime('%Y-%m-%dT%H:%M:%SZ'))
        hourly_data[i] = [high_price_arr,low_price_arr,open_price_arr,close_price_arr,time_arr]

    return hourly_data


def get_current_utc_timestamp():
    utc_datetime = datetime.datetime.now()
    utc_datetime = datetime.timedelta(minutes=-20) + utc_datetime
    utc_datetime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    a = int(time.mktime(time.strptime(utc_datetime, "%Y-%m-%d %H:%M:%S")))
    return a


def get_how_many_up_down_number(dict):
    result = {}
    for i in dict:
        up_arr = []
        down_arr = []

        arr = dict[i][0]
        count = 0
        is_up = False
        before = 0
        firs_time = True
        max_up = float('-inf')
        max_down = float('-inf')
        min_up = float('inf')
        min_down = float('inf')
        max_up_date = 0
        min_up_date = 0
        max_down_date = 0
        min_down_date = 0

        day = 0
        # this for is for up values
        for idx,deger in enumerate(arr):
            if deger >= before:
                if not is_up and not firs_time:
                    down_arr.append(count)
                    if count > max_down:
                        max_down = count
                        max_down_date =  str(day) + " - " +str(dict[i][4][idx])
                    if count < min_down:
                        min_down = count
                        min_down_date =  str(day) + " - " +str(dict[i][4][idx])
                    count = 0
                    day = dict[i][4][idx]
                is_up = True
                count += 1
            else:
                if is_up and not firs_time:
                    up_arr.append(count)
                    if count > max_up:
                        max_up = count
                        max_up_date = str(day) + " - " +str(dict[i][4][idx])
                    if count < min_up:
                        min_up = count
                        min_up_date =  str(day) + " - " +str(dict[i][4][idx])
                    count = 0
                    day = dict[i][4][idx]
                is_up = False
                count += 1
            before = deger
            if firs_time:
                firs_time = False
        if is_up:
            up_arr.append(count)
        else:
            down_arr.append(count)

        up_number = len(up_arr)
        down_number = len(down_arr)

        en_uzun_continuous_up = max(up_arr)
        en_kisa_continuous_up = min(up_arr)

        en_uzun_continuous_down = max(down_arr)
        en_kisa_continuous_down = min(down_arr)

        ortalama_continuous_up = 0
        ortalama_continuous_down = 0

        for p in up_arr:
            ortalama_continuous_up += p
        for l in down_arr:
            ortalama_continuous_down += l
        ortalama_continuous_up = float(ortalama_continuous_up) / up_number
        ortalama_continuous_down = float(ortalama_continuous_down) / down_number

        out = [up_number,down_number,en_uzun_continuous_up,en_kisa_continuous_up,en_uzun_continuous_down,en_kisa_continuous_down,ortalama_continuous_up,ortalama_continuous_down,max_up_date ,min_up_date ,max_down_date,min_down_date]

        result[i] = out
    return result


def get_open_close_statistics(dict):
    result = {}
    for i in dict:
        open_arr = dict[i][2]
        close_arr= dict[i][3]
        high_arr = dict[i][0]
        low_arr = dict[i][1]

        dif_btw_o_c = []
        dif_btw_o_high = []
        dif_btw_c_high = []
        dif_btw_o_low = []
        dif_btw_c_low = []

        positive_oc_number = 0
        negative_oc_number = 0

        for o,c,h,l in zip(open_arr,close_arr,high_arr,low_arr):
            dif_btw_o_c.append(abs(o - c))
            dif_btw_o_high.append(abs(h - o))
            dif_btw_c_high.append(abs(h - c))
            dif_btw_o_low.append(abs(o - l))
            dif_btw_c_low.append(abs(c - l))
            if c - o >= 0:
                positive_oc_number += 1
            else:
                negative_oc_number += 1

        ortalama_fark_o_c = 0
        ortalama_fark_o_h = 0
        ortalama_fark_c_h = 0
        ortalama_fark_o_l = 0
        ortalama_fark_c_l = 0

        for oc,oh,ch,ol,cl in zip(dif_btw_o_c,dif_btw_o_high,dif_btw_c_high,dif_btw_o_low,dif_btw_c_low):
            ortalama_fark_o_c += oc
            ortalama_fark_o_h += oh
            ortalama_fark_c_h += ch
            ortalama_fark_o_l += ol
            ortalama_fark_c_l += cl

        ortalama_fark_o_c = float(ortalama_fark_o_c) / len(dif_btw_o_c)
        ortalama_fark_o_h = float(ortalama_fark_o_h) / len(dif_btw_o_high)
        ortalama_fark_c_h = float(ortalama_fark_c_h) / len(dif_btw_c_high)
        ortalama_fark_o_l = float(ortalama_fark_o_l) / len(dif_btw_o_low)
        ortalama_fark_c_l = float(ortalama_fark_c_l) / len(dif_btw_c_low)

        result[i] = [positive_oc_number,negative_oc_number,ortalama_fark_o_c,ortalama_fark_o_h,ortalama_fark_c_h,ortalama_fark_o_l,ortalama_fark_c_l]

    return result







