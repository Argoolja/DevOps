#!/usr/bin/env python3
#https://rapidapi.com/fyhao/api/currency-exchange

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests
def label(from_currency, to_currency, client, provider):
    out_put_field.create_text(50,20,text="Intermediary \ncurrency")
    out_put_field.create_text(150,20,text=from_currency + " to intermediary \ncurrency.")
    out_put_field.create_text(260,20,text="Intermediary \ncurrency to " + to_currency)
    out_put_field.create_text(350,20,text="PROFIT!")
    out_put_field.create_text(80,215,text="Best for consumer: " + client)
    out_put_field.create_text(95,235,text="Best for service provider: " + provider)
    
def clean():
    out_put_field.delete('all')
    out_put_field.create_text(200,100,text="Loading...")
    win.update()
    


def draw(all_currencies):
    topy = 40
    sizes_x = [65, 120, 120, 65]
    size_y = 20

    for currency in all_currencies:
        topx = 10
        for i in range(len(currency)):
            out_put_field.create_rectangle(topx, topy, topx + sizes_x[i], topy + size_y, fill="white")
            mid_x = topx + sizes_x[i]/2
            mid_y = topy + size_y/2
            out_put_field.create_text(mid_x, mid_y, text=currency[i])
            topx += sizes_x[i]
        topy += size_y


def get_amount():
        error = False
        try:
            float(amount_input.get())
            return amount_input.get(), error
        except:
            messagebox.showerror(title="Incorrect amount", message="Amount should be a number")
            error = True
            return 100, error

def exchange_rates(from_currency, to_currency, amount):
    error = False
    url = "https://currency-exchange.p.rapidapi.com/exchange"
    available_currencies = ["SGD","USD", "EUR", "AUD", "JPY", "CAD", "DKK", "THB", "VND", "GBP"]
    result = []
    try:
        available_currencies.remove(from_currency)
        available_currencies.remove(to_currency)
    except:
            messagebox.showerror(title="Incorrect currencies", message="Can't convert to same currency or without currency")
            error = True
            return [], error

    for intermediary_currency in available_currencies:
        exchange = []
        querystring = {"to":intermediary_currency,"from":from_currency,"q":amount}
        headers = {
            'x-rapidapi-key': "682677e02amsh4ba20d461819455p1690a8jsnd7c111104f2a",
            'x-rapidapi-host': "currency-exchange.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        intermediary_currency_value = round(float(amount)*response.json(),4)

        querystring = {"to":to_currency,"from":intermediary_currency,"q":str(intermediary_currency_value)}
        response = requests.request("GET", url, headers=headers, params=querystring)
        to_currency_value =  round(intermediary_currency_value*response.json(),4)
        profit = "0.00" + str(to_currency_value).split(".")[1][2:]
        exchange.append(intermediary_currency)
        exchange.append(intermediary_currency_value)
        exchange.append(to_currency_value)
        exchange.append(profit)
        result.append(exchange)
        
    return result, error

def calc_bests(all_currencies):
    best_client = 0
    best_provider = 0
    best_client_currency = ""
    best_provider_currency = ""
    for currency in all_currencies:
        if best_client < float(currency[2]):
            best_client = float(currency[2])
            best_client_currency = currency[0]
        if best_provider < float(currency[3]):
            best_provider = float(currency[3])
            best_provider_currency = currency[0]
    return best_client_currency, best_provider_currency

def run(from_currency, to_currency):
    clean()
    amount_error = False
    conversion_error = False
    amount, amount_error = get_amount()
    if not amount_error:
        all_currencies, conversion_error = exchange_rates(from_currency, to_currency, amount)
        if not conversion_error:
            client, provider = calc_bests(all_currencies)
            draw(all_currencies)
            label(from_currency, to_currency, client, provider)
    else:
        out_put_field.delete('all')

# GUI
win = Tk()
win.title("Currency exchange")
win.resizable(False, False)
win.geometry("400x450")

convert = ttk.Button(win, text="convert", command = lambda : run(clicked_from.get(), clicked_to.get()))
convert.place(x=50, y=160,height=25, width=80)

text_output = Text(win, width=25, height=9)
text_output.place(x=450, y=30)

out_put_field = Canvas(win, width=400, height=250, background="white")
out_put_field.place(x=0, y=200)


amount_input = ttk.Entry(win)
amount_label = ttk.Label(win, text="Amount:")
amount_label.place(x=50, y=0)
amount_input.place(x=50, y=20, height=25, width=150)

options = [" ", "SGD","USD", "EUR", "AUD", "JPY", "CAD", "DKK", "THB", "VND", "GBP"]
  
clicked_from = StringVar()
clicked_from.set("USD")
from_currency = ttk.OptionMenu( win, clicked_from , *options )
from_label = ttk.Label(win, text="From currency:")
from_label.place(x=50, y=50)
from_currency.place(x=50, y=70, height=25, width=100)

clicked_to = StringVar()
to_currency = ttk.OptionMenu( win , clicked_to , *options )
from_lable = ttk.Label(win, text="To currency:")
from_lable.place(x=50, y=100)
to_currency.place(x=50, y=120, height=25, width=100)

win.mainloop()