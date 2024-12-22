import sys
import json
import tkinter as tk
from tkinter import *
import urllib.request
import webbrowser
from functools import partial
from tkinter import Tk, StringVar , ttk

def CurrencyConverter():

    ids = {"US Dollar" : 'USD', "Euros" : 'EUR', "Indian Rupees" : 'INR', "Qatar Doha" : 'QAR', "Zimbwabe Harare" : 'ZWD', "Arab Emirates Dirham" : 'AED', "Pound Sterling" : 'GBP', "Japanese Yen" : 'JPY', "Yuan Renminbi" : 'CNY'}

def CurrencyConverter():
    # Currency IDs mapping
    ids = {
        "US Dollar": 'USD',
        "Euros": 'EUR',
        "Indian Rupees": 'INR',
        "Qatar Riyal": 'QAR',
        "Zimbabwe Dollar": 'ZWD',
        "Arab Emirates Dirham": 'AED',
        "Pound Sterling": 'GBP',
        "Japanese Yen": 'JPY',
        "Yuan Renminbi": 'CNY',
        "Philippine Peso": 'PHP'
    }

    # Fixer.io API key and endpoint
    API_KEY = "fffea497a4279524f01b786d728e59f6"  # Replace with your Fixer.io API key
    API_URL = f"http://data.fixer.io/api/latest?access_key=fffea497a4279524f01b786d728e59f6"

    def convert(amt, frm, to):
        try:
            # Assertions to validate that amount and currency codes are valid
            assert isinstance(amt, (int, float)), "Amount must be a number"
            assert amt >= 0, "Amount must be non-negative"
            assert frm in ids.values(), f"Invalid input currency code: {frm}"
            assert to in ids.values(), f"Invalid output currency code: {to}"

            # Fetch exchange rates
            response = urllib.request.urlopen(API_URL)
            data = json.loads(response.read().decode('utf-8'))

            # Check for API success
            if not data.get("success"):
                return f"Error: {data.get('error', {}).get('info', 'Unknown error')}"

            # Get conversion rates
            rates = data.get("rates", {})
            if frm not in rates or to not in rates:
                return "Currency not supported"

            # Perform the conversion
            rate_from = rates[frm]
            rate_to = rates[to]
            converted_amt = amt * (rate_to / rate_from)

            # Invariant: Converted amount should always be a positive number
            assert converted_amt >= 0, "Converted amount must be non-negative"

            return f"{converted_amt:.2f}"
        except AssertionError as ae:
            return f"Assertion Error: {str(ae)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def callback():
        try:
            amt = float(in_field.get())
            assert amt >= 0, "Amount must be non-negative"
        except ValueError:
            out_amt.set('Invalid input')
            return None
        except AssertionError as ae:
            out_amt.set(str(ae))
            return None

        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            frm = ids.get(in_unit.get())
            to = ids.get(out_unit.get())
            if frm and to:
                out_amt.set(convert(amt, frm, to))
            else:
                out_amt.set('Invalid currency selected')

    # Create Tkinter window
    root = Toplevel()
    root.title("Currency Converter")

    # Main frame
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.pack(fill=BOTH, expand=1)

    # Title label
    titleLabel = Label(mainframe, text="Currency Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    titleLabel.grid(column=1, row=1, columnspan=2)

    # Input/output variables
    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()
    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Input field
    in_field = ttk.Entry(mainframe, width=30, textvariable=in_amt)
    in_field.grid(row=2, column=1, sticky=(W, E))

    # Input unit dropdown
    OptionMenu(mainframe, in_unit, *ids.keys()).grid(column=2, row=2, sticky=W)

    # Output field
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=1, row=4, sticky=(W, E))

    # Output unit dropdown
    OptionMenu(mainframe, out_unit, *ids.keys()).grid(column=2, row=4, sticky=W)

    # Calculate button
    ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=3, sticky=E)

    # Padding
    for child in mainframe.winfo_children():
        child.grid_configure(padx=20, pady=5)

    in_field.focus()