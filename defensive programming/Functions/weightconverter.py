import sys
import json
import tkinter as tk
from tkinter import *
import urllib.request
import webbrowser
from functools import partial
from tkinter import Tk, StringVar , ttk

def WeightConverter():
    # Conversion factors to convert from units to grams (g)
    factors = {
        'kg': 1000, 'hg': 100, 'dg': 10, 'g': 1, 
        'deg': 0.1, 'cg': 0.01, 'mg': 0.001
    }

    # Dictionary mapping user-friendly names to factor keys
    unit_ids = {
        "Kilogram": 'kg', "Hectagram": 'hg', "Decagram": 'dg', 
        "Gram": 'g', "Decigram": 'deg', "Centigram": 'cg', "Milligram": 'mg'
    }

    def convert(amt, frm, to):
        """
        Convert the amount from one unit to another.
        Converts both to and from grams.
        """
        # Assertions for input validation
        assert isinstance(amt, (int, float)), "Amount must be a number"
        assert amt >= 0, "Amount must be non-negative"
        assert frm in factors, f"Invalid from unit: {frm}"
        assert to in factors, f"Invalid to unit: {to}"

        if frm == to:
            return amt  # No conversion needed if units are the same
        # Convert to grams first and then to the target unit
        amt_in_grams = amt * factors[frm]
        # Invariant: Conversion should result in a positive value
        result = amt_in_grams / factors[to]
        assert result >= 0, "Conversion result must be non-negative"
        return result

    def callback():
        """
        Handle the conversion logic when the user clicks the Calculate button.
        """
        try:
            amt = float(in_field.get())  # Get the input value
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

        # Get the units from the dropdowns
        frm = unit_ids[in_unit.get()]
        to = unit_ids[out_unit.get()]

        # Perform the conversion
        try:
            result = convert(amt, frm, to)
            out_amt.set(f"{result:.4f}")  # Display the result with 4 decimal places
        except AssertionError as ae:
            out_amt.set(str(ae))

    # Initiate window
    root = Toplevel()
    root.title("Weight Converter")

    # Frame for content
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.pack(fill=BOTH, expand=1)

    titleLabel = Label(mainframe, text="Weight Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    titleLabel.grid(column=1, row=1)

    # Variables to hold input and output values
    in_amt = StringVar(value='0')
    out_amt = StringVar()

    in_unit = StringVar(value='Select Unit')
    out_unit = StringVar(value='Select Unit')

    # Add input field for amount
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, *unit_ids.keys())
    in_select.grid(column=3, row=1, sticky=W)

    # Add output field and drop-down for output unit
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    out_select = OptionMenu(mainframe, out_unit, *unit_ids.keys())
    out_select.grid(column=3, row=3, sticky=W)

    # Add Calculate button
    calc_button = ttk.Button(mainframe, text="Calculate", command=callback)
    calc_button.grid(column=2, row=2, sticky=E)

    # Configure spacing for layout
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Focus on the input field initially
    in_field.focus()