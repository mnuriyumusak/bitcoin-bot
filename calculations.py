#!/usr/bin/env python
# -*- coding: utf-8 -*-
import api_handler

my_balance_BTC = {}
my_balance_ETH = {}
my_balance_LTC = {}
my_balance_DASH = {}
my_balance_XMR = {}
my_balance_ZEC = {}

my_balance_BTC_tl = {}
my_balance_ETH_tl= {}
my_balance_LTC_tl= {}
my_balance_DASH_tl = {}
my_balance_XMR_tl = {}
my_balance_ZEC_tl = {}

my_balance_BTC["Poloniex"] = 0.01066575
my_balance_BTC["Paribu"] = 0
my_balance_ETH["Poloniex"] = 0
my_balance_LTC["Poloniex"] = 0.20840316
my_balance_DASH["Poloniex"] = 0.02989282
my_balance_XMR["Poloniex"] = 0
my_balance_ZEC["Poloniex"] = 0.03837560


BTC_dic,ETH_dic,LTC_dic,DASH_dic,XMR_dic,ZEC_dic = api_handler.initialize_prices()


def initialize_and_get_my_total_balance_in_tl():
    total = 0

    for i in my_balance_BTC:
        my_balance_BTC_tl[i] = my_balance_BTC[i] * BTC_dic[i]
        total += my_balance_BTC_tl[i]
    for i in my_balance_ETH:
        my_balance_ETH_tl[i] = my_balance_ETH[i] * ETH_dic[i]
        total += my_balance_BTC_tl[i]
    for i in my_balance_LTC:
        my_balance_LTC_tl[i] = my_balance_LTC[i] * LTC_dic[i]
        total += my_balance_BTC_tl[i]
    for i in my_balance_DASH:
        my_balance_DASH_tl[i] = my_balance_DASH[i] * DASH_dic[i]
        total += my_balance_BTC_tl[i]
    for i in my_balance_XMR:
        my_balance_XMR_tl[i] = my_balance_XMR[i] * XMR_dic[i]
        total += my_balance_BTC_tl[i]
    for i in my_balance_ZEC:
        my_balance_ZEC_tl[i] = my_balance_ZEC[i] * ZEC_dic[i]
        total += my_balance_BTC_tl[i]

    return total


def calculate_after_sell(coin_type,price,market=None):
    initialize_and_get_my_total_balance_in_tl()
    after_sell = {}

    iterating_dict = {}
    if coin_type == api_handler.BTC:
        iterating_dict = BTC_dic
    elif coin_type == api_handler.ETH:
        iterating_dict = ETH_dic
    elif coin_type == api_handler.LTC:
        iterating_dict = LTC_dic
    elif coin_type == api_handler.DASH:
        iterating_dict = DASH_dic
    elif coin_type == api_handler.XMR:
        iterating_dict = XMR_dic
    elif coin_type == api_handler.ZEC:
        iterating_dict = ZEC_dic

    if market is None:
        for i in iterating_dict:
            remain_money = api_handler.calculate_after_fee_amounts(price, i, coin_type, api_handler.SATIS,
                                                    BTC_dic, ETH_dic, LTC_dic,
                                                    DASH_dic, XMR_dic,
                                                    ZEC_dic)
            after_sell[i] = remain_money

        return after_sell
    else:
        remain_money = api_handler.calculate_after_fee_amounts(price, market, coin_type, api_handler.SATIS,
                                                               BTC_dic, ETH_dic, LTC_dic,
                                                               DASH_dic, XMR_dic,
                                                               ZEC_dic)
        return  remain_money


def calculate_after_buy(price,coin_type):
    initialize_and_get_my_total_balance_in_tl()
    after_buy = {}

    iterating_dict = {}
    if coin_type == api_handler.BTC:
        iterating_dict = BTC_dic
    elif coin_type == api_handler.ETH:
        iterating_dict = ETH_dic
    elif coin_type == api_handler.LTC:
        iterating_dict = LTC_dic
    elif coin_type == api_handler.DASH:
        iterating_dict = DASH_dic
    elif coin_type == api_handler.XMR:
        iterating_dict = XMR_dic
    elif coin_type == api_handler.ZEC:
        iterating_dict = ZEC_dic

    for i in iterating_dict:
        remain_money = api_handler.calculate_after_fee_amounts(price, i, coin_type, api_handler.ALIS,
                                                BTC_dic, ETH_dic, LTC_dic,
                                                DASH_dic, XMR_dic,
                                                ZEC_dic)
        how_much = remain_money / iterating_dict[i]
        after_buy[i] = how_much

    return after_buy


def find_max(dict):
    max = -10000000
    market = 1
    for i in dict:
        if dict[i] > max:
            max = dict[i]
            market = i

    return max,market


def return_best_arbitrage(coin_type,price = None):
    if price is None:
        price = 1000
    else:
        price = price

    after_buy = {}
    kar = {}

    iterating_dict = {}
    if coin_type == api_handler.BTC:
        iterating_dict = BTC_dic
    elif coin_type == api_handler.ETH:
        iterating_dict = ETH_dic
    elif coin_type == api_handler.LTC:
        iterating_dict = LTC_dic
    elif coin_type == api_handler.DASH:
        iterating_dict = DASH_dic
    elif coin_type == api_handler.XMR:
        iterating_dict = XMR_dic
    elif coin_type == api_handler.ZEC:
        iterating_dict = ZEC_dic

    for i in iterating_dict:
        remain_money = api_handler.calculate_after_fee_amounts(price, i, coin_type, api_handler.ALIS,
                                                BTC_dic, ETH_dic, LTC_dic,
                                                DASH_dic, XMR_dic,
                                                ZEC_dic)
        remain_money = api_handler.calculate_after_fee_amounts(remain_money, i, coin_type, api_handler.SATIS,
                                                               BTC_dic, ETH_dic, LTC_dic,
                                                               DASH_dic, XMR_dic,
                                                               ZEC_dic)
        how_much = remain_money / iterating_dict[i]
        after_buy[i] = how_much

    max_buy,market_buy = find_max(after_buy)
    # print "You should buy from "+ str(market_buy)
    for i in iterating_dict:
        curent_money = max_buy * iterating_dict[i]
        remain_money = api_handler.calculate_after_fee_amounts(curent_money, i, coin_type, api_handler.SATIS,
                                                              BTC_dic, ETH_dic, LTC_dic,
                                                              DASH_dic, XMR_dic,
                                                              ZEC_dic)
        kar[i] = remain_money - price

    max_sell, market_sell = find_max(kar)
    # print "You should sell from "+ str(market_sell)
    # print "Your total gain is " + str(max_sell)

    return [market_buy,market_sell,max_sell]


def calculate_money_after_sell_current_market(is_cash):
    BTC = {}
    ETH = {}
    LTC = {}
    DASH = {}
    XMR = {}
    ZEC = {}

    BTC_kar = {}
    ETH_kar= {}
    LTC_kar= {}
    DASH_kar = {}
    XMR_kar = {}
    ZEC_kar = {}

    initialize_and_get_my_total_balance_in_tl()
    for i in my_balance_BTC_tl:
        BTC[i] = calculate_after_sell(api_handler.BTC,my_balance_BTC_tl[i],i) / BTC_dic[i]
    for i in my_balance_ETH_tl:
        ETH[i] = calculate_after_sell(api_handler.ETH,my_balance_ETH_tl[i],i) / ETH_dic[i]
    for i in my_balance_LTC_tl:
        LTC[i] = calculate_after_sell(api_handler.LTC,my_balance_LTC_tl[i],i) / LTC_dic[i]
    for i in my_balance_DASH_tl:
        DASH[i] = calculate_after_sell(api_handler.DASH,my_balance_DASH_tl[i],i) / DASH_dic[i]
    for i in my_balance_XMR_tl:
        XMR[i] = calculate_after_sell(api_handler.XMR,my_balance_XMR_tl[i],i) / XMR_dic[i]
    for i in my_balance_ZEC_tl:
        ZEC[i] = calculate_after_sell(api_handler.ZEC,my_balance_ZEC_tl[i],i) / ZEC_dic[i]

    tmp = {}
    for i in BTC:
        for k in api_handler.market_BTC:
            volume = BTC[i] * BTC_dic[k]
            out = calculate_after_sell(api_handler.BTC,volume,k)
            tmp[k] = out
        max_BTC,market_BTC = find_max(tmp)
        BTC_kar[i] = [market_BTC,max_BTC - my_balance_BTC_tl[i]]

    tmp = {}
    for i in ETH:
        for k in api_handler.market_ALTCOIN:
            volume = ETH[i] * ETH_dic[k]
            out = calculate_after_sell(api_handler.ETH,volume,k)
            tmp[k] = out
        max_ETH,market_ETH = find_max(tmp)
        ETH_kar[i] = [market_ETH, max_ETH - my_balance_ETH_tl[i]]

    tmp = {}
    for i in LTC:
        for k in api_handler.market_LTC:
            volume = LTC[i] * LTC_dic[k]
            out = calculate_after_sell(api_handler.LTC,volume,k)
            tmp[k] = out
        max_LTC,market_LTC = find_max(tmp)
        LTC_kar[i] = [market_LTC, max_LTC - my_balance_LTC_tl[i]]

    tmp = {}
    for i in DASH:
        for k in api_handler.market_ALTCOIN:
            volume = DASH[i] * DASH_dic[k]
            out = calculate_after_sell(api_handler.DASH,volume,k)
            tmp[k] = out
        max_DASH,market_DASH = find_max(tmp)
        DASH_kar[i] = [market_DASH, max_DASH - my_balance_DASH_tl[i]]

    tmp = {}
    for i in XMR:
        for k in api_handler.market_ALTCOIN:
            volume = XMR[i] * XMR_dic[k]
            out = calculate_after_sell(api_handler.XMR,volume,k)
            tmp[k] = out
        max_XMR,market_XMR = find_max(tmp)
        XMR_kar[i] = [market_XMR, max_XMR - my_balance_XMR_tl[i]]

    tmp = {}
    for i in ZEC:
        for k in api_handler.market_ALTCOIN:
            volume = ZEC[i] * ZEC_dic[k]
            out = calculate_after_sell(api_handler.ZEC,volume,k)
            tmp[k] = out
        max_ZEC,market_ZEC = find_max(tmp)
        ZEC_kar[i] = [market_ZEC, max_ZEC - my_balance_ZEC_tl[i]]

    if not is_cash:
        return BTC_kar,ETH_kar,LTC_kar,DASH_kar,XMR_kar,ZEC_kar
    else:
        for i in BTC_kar:
            volume = BTC_kar[i][1] + my_balance_BTC_tl[i]
            remain = calculate_after_sell_from_turk_borsasi(api_handler.BTC, volume, i)
            remain = remain - my_balance_BTC_tl[i]
            BTC_kar[i][1] = remain
        for i in ETH_kar:
            volume = ETH_kar[i][1] + my_balance_ETH_tl[i]
            remain = calculate_after_sell_from_turk_borsasi(api_handler.LTC, volume, i)
            remain = remain - my_balance_ETH_tl[i]
            ETH_kar[i][1] = remain
        for i in LTC_kar:
            volume = LTC_kar[i][1] + my_balance_LTC_tl[i]
            remain = calculate_after_sell_from_turk_borsasi(api_handler.LTC, volume, i)
            remain = remain - my_balance_LTC_tl[i]
            LTC_kar[i][1] = remain
        for i in DASH_kar:
            volume = DASH_kar[i][1] + my_balance_DASH_tl[i]
            remain = calculate_after_sell_from_turk_borsasi(api_handler.DASH, volume, i)
            remain = remain - my_balance_DASH_tl[i]
            DASH_kar[i][1] = remain
        for i in XMR_kar:
            volume = XMR_kar[i][1] + my_balance_XMR_tl[i]
            remain = calculate_after_sell_from_turk_borsasi(api_handler.XMR, volume, i)
            remain = remain - my_balance_XMR_tl[i]
            XMR_kar[i][1] = remain
        for i in ZEC_kar:
            volume = ZEC_kar[i][1] + my_balance_ZEC_tl[i]
            remain = calculate_after_sell_from_turk_borsasi(api_handler.ZEC, volume, i)
            remain = remain - my_balance_ZEC_tl[i]
            ZEC_kar[i][1] = remain

        return BTC_kar, ETH_kar, LTC_kar, DASH_kar, XMR_kar, ZEC_kar


def calculate_after_sell_from_turk_borsasi(coin_type,volume,market):
    remain = calculate_after_sell(coin_type, volume, market)

    if coin_type != api_handler.BTC:
        remain = calculate_after_sell(api_handler.BTC, remain, market)

    remain1 = calculate_after_sell(api_handler.BTC, remain, "Paribu")
    remain2 = calculate_after_sell(api_handler.BTC, remain, "Koinim")

    if remain1 > remain2:
        return remain1
    else:
        return  remain2

def give_same_type_suggestion(is_cash):
    BTC_kar, ETH_kar, LTC_kar, DASH_kar, XMR_kar, ZEC_kar = calculate_money_after_sell_current_market(is_cash)
    suggestion = {}
    for i in BTC_kar:
        if BTC_kar[i][1] > 0:
            suggestion["BTC"] = [i,BTC_kar[i][0],BTC_kar[i][1]]
    for i in ETH_kar:
        if ETH_kar[i][1] > 0:
            suggestion["ETH"] = [i,ETH_kar[i][0],ETH_kar[i][1]]
    for i in LTC_kar:
        if LTC_kar[i][1] > 0:
            suggestion["LTC"] = [i,LTC_kar[i][0],LTC_kar[i][1]]
    for i in DASH_kar:
        if DASH_kar[i][1] > 0:
            suggestion["DASH"] = [i,DASH_kar[i][0],DASH_kar[i][1]]
    for i in XMR_kar:
        if XMR_kar[i][1] > 0:
            suggestion["XMR"] = [i,XMR_kar[i][0],XMR_kar[i][1]]
    for i in ZEC_kar:
        if ZEC_kar[i][1] > 0:
            suggestion["ZEC"] = [i,ZEC_kar[i][0],ZEC_kar[i][1]]

    for i in suggestion:
        if suggestion[i][2] > 0:
            print "You should sell your " + str(i) +" from " + str(suggestion[i][0]) + " and sell it to " + str(suggestion[i][1]) + ". Total gain is " + str(suggestion[i][2]) + " TL"


def examine_mix_suggestion_dict(dict):
    max = -100000
    your_current = ""
    buy_from = ""
    sell_to = ""
    ctype = ""
    for i in dict:
        if dict[i][2] > max:
            max = dict[i][2]
            your_current = dict[i][3]
            buy_from = dict[i][0]
            sell_to = dict[i][1]
            ctype = i

    if ctype == 0:
        ctype = "BTC"
    elif ctype == 1:
        ctype = "ETH"
    elif ctype == 2:
        ctype = "LTC"
    elif ctype == 3:
        ctype = "DASH"
    elif ctype == 4:
        ctype = "XMR"
    elif ctype == 5:
        ctype = "ZEC"

    return [your_current,buy_from,sell_to,max,ctype]


def give_mix_type_suggestion(is_cash):
    BTC_kar = {}
    ETH_kar= {}
    LTC_kar= {}
    DASH_kar = {}
    XMR_kar = {}
    ZEC_kar = {}

    initialize_and_get_my_total_balance_in_tl()

    for i in my_balance_BTC_tl:
        BTC_kar[i] = calculate_after_sell(api_handler.BTC,my_balance_BTC_tl[i],i)
    for i in my_balance_ETH_tl:
        ETH_kar[i] = calculate_after_sell(api_handler.ETH,my_balance_ETH_tl[i],i)
    for i in my_balance_LTC_tl:
        LTC_kar[i] = calculate_after_sell(api_handler.LTC,my_balance_LTC_tl[i],i)
    for i in my_balance_DASH_tl:
        DASH_kar[i] = calculate_after_sell(api_handler.DASH,my_balance_DASH_tl[i],i)
    for i in my_balance_XMR_tl:
        XMR_kar[i] = calculate_after_sell(api_handler.XMR,my_balance_XMR_tl[i],i)
    for i in my_balance_ZEC_tl:
        ZEC_kar[i] = calculate_after_sell(api_handler.ZEC,my_balance_ZEC_tl[i],i)

    suggestions = []
    types = [api_handler.BTC,api_handler.ETH,api_handler.LTC,api_handler.DASH,api_handler.XMR,api_handler.ZEC]
    pack = [BTC_kar,ETH_kar,LTC_kar,DASH_kar,XMR_kar,ZEC_kar]

    index = 0
    for kar_type in pack:
        tmp = {}
        tmp2 = []
        for i in kar_type:
            for k in types:
                out = return_best_arbitrage(k, kar_type[i])
                out.append(i)
                tmp[k] = out
            tmp3 = (examine_mix_suggestion_dict(tmp))
            tmp3.append(kar_type[i])
            tmp2.append(tmp3)
        maximu = 0
        for idx,i in enumerate(tmp2):
            if i[3] > 0 and i[3] > tmp2[maximu][3]:
                maximu = idx
        typo = ""
        if index == 0:
            typo = "BTC"
        elif index == 1:
            typo = "ETH"
        elif index == 2:
            typo = "LTC"
        elif index == 3:
            typo = "DASH"
        elif index == 4:
            typo = "XMR"
        elif index == 5:
            typo = "ZEC"

        if is_cash:
            volume = tmp2[maximu][3] + tmp2[maximu][5]
            miktar = volume / BTC_dic[tmp2[maximu][2]]
            volumes = []
            v1 = miktar * BTC_dic["Paribu"]
            v1 = calculate_after_sell(api_handler.BTC, v1, "Paribu")
            v2 = miktar * BTC_dic["Koinim"]
            v2 = calculate_after_sell(api_handler.BTC, v1, "Koinim")
            volumes.append(v1)
            volumes.append(v2)
            remain = max(volumes)
            remain = remain - tmp2[maximu][5]
            tmp2[maximu][3] = remain
        if tmp2[maximu][3] > 0:
            suggestions.append("Your " + str(typo) + " in " + str(tmp2[maximu][0]) +". You should sell them and buy " + str(tmp2[maximu][4]) +" from " + str(tmp2[maximu][1]) +" and sell them from "+str(tmp2[maximu][2])+ ". Your gain is "+ str(tmp2[maximu][3]) + " TL")
        index += 1

    for i in suggestions:
        print i



# Example Working Code
give_same_type_suggestion(True)
give_mix_type_suggestion(True)
