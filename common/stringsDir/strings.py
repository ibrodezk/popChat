# -*- coding: utf-8 -*-
#strings variables
he = "he"
en = "en"
languages = [he,en]
#translation variables
Strings = {
    'heHome' : "בית",
    'enHome' : "Home",
    'heSell' : "מכירה",
    'enSell' : "Sell",
    'heRent': "השכרה",
    'enRent': "Rent",
    'heTrade': "החלפה",
    'enTrade': "Trade",
    'heSignIn': "התחברות",
    'enSignIn': "Sign In",
    'heAgent': "סוכן",
    'enAgent': "Agent",
    'he': "",
    'en': "",
    #'he': "",
    #'en': "",

}




# context variables
home = "home"
def getNebBarCon(language):
    return {
        "home" : Strings[language + 'Home'],
        "sales" : Strings[language + 'Sell'],
        "rent" : Strings[language + 'Rent'],
        "trade" : Strings[language + 'Trade'],
        "signin" : Strings[language + 'SignIn'],
        "agent" : Strings[language + 'Agent']

    }

def getFormSearchSales():
    return {
        "date_help_text" : "Enter a date between now and 4 weeks (default 3)"
    }

def getGlobalCon(language):
    return {
        "home" : Strings[language + 'Home'],
        "sales" : Strings[language + 'Sell'],
        "rent" : Strings[language + 'Rent'],
        "trade" : Strings[language + 'Trade'],
        "signin" : Strings[language + 'SignIn'],
        "agent" : Strings[language + 'Agent']

    }

strings_Title = "דירהקל"

def navbarStrings(language):
    if(language == en):
        return getNebBarCon(en)
    if(language == he):
        return getNebBarCon(he)
    return enNavBarCon

def getTitle():
    return "test"